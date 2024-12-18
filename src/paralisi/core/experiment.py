# src/pyisi/core/experiment.py
"""Core experiment handling for ISI analysis.

This module provides the main experiment class for handling Intrinsic Signal Imaging
(ISI) experiments, including data loading, processing, and analysis.
"""
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

import numpy as np
import torch

from .config import ExperimentConfig
from .data_types import TrialData
from .exceptions import (
    ConfigurationError,
    DataLoadingError,
    ProcessingError,
    StorageError
)
from ..utils.cuda_setup import setup_cuda
from ..processing.trial_processor import process_trial
from ..io.readers import load_trial_data
from ..io.writers import save_processed_data

logger = logging.getLogger(__name__)

class ExperimentStatus(Enum):
    """Status tracking for experiment processing."""
    INITIALIZED = auto()
    LOADING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()

    def __str__(self) -> str:
        return self.name.lower()

class ISIExperiment:
    """Main class for handling ISI experiments.

    This class manages the full lifecycle of an ISI experiment, including:
    - Data loading and validation
    - Trial processing
    - Analysis and results generation
    - Result storage and export
    """

    def __init__(
        self,
        config: ExperimentConfig,
        device: Optional[torch.device] = None
    ) -> None:
        """Initialize an ISI experiment.

        Args:
            config: Configuration parameters for the experiment
            device: Optional torch device for GPU acceleration

        Raises:
            ConfigurationError: If configuration is invalid
            RuntimeError: If GPU is requested but not available
        """
        self._validate_config(config)
        self.config = config

        # Setup device and GPU if needed
        try:
            self.device = setup_cuda(device, config.processing.mode)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to setup device: {str(e)}")

        # Initialize data structures
        self.raw_data: Dict[str, np.ndarray] = {}
        self.processed_trials: Dict[int, TrialData] = {}
        self.analysis_results: Dict[str, Any] = {}

        # State tracking
        self.status = ExperimentStatus.INITIALIZED
        self._current_trial = 0

        logger.info(f"Initialized experiment: {config.name}")

    @staticmethod
    def _validate_config(config: ExperimentConfig) -> None:
        """Validate experiment configuration.

        Args:
            config: Configuration to validate

        Raises:
            ConfigurationError: If configuration parameters are invalid
        """
        if not config.data_path.exists():
            raise ConfigurationError(f"Data path does not exist: {config.data_path}")

        if not config.acquisition.sampling_rate > 0:
            raise ConfigurationError("Invalid sampling rate")

        # Add additional validation as needed

    def load_data(self, trial_indices: Optional[List[int]] = None) -> None:
        """Load experimental data from disk.

        Args:
            trial_indices: Optional list of specific trials to load. If None,
                         loads all trials.

        Raises:
            DataLoadingError: If data loading fails
        """
        self._update_status(ExperimentStatus.LOADING)
        logger.info("Loading experimental data...")

        try:
            self._load_trials(trial_indices)
            logger.info(f"Loaded {len(self.raw_data)} trials")

        except Exception as e:
            self._handle_error(f"Error loading data: {str(e)}")
            raise DataLoadingError(f"Failed to load data: {str(e)}") from e

    def _load_trials(self, trial_indices: Optional[List[int]] = None) -> None:
        """Helper method to load trial data.

        Args:
            trial_indices: Optional list of specific trials to load
        """
        if trial_indices is None:
            trial_indices = range(self.config.acquisition.frames_per_trial)

        for trial_idx in trial_indices:
            data = load_trial_data(
                self.config.data_path,
                trial_idx,
                self.config.acquisition
            )
            self.raw_data[f"trial_{trial_idx}"] = data

        self._current_trial = 0

    def process_trials(
        self,
        start_trial: int = 0,
        end_trial: Optional[int] = None
    ) -> None:
        """Process experimental trials.

        Args:
            start_trial: Index of first trial to process
            end_trial: Optional index of last trial to process

        Raises:
            ProcessingError: If processing fails
            ValueError: If trial indices are invalid
        """
        self._update_status(ExperimentStatus.PROCESSING)
        logger.info("Processing trials...")

        try:
            self._validate_trial_range(start_trial, end_trial)
            self._process_trial_range(start_trial, end_trial or len(self.raw_data))

            self._update_status(ExperimentStatus.COMPLETED)
            logger.info("Trial processing completed")

        except Exception as e:
            self._handle_error(f"Error processing trials: {str(e)}")
            raise ProcessingError(f"Failed to process trials: {str(e)}") from e

    def _validate_trial_range(self, start_trial: int, end_trial: Optional[int]) -> None:
        """Validate trial range parameters.

        Args:
            start_trial: Starting trial index
            end_trial: Optional ending trial index

        Raises:
            ValueError: If trial range is invalid
        """
        if start_trial < 0:
            raise ValueError("start_trial must be non-negative")

        if end_trial is not None:
            if end_trial <= start_trial:
                raise ValueError("end_trial must be greater than start_trial")
            if end_trial > len(self.raw_data):
                raise ValueError("end_trial exceeds available trials")

    def _process_trial_range(self, start_trial: int, end_trial: int) -> None:
        """Process a range of trials.

        Args:
            start_trial: Starting trial index
            end_trial: Ending trial index
        """
        for trial_idx in range(start_trial, end_trial):
            self._current_trial = trial_idx
            trial_key = f"trial_{trial_idx}"

            if trial_key not in self.raw_data:
                raise ValueError(f"Trial {trial_idx} not loaded")

            processed_data = process_trial(
                self.raw_data[trial_key],
                self.config.processing,
                self.device
            )

            self.processed_trials[trial_idx] = processed_data
            logger.debug(f"Processed trial {trial_idx}")

    def save_results(self, output_path: Optional[Path] = None) -> None:
        """Save processed results to disk.

        Args:
            output_path: Optional specific path for output. If None, uses
                        configured output path.

        Raises:
            StorageError: If saving results fails
            ValueError: If no results exist
        """
        if not self.processed_trials:
            raise ValueError("No processed results to save")

        output_path = output_path or self.config.output_path

        try:
            save_processed_data(
                self.processed_trials,
                output_path,
                self.config
            )
            logger.info(f"Saved results to {output_path}")

        except Exception as e:
            error_msg = f"Error saving results: {str(e)}"
            logger.error(error_msg)
            raise StorageError(error_msg) from e

    def _update_status(self, new_status: ExperimentStatus) -> None:
        """Update experiment status with logging.

        Args:
            new_status: New status to set
        """
        self.status = new_status
        logger.debug(f"Status updated to: {new_status}")

    def _handle_error(self, error_msg: str) -> None:
        """Handle error state with logging.

        Args:
            error_msg: Error message to log
        """
        self._update_status(ExperimentStatus.ERROR)
        logger.error(error_msg)

    @property
    def progress(self) -> float:
        """Calculate processing progress.

        Returns:
            Float between 0 and 1 indicating progress
        """
        if not self.raw_data:
            return 0.0
        return self._current_trial / len(self.raw_data)

    def get_trial_data(self, trial_idx: int) -> Optional[TrialData]:
        """Get processed data for a specific trial.

        Args:
            trial_idx: Index of trial to retrieve

        Returns:
            Processed trial data if available, None otherwise
        """
        return self.processed_trials.get(trial_idx)

# src/paralisi/core/experiments/isi_experiment.py

from pathlib import Path
from typing import Optional, List, Dict, Any
import torch
import numpy as np
from datetime import datetime
from .base_experiment import BaseExperiment
from ..configurations.experiment_config import ExperimentConfig
from ...io.loaders.trial_data_loader import TrialDataLoader
from ...processing.trial_processor import ConditionProcessor
from ...utils.cuda_setup import setup_cuda
from ...io.writers.data_writer import DataWriter

class ISIExperiment(BaseExperiment):
    """Class for handling ISI experiments."""

    def __init__(self,
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
        super().__init__(config)
        try:
            self.device = setup_cuda(device, config.processing.mode)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to setup device: {str(e)}")

        # Initialize the trial data loader
        self.trial_data_loader = TrialDataLoader(config.data_path)

        # Initialize the condition processor
        self.condition_processor = ConditionProcessor(image_size=(config.acquisition.image_height, config.acquisition.image_width))

        # Initialize data containers
        self.raw_data: Dict[str, np.ndarray] = {}
        # Using Dict[int, Dict[str, Any]] as TrialData type alias
        self.processed_trials: Dict[int, Dict[str, Any]] = {}

    def _load_trials(self, trial_indices: Optional[List[int]] = None) -> None:
        """Helper method to load trial data.

        Args:
            trial_indices: Optional list of specific trials to load
        """
        if trial_indices is None:
            trial_indices = list(range(self.config.acquisition.frames_per_trial))

        for trial_idx in trial_indices:
            data = self.trial_data_loader.load_trial_data(
                trial_idx,
                self.config.acquisition
            )
            self.raw_data[f"trial_{trial_idx}"] = data

        self._current_trial = 0

    def _process_trial_range(self, start_trial: int, end_trial: int) -> None:
        """Process a range of trials.

        Args:
            start_trial: Starting trial index
            end_trial: Ending trial index
        """
        trials = [self.raw_data[f"trial_{idx}"] for idx in range(start_trial, end_trial) if f"trial_{idx}" in self.raw_data]

        # Use condition processor to process trials
        processed_data = self.condition_processor.process_condition_data(trials, self.config.processing)

        for i, key in enumerate(range(start_trial, end_trial)):
            self.processed_trials[key] = {k: v[i] for k, v in processed_data.items()}

    def _save_results_to_disk(self, output_path: Path) -> None:
        """Helper method to save results to disk.

        Args:
            output_path: Path to save the results
        """
        # Initialize DataWriter
        writer = DataWriter(output_path)

        # Transform processed_trials to match the expected type
        transformed_data = {f"trial_{k}": v if isinstance(v, np.ndarray) else np.array(v)
                            for k, v in self.processed_trials.items()}

        # Save processed data using DataWriter
        writer.save_processed_data(
            data=transformed_data,
            metadata={'processing_date': datetime.now().isoformat()},
            animal_id=self.config.animal_id,
            experiment_id=self.config.experiment_id,
            format='hdf5'
        )

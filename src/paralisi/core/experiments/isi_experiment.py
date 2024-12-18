# src/paralisi/core/experiments/isi_experiment.py

from pathlib import Path
from typing import Optional, List
import torch
import numpy as np
from .base_experiment import BaseExperiment
from ..configurations.experiment_config import ExperimentConfig
from ..io.readers import load_trial_data  # Updated import
from ..processing.trial_processor import process_trial
from ..utils.cuda_setup import setup_cuda
from ..io.writers.data_writer import DataWriter  # Updated import

class ISIExperiment(BaseExperiment):
    """Class for handling ISI experiments."""

    def __init__(self, config: ExperimentConfig, device: Optional[torch.device] = None) -> None:
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

    def _save_results_to_disk(self, output_path: Path) -> None:
        """Helper method to save results to disk.

        Args:
            output_path: Path to save the results
        """
        # Initialize DataWriter
        writer = DataWriter(output_path)

        # Save processed data using DataWriter
        writer.save_processed_data(
            data=self.processed_trials,
            metadata={'processing_date': datetime.now().isoformat()},
            animal_id="animal_id_placeholder",  # Replace with actual animal ID
            experiment_id="experiment_id_placeholder",  # Replace with actual experiment ID
            format='hdf5'  # or 'npz' based on your requirement
        )

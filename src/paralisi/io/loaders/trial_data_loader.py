# src/paralisi/io/loaders/trial_data_loader.py

"""Trial Data Loader."""

from pathlib import Path
import numpy as np
from typing import Any

class TrialDataLoader:
    """Class to handle trial data loading."""

    def __init__(self, data_path: Path):
        self.data_path = data_path

    def load_trial_data(self, trial_idx: int, acquisition_config: Any) -> np.ndarray:
        """Load trial data from the specified path.

        Args:
            trial_idx: Index of the trial to load
            acquisition_config: Acquisition configuration details

        Returns:
            Loaded trial data
        """
        # Add logic to load the trial data based on the given parameters
        # This is a placeholder implementation
        trial_file = self.data_path / f"trial_{trial_idx}.npy"
        if not trial_file.exists():
            raise FileNotFoundError(f"Trial file not found: {trial_file}")
        trial_data = np.load(trial_file)
        return trial_data

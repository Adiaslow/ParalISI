# src/paralisi/io/loaders/trial_data_loader.py

"""Trial Data Loader."""

from pathlib import Path
import numpy as np
from typing import Any, Union
from .numpy_loader import NumpyLoader
from .hdf5_loader import HDF5Loader
from .tiff_loader import TiffLoader

class TrialDataLoader:
    """Class to handle trial data loading."""

    def __init__(self, data_path: Path):
        """Initialize the TrialDataLoader with the base data path.

        Args:
            data_path (Path): Path to the directory containing trial data files.
        """
        self.data_path = data_path

    def load_trial_data(self, trial_idx: int, acquisition_config: Any) -> np.ndarray:
        """Load trial data from the specified path.

        Args:
            trial_idx (int): Index of the trial to load.
            acquisition_config (Any): Acquisition configuration details, including data format.

        Returns:
            np.ndarray: Loaded trial data.

        Raises:
            FileNotFoundError: If the trial file does not exist.
            ValueError: If the data format is unsupported.
        """
        data_format = acquisition_config.data_format
        file_path = self.data_path / f"trial_{trial_idx}.{data_format}"

        if not file_path.exists():
            raise FileNotFoundError(f"Trial file not found: {file_path}")

        if data_format == 'npy':
            return NumpyLoader.load(file_path)
        elif data_format == 'h5':
            return HDF5Loader.load(file_path, acquisition_config.dataset_name)
        elif data_format == 'tiff':
            return TiffLoader.load(file_path)
        else:
            raise ValueError(f"Unsupported data format: {data_format}")

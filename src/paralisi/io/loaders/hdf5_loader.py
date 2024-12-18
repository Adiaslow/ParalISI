# src/paralisi/io/loaders/hdf5_loader.py

"""Module for loading data from HDF5 files."""

import h5py
from pathlib import Path
import numpy as np

class HDF5Loader:
    """Class for loading HDF5 files."""

    @staticmethod
    def load(file_path: Path, dataset_name: str) -> np.ndarray:
        """Load data from an HDF5 file.

        Args:
            file_path (Path): Path to the HDF5 file.
            dataset_name (str): Name of the dataset to load from the file.

        Returns:
            np.ndarray: Loaded data.

        Raises:
            FileNotFoundError: If the file does not exist.
            KeyError: If the dataset is not found in the file.
            ValueError: If the dataset cannot be converted to a numpy array.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with h5py.File(file_path, 'r') as f:
                if dataset_name not in f:
                    raise KeyError(f"Dataset '{dataset_name}' not found in file: {file_path}")
                # Explicitly cast to numpy array to handle different HDF5 types
                data = np.array(f[dataset_name])
        except Exception as e:
            raise ValueError(f"Failed to load dataset '{dataset_name}' from file '{file_path}': {str(e)}") from e

        return data

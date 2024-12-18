# src/paralisi/io/loaders/numpy_loader.py

import numpy as np
from pathlib import Path

class NumpyLoader:
    """Class for loading NumPy files."""

    @staticmethod
    def load(file_path: Path) -> np.ndarray:
        """Load data from a NumPy file.

        Args:
            file_path (Path): Path to the NumPy file.

        Returns:
            np.ndarray: Loaded data.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return np.load(file_path)

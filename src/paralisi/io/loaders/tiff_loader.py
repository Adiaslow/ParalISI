# src/io/loaders/tiff_loader.py

from pathlib import Path
import tifffile as tiff
import numpy as np

class TiffLoader:
    """Class for loading TIFF files."""

    @staticmethod
    def load(file_path: Path) -> np.ndarray:
        """Load data from a TIFF file.

        Args:
            file_path (Path): Path to the TIFF file.

        Returns:
            np.ndarray: Loaded data.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return tiff.imread(file_path)

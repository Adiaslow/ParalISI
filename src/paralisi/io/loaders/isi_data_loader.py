# src/paralisi/io/loaders/isi_data_loader.py

"""Data loading implementations."""
from pathlib import Path
from typing import Dict, Any, Optional
import h5py
import numpy as np

from numpy.typing import NDArray
from ...core.interfaces.data_loader import DataLoader
from ...core.data.data import RawData
from ...core.exceptions.data_exceptions import DataLoadingError

class ISIDataLoader(DataLoader):
    """Loads intrinsic signal imaging data from HDF5 files."""

    def load(self, path: Path) -> RawData:
        """Load raw imaging data from HDF5 file.

        Args:
            path: Path to HDF5 data file

        Returns:
            RawData object containing imaging data and metadata

        Raises:
            DataLoadingError: If file cannot be loaded or is invalid
        """
        try:
            with h5py.File(path, "r") as f:
                data = np.array(f["imaging_data"], dtype=np.float64)
                return data
        except (OSError, KeyError) as e:
            raise DataLoadingError(f"Failed to load {path}: {str(e)}")

    def supports_format(self, path: Path) -> bool:
        """Check if file format is supported.

        Args:
            path: Path to check

        Returns:
            True if file format is supported, False otherwise
        """
        return path.suffix in {".h5", ".hdf5"}

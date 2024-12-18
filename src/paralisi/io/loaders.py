# src/pyisi/io/loaders.py
"""Data loading implementations."""
from pathlib import Path
from typing import Dict, Any, Optional
import h5py
import numpy as np

from ..core.protocols.loading import DataLoader
from ..core.types.data_types import RawData
from ..core.exceptions import DataLoadingError

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
                data = np.array(f["imaging_data"])
                metadata = dict(f.attrs)
                return RawData(data=data, metadata=metadata)
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

from typing import Dict, Type
from ..interfaces.data_loader import DataLoader
from ...io.loaders.numpy_loader import NumpyLoader
from ...io.loaders.hdf5_loader import HDF5Loader
from ...io.loaders.tiff_loader import TiffLoader

class LoaderFactory:
    """Factory for creating data loaders."""

    _loaders: Dict[str, Type[DataLoader]] = {
        'numpy': NumpyLoader,  # type: ignore
        'hdf5': HDF5Loader,  # type: ignore
        'tiff': TiffLoader  # type: ignore
    }

    @classmethod
    def create(cls, format_type: str, **kwargs) -> DataLoader:
        """Create a loader instance."""
        if format_type not in cls._loaders:
            raise ValueError(f"Unknown format type: {format_type}")

        return cls._loaders[format_type](**kwargs)

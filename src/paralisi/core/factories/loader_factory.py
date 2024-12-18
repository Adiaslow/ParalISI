from typing import Dict, Type
from ..interfaces.data_loader import DataLoader
from ..io.loaders import NumpyLoader, HDF5Loader, TiffLoader

class LoaderFactory:
    """Factory for creating data loaders."""

    _loaders: Dict[str, Type[DataLoader]] = {
        'numpy': NumpyLoader,
        'hdf5': HDF5Loader,
        'tiff': TiffLoader
    }

    @classmethod
    def create(cls, format_type: str, **kwargs) -> DataLoader:
        """Create a loader instance."""
        if format_type not in cls._loaders:
            raise ValueError(f"Unknown format type: {format_type}")

        return cls._loaders[format_type](**kwargs)

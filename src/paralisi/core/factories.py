# src/PyISI/core/factories.py
"""Factories for creating PyISI components."""

from typing import Dict, Type

from .interfaces import DataLoader, DataProcessor, CacheStrategy
from ..processing.processors import (
    BasicProcessor,
    GPUProcessor,
    ParallelProcessor
)
from ..io.loaders import (
    NumpyLoader,
    HDF5Loader,
    TiffLoader
)

class ProcessorFactory:
    """Factory for creating data processors."""

    _processors: Dict[str, Type[DataProcessor]] = {
        'basic': BasicProcessor,
        'gpu': GPUProcessor,
        'parallel': ParallelProcessor
    }

    @classmethod
    def create(cls, processor_type: str, **kwargs) -> DataProcessor:
        """Create a processor instance."""
        if processor_type not in cls._processors:
            raise ValueError(f"Unknown processor type: {processor_type}")

        return cls._processors[processor_type](**kwargs)

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

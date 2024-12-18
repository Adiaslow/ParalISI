# src/paralisi/core/factories/processor_factory.py

from typing import Dict, Type
from ..interfaces.data_processor import DataProcessor
from ..processing.processors import BasicProcessor, GPUProcessor, ParallelProcessor

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

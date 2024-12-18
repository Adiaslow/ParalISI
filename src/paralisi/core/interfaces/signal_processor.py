# src/paralisi/core/interfaces/signal_processor.py
from typing import Protocol
from numpy.typing import NDArray

class SignalProcessor(Protocol):
    """Interface for signal processing operations."""
    def process(self, data: NDArray) -> NDArray:
        ...

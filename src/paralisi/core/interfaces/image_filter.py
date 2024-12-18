# src/paralisi/core/interfaces/image_filter.py
from typing import Protocol
from numpy.typing import NDArray

class ImageFilter(Protocol):
    """Interface for image filtering operations."""
    def apply(self, data: NDArray) -> NDArray:
        ...

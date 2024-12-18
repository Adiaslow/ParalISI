# src/paralisi/core/interfaces/image_registration.py
from typing import Protocol
from numpy.typing import NDArray

class ImageRegistration(Protocol):
    """Interface for image registration operations."""
    def register(self, reference: NDArray, target: NDArray) -> NDArray:
        ...

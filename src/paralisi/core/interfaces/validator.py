# src/paralisi/core/interfaces/validator.py

from typing import Dict, Protocol
from numpy.typing import NDArray

class Validator(Protocol):
    """Protocol for data validators"""

    def validate(self, data: NDArray, metadata: Dict) -> float:
        """Validate the data and return a metric or raise ValidationError if validation fails"""
        ...

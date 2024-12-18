# src/paralisi/core/results/registration_result.py

from dataclasses import dataclass
from numpy.typing import NDArray
from typing import Dict

@dataclass
class RegistrationResult:
    """Container for registration results."""
    transformed_image: NDArray
    transform_params: Dict[str, NDArray]
    convergence_metric: float
    iteration_count: int
    success: bool

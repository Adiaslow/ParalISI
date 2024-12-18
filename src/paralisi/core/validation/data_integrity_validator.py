# src/paralisi/core/validation/data_integrity_validator.py

import numpy as np
from numpy.typing import NDArray
from typing import Dict
from ..interfaces import Validator
from ..exceptions import ValidationError

class DataIntegrityValidator(Validator):
    """Validates data integrity and consistency"""

    def validate(self, data: NDArray, metadata: Dict) -> float:
        expected_frames = metadata.get('frames_expected', 0)
        if expected_frames > 0 and data.shape[0] != expected_frames:
            raise ValidationError(f"Frame count mismatch: {data.shape[0]} vs {expected_frames}")

        if np.any(np.isnan(data)):
            raise ValidationError("Dataset contains NaN values")

        if not np.issubdtype(data.dtype, np.floating):
            raise ValidationError(f"Invalid data type: {data.dtype}")
        return 0.0  # Return a dummy metric for consistency

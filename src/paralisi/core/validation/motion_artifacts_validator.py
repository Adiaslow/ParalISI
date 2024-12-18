# src/paralisi/core/validation/motion_artifacts_validator.py

import numpy as np
from numpy.typing import NDArray
from typing import Dict
from ..interfaces import Validator

class MotionArtifactsValidator(Validator):
    """Detects and quantifies motion artifacts"""

    def validate(self, data: NDArray, metadata: Dict) -> float:
        frame_diff = np.diff(data, axis=0)
        motion_metric = np.mean(np.abs(frame_diff))
        intensity_range = np.max(data) - np.min(data)
        if intensity_range > 0:
            motion_metric /= intensity_range
        return float(motion_metric)

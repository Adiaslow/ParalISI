# src/paralisi/core/validation/photobleaching_validator.py

import numpy as np
from scipy.stats import linregress
from numpy.typing import NDArray
from typing import Dict
from ..interfaces import Validator

class PhotobleachingValidator(Validator):
    """Checks for photobleaching effects"""

    def validate(self, data: NDArray, metadata: Dict) -> float:
        mean_intensity = np.mean(data, axis=(1, 2))
        time_points = np.arange(len(mean_intensity))
        slope, intercept, r_value, p_value, std_err = linregress(time_points, mean_intensity)
        initial_intensity = float(mean_intensity[0])
        if initial_intensity == 0:
            return 0.0
        total_decay = float(slope) * len(mean_intensity) / initial_intensity
        return float(abs(total_decay))

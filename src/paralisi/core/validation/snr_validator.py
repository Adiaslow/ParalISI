# src/paralisi/core/validation/snr_validator.py

import numpy as np
from numpy.typing import NDArray
from typing import Dict
from ..interfaces import Validator

class SNRValidator(Validator):
    """Calculates signal-to-noise ratio"""

    def validate(self, data: NDArray, metadata: Dict) -> float:
        temporal_mean = np.mean(data, axis=0)
        temporal_std = np.std(data, axis=0)
        with np.errstate(divide='ignore', invalid='ignore'):
            snr = np.nanmean(temporal_mean / temporal_std)
        return float(snr)

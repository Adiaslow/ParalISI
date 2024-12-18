# src/paralisi/core/validation/sync_signal_validator.py

import numpy as np
from numpy.typing import NDArray
from typing import Dict
from ..interfaces import Validator

class SyncSignalValidator(Validator):
    """Validates synchronization signal quality"""

    def validate(self, data: NDArray, metadata: Dict) -> float:
        sync_signal = data

        sync_norm = (sync_signal - np.min(sync_signal)) / (np.max(sync_signal) - np.min(sync_signal))
        from scipy.signal import find_peaks
        peaks, properties = find_peaks(sync_norm, height=0.5)

        if len(peaks) < 2:
            return 0.0

        intervals = np.diff(peaks)
        timing_regularity = 1.0 - np.std(intervals) / np.mean(intervals)

        peak_heights = properties['peak_heights']
        amplitude_consistency = 1.0 - np.std(peak_heights) / np.mean(peak_heights)

        return float(np.mean([timing_regularity, amplitude_consistency]))

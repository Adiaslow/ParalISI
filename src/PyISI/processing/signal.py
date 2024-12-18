# src/PyISI/processing/signal.py

import numpy as np
from numpy.typing import NDArray

class SignalProcessor:
    """Core signal processing for ISI data"""

    def normalize_by_baseline(
        self,
        data: NDArray,
        baseline: NDArray,
        divide: bool = True
    ) -> NDArray:
        """Normalize data by baseline

        Parameters
        ----------
        data : NDArray
            Input data to normalize
        baseline : NDArray
            Baseline data
        divide : bool
            If True, divide by baseline after subtraction
        """
        if divide:
            return (data - baseline) / baseline
        return data - baseline

    def average_across_time(
        self,
        data: NDArray,
        start_idx: int,
        end_idx: int
    ) -> NDArray:
        """Average data across specified time window"""
        return np.mean(data[start_idx:end_idx], axis=0)

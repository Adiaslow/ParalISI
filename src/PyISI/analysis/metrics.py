# src/PyISI/analysis/metrics.py

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from numpy.typing import NDArray
from scipy import stats, signal
from ..core.exceptions import AnalysisError

@dataclass
class ResponseMetrics:
    """Container for response quality metrics"""
    snr: float
    reliability: float
    amplitude: float
    latency: float
    variance: float

class MetricsCalculator:
    """Calculates various response and signal quality metrics."""

    def __init__(self, sampling_rate: float):
        self.sampling_rate = sampling_rate

    def compute_response_metrics(
        self,
        signal: NDArray,
        baseline: NDArray,
        stimulus_onset: int
    ) -> ResponseMetrics:
        """Compute comprehensive response metrics.

        Parameters
        ----------
        signal : NDArray
            Response signal
        baseline : NDArray
            Baseline period
        stimulus_onset : int
            Stimulus onset time point

        Returns
        -------
        ResponseMetrics
            Computed metrics
        """
        try:
            # Calculate SNR
            snr = self._calculate_snr(signal, baseline)

            # Calculate response reliability
            reliability = self._calculate_reliability(signal)

            # Calculate response amplitude
            amplitude = self._calculate_amplitude(signal, baseline)

            # Calculate response latency
            latency = self._calculate_latency(signal, stimulus_onset)

            # Calculate response variance
            variance = self._calculate_variance(signal)

            return ResponseMetrics(
                snr=snr,
                reliability=reliability,
                amplitude=amplitude,
                latency=latency,
                variance=variance
            )

        except Exception as e:
            raise AnalysisError(f"Metrics calculation failed: {str(e)}") from e

    def _calculate_snr(
        self,
        signal: NDArray,
        baseline: NDArray
    ) -> float:
        """Calculate signal-to-noise ratio"""
        signal_power = np.mean(np.abs(signal - np.mean(baseline))**2)
        noise_power = np.var(baseline)
        return float(np.sqrt(signal_power / (noise_power + 1e-10)))

    def _calculate_reliability(
        self,
        signal: NDArray,
        window_size: int = 10
    ) -> float:
        """Calculate response reliability across trials"""
        if signal.ndim < 2:
            return 1.0

        # Compute trial-to-trial correlation
        n_trials = signal.shape[0]
        correlations = []

        for i in range(n_trials):
            for j in range(i+1, n_trials):
                corr = stats.pearsonr(signal[i], signal[j])[0]
                correlations.append(corr)

        return float(np.mean(correlations))

    def _calculate_amplitude(
        self,
        signal: NDArray,
        baseline: NDArray
    ) -> float:
        """Calculate response amplitude"""
        baseline_mean = np.mean(baseline)
        peak_amplitude = np.max(np.abs(signal - baseline_mean))
        return float(peak_amplitude)

    def _calculate_latency(
        self,
        signal: NDArray,
        stimulus_onset: int
    ) -> float:
        """Calculate response latency"""
        baseline_std = np.std(signal[:stimulus_onset])
        threshold = 2 * baseline_std

        # Find first crossing of threshold
        crossings = np.where(np.abs(signal[stimulus_onset:]) > threshold)[0]
        if len(crossings) > 0:
            latency = crossings[0] / self.sampling_rate
        else:
            latency = float('nan')

        return float(latency)

    def _calculate_variance(
        self,
        signal: NDArray
    ) -> float:
        """Calculate response variance"""
        return float(np.var(signal))

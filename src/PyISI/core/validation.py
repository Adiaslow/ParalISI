# src/PyISI/core/validation.py

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from numpy.typing import NDArray
import torch
from pathlib import Path
from ..core.exceptions import ValidationError
from ..utils.decorators import validate_input

class DataQualityMetric(Enum):
    """Common data quality metrics"""
    SNR = "signal_to_noise"
    MOTION = "motion_artifact"
    SYNC_QUALITY = "sync_quality"
    BLEACHING = "photobleaching"
    CONTRAST = "contrast"

@dataclass
class ValidationResult:
    """Container for validation results"""
    passed: bool
    metrics: Dict[str, float]
    issues: List[str]
    recommendations: List[str]

class DataValidator:
    """Validates experimental data quality and integrity.

    Implements comprehensive checks for ISI data quality including motion artifacts,
    signal quality, synchronization issues, and data integrity.

    Parameters
    ----------
    threshold_snr : float, optional
        Minimum required SNR, by default 2.0
    max_motion : float, optional
        Maximum allowed motion (pixels), by default 1.0
    min_sync_quality : float, optional
        Minimum sync signal quality, by default 0.8
    """

    def __init__(
        self,
        threshold_snr: float = 2.0,
        max_motion: float = 1.0,
        min_sync_quality: float = 0.8
    ):
        self.threshold_snr = threshold_snr
        self.max_motion = max_motion
        self.min_sync_quality = min_sync_quality

    def validate_experiment(
        self,
        data: NDArray,
        sync_signal: NDArray,
        metadata: Dict
    ) -> ValidationResult:
        """Validate complete experimental dataset.

        Parameters
        ----------
        data : NDArray
            Raw imaging data (time, height, width)
        sync_signal : NDArray
            Synchronization signal
        metadata : Dict
            Experiment metadata

        Returns
        -------
        ValidationResult
            Validation results and recommendations
        """
        try:
            issues = []
            recommendations = []
            metrics = {}

            # Check data integrity
            self._validate_data_integrity(data, metadata)

            # Check sync signal
            sync_quality = self._validate_sync_signal(sync_signal)
            metrics['sync_quality'] = sync_quality
            if sync_quality < self.min_sync_quality:
                issues.append(f"Poor sync signal quality: {sync_quality:.2f}")
                recommendations.append("Check stimulus timing and sync connections")

            # Check for motion artifacts
            motion_metric = self._detect_motion_artifacts(data)
            metrics['motion'] = motion_metric
            if motion_metric > self.max_motion:
                issues.append(f"Excessive motion detected: {motion_metric:.2f} pixels")
                recommendations.append("Consider motion correction or data exclusion")

            # Calculate SNR
            snr = self._calculate_snr(data)
            metrics['snr'] = snr
            if snr < self.threshold_snr:
                issues.append(f"Low SNR: {snr:.2f}")
                recommendations.append("Check imaging parameters and focus")

            # Check for photobleaching
            bleaching_metric = self._check_photobleaching(data)
            metrics['bleaching'] = bleaching_metric
            if bleaching_metric > 0.2:  # 20% signal decay
                issues.append(f"Significant photobleaching detected: {bleaching_metric:.1%}")
                recommendations.append("Reduce light intensity or exposure time")

            return ValidationResult(
                passed=len(issues) == 0,
                metrics=metrics,
                issues=issues,
                recommendations=recommendations
            )

        except Exception as e:
            raise ValidationError(f"Data validation failed: {str(e)}") from e

    def _validate_data_integrity(
        self,
        data: NDArray,
        metadata: Dict
    ) -> None:
        """Check data integrity and consistency"""
        # Check data dimensions
        expected_frames = metadata.get('frames_expected', 0)
        if expected_frames > 0 and data.shape[0] != expected_frames:
            raise ValidationError(f"Frame count mismatch: {data.shape[0]} vs {expected_frames}")

        # Check for missing data
        if np.any(np.isnan(data)):
            raise ValidationError("Dataset contains NaN values")

        # Check data type and range
        if not np.issubdtype(data.dtype, np.floating):
            raise ValidationError(f"Invalid data type: {data.dtype}")

    def _validate_sync_signal(
        self,
        sync_signal: NDArray
    ) -> float:
        """Validate synchronization signal quality"""
        # Normalize signal
        sync_norm = (sync_signal - np.min(sync_signal)) / (np.max(sync_signal) - np.min(sync_signal))

        # Find peaks
        from scipy.signal import find_peaks
        peaks, properties = find_peaks(sync_norm, height=0.5)

        if len(peaks) < 2:
            return 0.0

        # Calculate timing regularity
        intervals = np.diff(peaks)
        timing_regularity = 1.0 - np.std(intervals) / np.mean(intervals)

        # Calculate amplitude consistency
        peak_heights = properties['peak_heights']
        amplitude_consistency = 1.0 - np.std(peak_heights) / np.mean(peak_heights)

        return np.mean([timing_regularity, amplitude_consistency])

    def _detect_motion_artifacts(
        self,
        data: NDArray
    ) -> float:
        """Detect and quantify motion artifacts"""
        # Compute frame-to-frame difference
        frame_diff = np.diff(data, axis=0)

        # Calculate motion metric (mean absolute frame difference)
        motion_metric = np.mean(np.abs(frame_diff))

        # Normalize by image intensity range
        intensity_range = np.max(data) - np.min(data)
        if intensity_range > 0:
            motion_metric /= intensity_range

        return motion_metric

    def _calculate_snr(
        self,
        data: NDArray
    ) -> float:
        """Calculate signal-to-noise ratio"""
        # Compute temporal mean and std
        temporal_mean = np.mean(data, axis=0)
        temporal_std = np.std(data, axis=0)

        # Calculate SNR
        with np.errstate(divide='ignore', invalid='ignore'):
            snr = np.nanmean(temporal_mean / temporal_std)

        return float(snr)

    def _check_photobleaching(
        self,
        data: NDArray
    ) -> float:
        """Check for photobleaching effects"""
        # Calculate mean intensity over time
        mean_intensity = np.mean(data, axis=(1, 2))

        # Fit linear trend
        time_points = np.arange(len(mean_intensity))
        from scipy.stats import linregress
        slope, _, _, _, _ = linregress(time_points, mean_intensity)

        # Calculate relative signal decay
        total_decay = (slope * len(mean_intensity)) / mean_intensity[0]

        return abs(total_decay)

class BatchValidator:
    """Validates multiple experiments for consistency"""

    def __init__(self, validator: DataValidator):
        self.validator = validator

    def validate_batch(
        self,
        data_paths: List[Path],
        group_metadata: Optional[Dict] = None
    ) -> Dict[str, ValidationResult]:
        """Validate multiple experiments"""
        results = {}

        for path in data_paths:
            try:
                # Load data (implement data loading logic)
                data = self._load_data(path)
                sync = self._load_sync(path)
                metadata = self._load_metadata(path)

                # Update metadata with group info
                if group_metadata:
                    metadata.update(group_metadata)

                # Validate individual experiment
                result = self.validator.validate_experiment(data, sync, metadata)
                results[str(path)] = result

            except Exception as e:
                results[str(path)] = ValidationResult(
                    passed=False,
                    metrics={},
                    issues=[f"Validation failed: {str(e)}"],
                    recommendations=["Check data files and format"]
                )

        return results

# Example usage:
if __name__ == "__main__":
    # Create validator
    validator = DataValidator(
        threshold_snr=2.0,
        max_motion=1.0,
        min_sync_quality=0.8
    )

    # Load example data
    data = np.load("sample_data.npy")
    sync = np.load("sample_sync.npy")
    metadata = {
        "frames_expected": 1000,
        "framerate": 30.0,
        "pixel_size": 10.0
    }

    # Validate data
    result = validator.validate_experiment(data, sync, metadata)

    # Print results
    print(f"Validation {'passed' if result.passed else 'failed'}")
    print("\nMetrics:")
    for name, value in result.metrics.items():
        print(f"{name}: {value:.3f}")

    if result.issues:
        print("\nIssues found:")
        for issue in result.issues:
            print(f"- {issue}")

        print("\nRecommendations:")
        for rec in result.recommendations:
            print(f"- {rec}")

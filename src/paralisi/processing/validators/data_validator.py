# src/paralisi/core/validation/data_validator.py

from typing import Dict, List
from numpy.typing import NDArray
from ...types.data_quality_metric import DataQualityMetric
from ...results.validation_result import ValidationResult
from ...exceptions import ValidationError
from ...processing.validators.data_integrity_validator import validate_data_integrity
from ...processing.validators.sync_signal_validator import validate_sync_signal
from ...processing.validators.motion_artifacts_validator import detect_motion_artifacts
from ...processing.validators.snr_calculator import calculate_snr
from ...processing.validators.photobleaching_checker import check_photobleaching

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
            validate_data_integrity(data, metadata)

            # Check sync signal
            sync_quality = validate_sync_signal(sync_signal)
            metrics['sync_quality'] = sync_quality
            if sync_quality < self.min_sync_quality:
                issues.append(f"Poor sync signal quality: {sync_quality:.2f}")
                recommendations.append("Check stimulus timing and sync connections")

            # Check for motion artifacts
            motion_metric = detect_motion_artifacts(data)
            metrics['motion'] = motion_metric
            if motion_metric > self.max_motion:
                issues.append(f"Excessive motion detected: {motion_metric:.2f} pixels")
                recommendations.append("Consider motion correction or data exclusion")

            # Calculate SNR
            snr = calculate_snr(data)
            metrics['snr'] = snr
            if snr < self.threshold_snr:
                issues.append(f"Low SNR: {snr:.2f}")
                recommendations.append("Check imaging parameters and focus")

            # Check for photobleaching
            bleaching_metric = check_photobleaching(data)
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

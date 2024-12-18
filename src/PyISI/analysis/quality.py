# src/PyISI/analysis/quality.py

from enum import Enum
from typing import Dict, List, Optional
import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass
from scipy import stats

from ..core.exceptions import QualityError

class QualityLevel(Enum):
    """Data quality levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"

@dataclass
class QualityMetrics:
    """Container for quality assessment metrics"""
    motion_score: float
    noise_level: float
    signal_quality: float
    artifact_score: float
    overall_quality: QualityLevel

class QualityAnalyzer:
    """Analyzes data quality and detects artifacts."""

    def __init__(
        self,
        motion_threshold: float = 1.0,
        noise_threshold: float = 0.5,
        artifact_threshold: float = 0.3
    ):
        self.motion_threshold = motion_threshold
        self.noise_threshold = noise_threshold
        self.artifact_threshold = artifact_threshold

    def assess_quality(
        self,
        data: NDArray,
        mask: Optional[NDArray] = None
    ) -> QualityMetrics:
        """Assess data quality comprehensively.

        Parameters
        ----------
        data : NDArray
            Input data to assess
        mask : Optional[NDArray]
            Optional mask for ROI

        Returns
        -------
        QualityMetrics
            Quality assessment results
        """
        try:
            # Apply mask if provided
            if mask is not None:
                data = data * mask

            # Calculate motion score
            motion_score = self._detect_motion(data)

            # Calculate noise level
            noise_level = self._calculate_noise(data)

            # Assess signal quality
            signal_quality = self._assess_signal(data)

            # Detect artifacts
            artifact_score = self._detect_artifacts(data)

            # Determine overall quality
            overall_quality = self._determine_quality(
                motion_score,
                noise_level,
                signal_quality,
                artifact_score
            )

            return QualityMetrics(
                motion_score=motion_score,
                noise_level=noise_level,
                signal_quality=signal_quality,
                artifact_score=artifact_score,
                overall_quality=overall_quality
            )

        except Exception as e:
            raise QualityError(f"Quality assessment failed: {str(e)}") from e

    def _detect_motion(self, data: NDArray) -> float:
        """Detect and quantify motion artifacts"""
        if data.ndim < 3:
            return 0.0

        frame_diff = np.diff(data, axis=0)
        motion_metric = np.mean(np.abs(frame_diff))
        return float(motion_metric)

    def _calculate_noise(self, data: NDArray) -> float:
        """Calculate noise level"""
        if data.ndim < 2:
            return float(np.std(data))

        temporal_noise = np.std(data, axis=0)
        return float(np.mean(temporal_noise))

    def _assess_signal(self, data: NDArray) -> float:
        """Assess signal quality"""
        if data.ndim < 2:
            return 0.0

        # Calculate temporal SNR
        temporal_mean = np.mean(data, axis=0)
        temporal_std = np.std(data, axis=0)
        tsnr = np.mean(temporal_mean) / (np.mean(temporal_std) + 1e-10)
        return float(tsnr)

    def _detect_artifacts(self, data: NDArray) -> float:
        """Detect artifacts in the data"""
        # Z-score the data
        z_scored = stats.zscore(data, axis=None)

        # Count extreme values
        artifact_ratio = np.mean(np.abs(z_scored) > 3.0)
        return float(artifact_ratio)

    def _determine_quality(
        self,
        motion: float,
        noise: float,
        signal: float,
        artifacts: float
    ) -> QualityLevel:
        """Determine overall quality level"""
        # Compute quality score
        score = (
            (1.0 - motion/self.motion_threshold) * 0.3 +
            (1.0 - noise/self.noise_threshold) * 0.3 +
            (signal / 10.0) * 0.2 +
            (1.0 - artifacts/self.artifact_threshold) * 0.2
        )

        # Map to quality levels
        if score > 0.8:
            return QualityLevel.EXCELLENT
        elif score > 0.6:
            return QualityLevel.GOOD
        elif score > 0.4:
            return QualityLevel.FAIR
        else:
            return QualityLevel.POOR

# src/PyISI/analysis/orientation.py

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from typing import Dict, Optional
from scipy import ndimage
from ..core.exceptions import ProcessingError
from ..utils.decorators import validate_input

@dataclass
class OrientationAnalysisResult:
    """Container for detailed orientation analysis results"""
    magnitude: NDArray
    orientation: NDArray
    selectivity: NDArray
    uniformity: NDArray  # Local orientation uniformity
    gradient: NDArray    # Orientation gradient magnitude
    pinwheel_centers: Optional[NDArray] = None  # Coordinates of pinwheel centers
    domain_size: Optional[float] = None         # Average orientation domain size

class OrientationAnalyzer:
    """Advanced analysis of orientation maps including pinwheel detection,
    gradient analysis, and domain size estimation.

    Extends the basic orientation analysis with additional metrics and
    features useful for characterizing orientation maps.
    """

    def __init__(
        self,
        smoothing_sigma: float = 1.0,
        min_magnitude: float = 0.1,
        pinwheel_threshold: float = 0.5,
        gradient_sigma: float = 2.0
    ):
        """
        Parameters
        ----------
        smoothing_sigma : float
            Gaussian smoothing sigma for map processing
        min_magnitude : float
            Minimum magnitude threshold for valid orientation values
        pinwheel_threshold : float
            Threshold for pinwheel center detection
        gradient_sigma : float
            Sigma for gradient calculation smoothing
        """
        self.smoothing_sigma = smoothing_sigma
        self.min_magnitude = min_magnitude
        self.pinwheel_threshold = pinwheel_threshold
        self.gradient_sigma = gradient_sigma

    @validate_input
    def analyze_orientation_map(
        self,
        magnitude: NDArray,
        orientation: NDArray,
        mask: Optional[NDArray] = None
    ) -> OrientationAnalysisResult:
        """Perform comprehensive orientation map analysis.

        Parameters
        ----------
        magnitude : NDArray
            Orientation selectivity magnitude map
        orientation : NDArray
            Preferred orientation map (in radians)
        mask : Optional[NDArray]
            Binary mask defining valid regions for analysis

        Returns
        -------
        OrientationAnalysisResult
            Complete analysis results
        """
        try:
            if mask is None:
                mask = np.ones_like(magnitude, dtype=bool)

            # Apply magnitude threshold
            valid_mask = mask & (magnitude > self.min_magnitude)

            # Calculate orientation gradient
            gradient = self._compute_orientation_gradient(orientation, valid_mask)

            # Calculate local uniformity
            uniformity = self._compute_local_uniformity(orientation, valid_mask)

            # Detect pinwheel centers
            pinwheel_centers = self._detect_pinwheels(orientation, magnitude, valid_mask)

            # Calculate average domain size
            domain_size = self._estimate_domain_size(orientation, valid_mask)

            return OrientationAnalysisResult(
                magnitude=magnitude,
                orientation=orientation,
                selectivity=magnitude,
                uniformity=uniformity,
                gradient=gradient,
                pinwheel_centers=pinwheel_centers,
                domain_size=domain_size
            )

        except Exception as e:
            raise ProcessingError(f"Orientation analysis failed: {str(e)}") from e

    def _compute_orientation_gradient(
        self,
        orientation: NDArray,
        mask: NDArray
    ) -> NDArray:
        """Compute the orientation gradient magnitude map."""
        # Smooth orientation map for gradient calculation
        smoothed = ndimage.gaussian_filter(orientation, self.gradient_sigma)

        # Calculate gradients using central differences
        dy, dx = np.gradient(smoothed)

        # Compute gradient magnitude
        gradient = np.sqrt(dx**2 + dy**2)

        # Apply mask
        gradient[~mask] = np.nan

        return gradient

    def _compute_local_uniformity(
        self,
        orientation: NDArray,
        mask: NDArray,
        kernel_size: int = 5
    ) -> NDArray:
        """Compute local orientation uniformity."""
        uniformity = np.zeros_like(orientation)

        for i in range(kernel_size//2, orientation.shape[0] - kernel_size//2):
            for j in range(kernel_size//2, orientation.shape[1] - kernel_size//2):
                if mask[i, j]:
                    # Extract local patch
                    patch = orientation[i-kernel_size//2:i+kernel_size//2+1,
                                     j-kernel_size//2:j+kernel_size//2+1]
                    patch_mask = mask[i-kernel_size//2:i+kernel_size//2+1,
                                    j-kernel_size//2:j+kernel_size//2+1]

                    if np.any(patch_mask):
                        # Compute circular variance
                        angles = patch[patch_mask]
                        mean_vector = np.mean(np.exp(2j * angles))
                        uniformity[i, j] = np.abs(mean_vector)

        uniformity[~mask] = np.nan
        return uniformity

    def _detect_pinwheels(
        self,
        orientation: NDArray,
        magnitude: NDArray,
        mask: NDArray
    ) -> NDArray:
        """Detect pinwheel centers using phase singularity detection."""
        # Calculate phase gradients
        dy, dx = np.gradient(orientation)

        # Compute curl
        curl = dx[1:-1, :-1] - dx[1:-1, 1:] - (dy[:-1, 1:-1] - dy[1:, 1:-1])

        # Threshold curl to detect singularities
        pinwheels = np.zeros_like(orientation, dtype=bool)
        pinwheels[1:-1, 1:-1] = np.abs(curl) > self.pinwheel_threshold

        # Apply magnitude threshold and mask
        pinwheels &= mask & (magnitude > self.min_magnitude)

        # Convert to coordinates
        y_coords, x_coords = np.where(pinwheels)
        return np.column_stack([x_coords, y_coords])

    def _estimate_domain_size(
        self,
        orientation: NDArray,
        mask: NDArray
    ) -> float:
        """Estimate average orientation domain size using autocorrelation."""
        # Calculate autocorrelation
        orientation_masked = orientation.copy()
        orientation_masked[~mask] = 0

        ac = ndimage.correlate(orientation_masked, orientation_masked)

        # Find first minimum in radial average
        center = np.array(ac.shape) // 2
        y, x = np.indices(ac.shape)
        r = np.sqrt((x - center[1])**2 + (y - center[0])**2)

        r_unique = np.unique(r.round().astype(int))
        ac_radial = [ac[r == rad].mean() for rad in r_unique]

        # Find first minimum after peak
        peak_idx = np.argmax(ac_radial)
        min_idx = peak_idx + np.argmin(ac_radial[peak_idx:])

        return r_unique[min_idx]

    def get_analysis_summary(
        self,
        result: OrientationAnalysisResult
    ) -> Dict[str, float]:
        """Generate summary statistics from analysis results."""
        return {
            'mean_selectivity': np.nanmean(result.selectivity),
            'median_uniformity': np.nanmedian(result.uniformity),
            'mean_gradient': np.nanmean(result.gradient),
            'pinwheel_density': len(result.pinwheel_centers) / np.sum(~np.isnan(result.selectivity)),
            'domain_size': result.domain_size
        }

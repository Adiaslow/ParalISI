# src/PyISI/analysis/maps.py

import numpy as np
import torch
from numpy.typing import NDArray
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from scipy import ndimage
from ..core.exceptions import ProcessingError
from ..utils.decorators import validate_input

@dataclass
class MapAnalysisResult:
    """Container for map analysis results"""
    magnitude: NDArray
    phase: NDArray
    direction: Optional[NDArray] = None
    orientation: Optional[NDArray] = None
    color_selectivity: Optional[NDArray] = None

class FeatureMapAnalyzer:
    """Analyzes various types of feature maps (orientation, direction, color, etc.)

    Port of GprocessOri.m, GprocessColor.m, GprocessDir.m functionality
    with modern Python implementation.
    """

    def __init__(
        self,
        smoothing_sigma: float = 1.0,
        min_magnitude: float = 0.1
    ):
        self.smoothing_sigma = smoothing_sigma
        self.min_magnitude = min_magnitude

    @validate_input
    def process_orientation_map(
        self,
        responses: NDArray,
        orientations: NDArray
    ) -> MapAnalysisResult:
        """Process orientation-selective responses.

        Parameters
        ----------
        responses : NDArray
            Response matrix (orientations × height × width)
        orientations : NDArray
            Stimulus orientations in degrees

        Returns
        -------
        MapAnalysisResult
            Processed orientation map results
        """
        try:
            # Convert orientations to radians
            theta = np.deg2rad(orientations)

            # Complex sum across orientations
            sum_real = np.sum(responses * np.cos(2 * theta[:, None, None]), axis=0)
            sum_imag = np.sum(responses * np.sin(2 * theta[:, None, None]), axis=0)

            # Calculate magnitude and phase
            magnitude = np.sqrt(sum_real**2 + sum_imag**2)
            phase = np.angle(sum_real + 1j * sum_imag) / 2

            # Apply smoothing
            magnitude = ndimage.gaussian_filter(magnitude, self.smoothing_sigma)
            phase = ndimage.gaussian_filter(phase, self.smoothing_sigma)

            # Mask low magnitude regions
            phase[magnitude < self.min_magnitude] = np.nan

            return MapAnalysisResult(magnitude=magnitude, phase=phase)

        except Exception as e:
            raise ProcessingError(f"Orientation map processing failed: {str(e)}") from e

    @validate_input
    def process_direction_map(
        self,
        responses: NDArray,
        directions: NDArray
    ) -> MapAnalysisResult:
        """Process direction-selective responses.

        Parameters
        ----------
        responses : NDArray
            Response matrix (directions × height × width)
        directions : NDArray
            Stimulus directions in degrees

        Returns
        -------
        MapAnalysisResult
            Processed direction map results
        """
        try:
            # Convert directions to radians
            theta = np.deg2rad(directions)

            # Complex sum across directions
            sum_real = np.sum(responses * np.cos(theta[:, None, None]), axis=0)
            sum_imag = np.sum(responses * np.sin(theta[:, None, None]), axis=0)

            # Calculate magnitude and direction
            magnitude = np.sqrt(sum_real**2 + sum_imag**2)
            direction = np.angle(sum_real + 1j * sum_imag)

            # Apply smoothing
            magnitude = ndimage.gaussian_filter(magnitude, self.smoothing_sigma)
            direction = ndimage.gaussian_filter(direction, self.smoothing_sigma)

            # Mask low magnitude regions
            direction[magnitude < self.min_magnitude] = np.nan

            return MapAnalysisResult(
                magnitude=magnitude,
                phase=direction,
                direction=direction
            )

        except Exception as e:
            raise ProcessingError(f"Direction map processing failed: {str(e)}") from e

    @validate_input
    def process_color_map(
        self,
        responses: NDArray,
        wavelengths: NDArray
    ) -> MapAnalysisResult:
        """Process color-selective responses.

        Parameters
        ----------
        responses : NDArray
            Response matrix (colors × height × width)
        wavelengths : NDArray
            Stimulus wavelengths in nm

        Returns
        -------
        MapAnalysisResult
            Processed color map results
        """
        try:
            # Normalize responses
            responses_norm = responses / np.max(responses, axis=0, keepdims=True)

            # Calculate color selectivity
            color_sel = np.std(responses_norm, axis=0)

            # Find preferred wavelength
            pref_idx = np.argmax(responses, axis=0)
            pref_wavelength = wavelengths[pref_idx]

            # Apply smoothing
            color_sel = ndimage.gaussian_filter(color_sel, self.smoothing_sigma)
            pref_wavelength = ndimage.gaussian_filter(pref_wavelength, self.smoothing_sigma)

            # Mask low selectivity regions
            pref_wavelength[color_sel < self.min_magnitude] = np.nan

            return MapAnalysisResult(
                magnitude=color_sel,
                phase=pref_wavelength,
                color_selectivity=color_sel
            )

        except Exception as e:
            raise ProcessingError(f"Color map processing failed: {str(e)}") from e

class MapStatistics:
    """Computes statistics and metrics for feature maps"""

    def __init__(self):
        pass

    def compute_selectivity_stats(
        self,
        magnitude: NDArray,
        roi: Optional[NDArray] = None
    ) -> Dict[str, float]:
        """Compute selectivity statistics within ROI"""
        if roi is None:
            roi = np.ones_like(magnitude, dtype=bool)

        valid_data = magnitude[roi & ~np.isnan(magnitude)]

        if len(valid_data) == 0:
            return {
                'mean_selectivity': np.nan,
                'median_selectivity': np.nan,
                'std_selectivity': np.nan,
                'coverage': 0.0
            }

        return {
            'mean_selectivity': np.mean(valid_data),
            'median_selectivity': np.median(valid_data),
            'std_selectivity': np.std(valid_data),
            'coverage': len(valid_data) / np.sum(roi)
        }

    def compute_preference_distribution(
        self,
        phase: NDArray,
        magnitude: NDArray,
        n_bins: int = 36,
        min_magnitude: Optional[float] = None
    ) -> Tuple[NDArray, NDArray]:
        """Compute distribution of preferred features"""
        if min_magnitude is None:
            min_magnitude = np.nanpercentile(magnitude, 25)

        # Mask low magnitude regions
        valid_phase = phase[magnitude > min_magnitude]

        # Convert to degrees and wrap to [0, 180] for orientation
        phase_deg = np.rad2deg(valid_phase) % 180

        # Compute histogram
        hist, bins = np.histogram(phase_deg, bins=n_bins, range=(0, 180))
        bin_centers = (bins[:-1] + bins[1:]) / 2

        return hist, bin_centers

# Example usage:
if __name__ == "__main__":
    # Create analyzer instance
    analyzer = FeatureMapAnalyzer(
        smoothing_sigma=1.0,
        min_magnitude=0.1
    )

    # Example orientation analysis
    orientations = np.array([0, 45, 90, 135])
    responses = np.random.rand(4, 100, 100)  # Example data

    ori_result = analyzer.process_orientation_map(
        responses=responses,
        orientations=orientations
    )

    # Compute statistics
    stats = MapStatistics()
    selectivity_stats = stats.compute_selectivity_stats(ori_result.magnitude)

    print("Map Analysis Results:")
    print(f"Mean selectivity: {selectivity_stats['mean_selectivity']:.3f}")
    print(f"Coverage: {selectivity_stats['coverage']:.1%}")

# src/paralisi/processing/segmentation/sign_map_generator.py

import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import gaussian_filter
import torch

class SignMapGenerator:
    """Handles generation of visual field sign maps from phase maps."""

    def generate_sign_map(self, phase_hor: NDArray, phase_vert: NDArray, smoothing_sigma: float = 1.0) -> NDArray:
        """Create visual field sign map from phase maps."""
        if torch.is_tensor(phase_hor):
            phase_hor = phase_hor.cpu().numpy()
        if torch.is_tensor(phase_vert):
            phase_vert = phase_vert.cpu().numpy()
        phase_hor_smooth = gaussian_filter(phase_hor, smoothing_sigma)
        phase_vert_smooth = gaussian_filter(phase_vert, smoothing_sigma)
        dhdx, dhdy = np.gradient(phase_hor_smooth)
        dvdx, dvdy = np.gradient(phase_vert_smooth)
        gradh = dhdx + 1j * dhdy
        gradv = dvdx + 1j * dvdy
        angle = np.angle(gradh * np.conj(gradv))
        sign_map = np.sign(angle)
        sign_map[np.isnan(phase_hor) | np.isnan(phase_vert)] = np.nan
        return sign_map

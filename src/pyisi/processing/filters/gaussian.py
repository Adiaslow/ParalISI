# src/PyISI/processing/filters/gaussian.py

import numpy as np
from numpy.typing import NDArray
from ...core.interfaces import ImageFilter

class GaussianFilter(ImageFilter):
    """Gaussian filter implementation."""

    def __init__(self, kernel_size: int, sigma: float):
        self.kernel_size = kernel_size
        self.sigma = sigma
        self._kernel = self._create_kernel()

    def apply(self, data: NDArray) -> NDArray:
        """Apply Gaussian filter to data."""
        return np.apply_along_axis(
            lambda x: np.convolve(x, self._kernel, mode='same'),
            0,
            data
        )

    def _create_kernel(self) -> NDArray:
        """Create Gaussian kernel."""
        x = np.linspace(-self.kernel_size/2, self.kernel_size/2, self.kernel_size)
        return np.exp(-x**2/(2*self.sigma**2)) / (self.sigma*np.sqrt(2*np.pi))

# src/PyISI/processing/filters.py

import numpy as np
from enum import Enum
from typing import Optional, Tuple, Union
from dataclasses import dataclass
from scipy import signal, ndimage
import torch
from numpy.typing import NDArray
from ..core.exceptions import ProcessingError

class KernelType(Enum):
    """Types of spatial filter kernels"""
    GAUSSIAN = "gaussian"
    HANN = "hann"
    DISK = "disk"

@dataclass
class FilterConfiguration:
    """Configuration for spatial filter creation"""
    high_pass_params: Optional[Tuple[float, KernelType]] = None  # (width, type)
    low_pass_params: Optional[Tuple[float, KernelType]] = None   # (width, type)
    normalize: bool = True

class SpatialFilter:
    """Creates and applies spatial filters for image processing.

    Implements configurable spatial filtering with support for:
    - High-pass, low-pass, and combined filtering
    - Multiple kernel types (Gaussian, Hann window, disk)
    - Automatic kernel size computation
    - Optional normalization
    """

    def __init__(self, kernel_size: Optional[Tuple[int, int]] = None):
        """
        Parameters
        ----------
        kernel_size : Optional[Tuple[int, int]]
            Fixed kernel size, if not computed from filter width
        """
        self.kernel_size = kernel_size

    def create_kernel(
        self,
        config: FilterConfiguration
    ) -> NDArray:
        """Create spatial filter kernel based on configuration.

        Parameters
        ----------
        config : FilterConfiguration
            Filter specification including component parameters

        Returns
        -------
        NDArray
            2D filter kernel
        """
        try:
            kernel = None

            if config.high_pass_params:
                width, kernel_type = config.high_pass_params
                base_kernel = self._create_base_kernel(width, kernel_type)
                kernel = np.eye(*base_kernel.shape) - base_kernel

            if config.low_pass_params:
                width, kernel_type = config.low_pass_params
                base_kernel = self._create_base_kernel(width, kernel_type)

                if kernel is not None:
                    kernel = signal.convolve2d(kernel, base_kernel, mode='full')
                else:
                    kernel = base_kernel

            if kernel is None:
                raise ProcessingError("Filter configuration must specify at least one component")

            if config.normalize:
                kernel = kernel / np.abs(kernel).sum()

            return kernel

        except Exception as e:
            raise ProcessingError(f"Failed to create filter kernel: {str(e)}") from e

    def _create_base_kernel(
        self,
        width: float,
        kernel_type: KernelType
    ) -> NDArray:
        """Create base filter kernel of specified type."""
        size = self.kernel_size or (int(3 * width), int(3 * width))

        if kernel_type == KernelType.GAUSSIAN:
            return self._create_gaussian(size, width)
        elif kernel_type == KernelType.HANN:
            return self._create_hann(size, width)
        else:  # DISK
            return self._create_disk(size, width)

    def _create_gaussian(
        self,
        size: Tuple[int, int],
        sigma: float
    ) -> NDArray:
        """Create Gaussian filter kernel"""
        y, x = np.ogrid[-size[0]//2:size[0]//2, -size[1]//2:size[1]//2]
        kernel = np.exp(-(x*x + y*y)/(2*sigma*sigma))
        return kernel / kernel.sum()

    def _create_hann(
        self,
        size: Tuple[int, int],
        width: float
    ) -> NDArray:
        """Create 2D Hann window filter"""
        hann_x = signal.hann(int(width))
        hann_y = signal.hann(int(width))
        kernel = np.outer(hann_y, hann_x)
        return kernel / kernel.sum()

    def _create_disk(
        self,
        size: Tuple[int, int],
        radius: float
    ) -> NDArray:
        """Create disk-shaped filter"""
        y, x = np.ogrid[-size[0]//2:size[0]//2, -size[1]//2:size[1]//2]
        disk = x*x + y*y <= radius*radius
        kernel = disk.astype(float)
        return kernel / kernel.sum()

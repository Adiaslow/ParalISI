# src/pyisi/core/config.py
"""Configuration management for ISI experiments.

This module provides configuration classes and utilities for managing
Intrinsic Signal Imaging (ISI) experimental parameters and settings.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

class ProcessingMode(Enum):
    """Enum for different processing modes."""
    CPU = "cpu"
    GPU = "gpu"
    HYBRID = "hybrid"

class FilterType(Enum):
    """Enum for different filter types used in signal processing."""
    GAUSSIAN = "gaussian"
    BUTTERWORTH = "butterworth"
    HANN = "hann"

@dataclass
class AcquisitionConfig:
    """Configuration for data acquisition parameters.

    Attributes:
        sampling_rate: Data acquisition rate in Hz
        frames_per_trial: Number of frames per trial
        image_width: Width of acquired images in pixels
        image_height: Height of acquired images in pixels
        pixel_size: Physical size of each pixel in millimeters
    """
    sampling_rate: float
    frames_per_trial: int
    image_width: int
    image_height: int
    pixel_size: float

    def __post_init__(self) -> None:
        """Validate acquisition parameters."""
        if self.sampling_rate <= 0:
            raise ValueError("Sampling rate must be positive")
        if self.frames_per_trial <= 0:
            raise ValueError("Frames per trial must be positive")
        if self.image_width <= 0 or self.image_height <= 0:
            raise ValueError("Image dimensions must be positive")
        if self.pixel_size <= 0:
            raise ValueError("Pixel size must be positive")

@dataclass
class ProcessingConfig:
    """Configuration for data processing parameters.

    Attributes:
        mode: Processing mode (CPU/GPU/HYBRID)
        filter_type: Type of filter to use for signal processing
        filter_kernel_size: Size of the filter kernel
        high_pass_cutoff: High-pass filter cutoff frequency
        low_pass_cutoff: Low-pass filter cutoff frequency
        parallel_workers: Number of parallel workers for processing
    """
    mode: ProcessingMode = ProcessingMode.CPU
    filter_type: FilterType = FilterType.GAUSSIAN
    filter_kernel_size: int = 5
    high_pass_cutoff: Optional[float] = None
    low_pass_cutoff: Optional[float] = None
    parallel_workers: int = 1

    def __post_init__(self) -> None:
        """Validate processing parameters."""
        if self.filter_kernel_size % 2 == 0:
            raise ValueError("Filter kernel size must be odd")
        if self.parallel_workers < 1:
            raise ValueError("Number of parallel workers must be positive")
        if (self.high_pass_cutoff is not None and
            self.low_pass_cutoff is not None and
            self.high_pass_cutoff >= self.low_pass_cutoff):
            raise ValueError("High-pass cutoff must be lower than low-pass cutoff")

@dataclass
class ExperimentConfig:
    """Main configuration class for ISI experiments.

    Attributes:
        name: Name of the experiment
        data_path: Path to raw data files
        output_path: Path for processed outputs
        acquisition: Acquisition configuration
        processing: Processing configuration
        metadata: Additional experiment metadata
    """
    name: str
    data_path: Path
    output_path: Path
    acquisition: AcquisitionConfig
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and process configuration after initialization."""
        # Convert string paths to Path objects
        if isinstance(self.data_path, str):
            self.data_path = Path(self.data_path)
        if isinstance(self.output_path, str):
            self.output_path = Path(self.output_path)

        # Validate paths
        if not self.data_path.exists():
            raise ValueError(f"Data path does not exist: {self.data_path}")
        self.output_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> 'ExperimentConfig':
        """Create configuration from YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            ExperimentConfig instance

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ValueError: If configuration is invalid
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path) as f:
            config_dict = yaml.safe_load(f)

        # Convert nested dictionaries to appropriate dataclasses
        acq_config = AcquisitionConfig(**config_dict.pop('acquisition'))
        proc_config = ProcessingConfig(**config_dict.pop('processing'))

        return cls(
            acquisition=acq_config,
            processing=proc_config,
            **config_dict
        )

    def save(self, path: Union[str, Path]) -> None:
        """Save configuration to YAML file.

        Args:
            path: Path to save configuration file
        """
        path = Path(path)

        # Convert to dictionary, handling nested dataclasses
        config_dict = {
            'name': self.name,
            'data_path': str(self.data_path),
            'output_path': str(self.output_path),
            'acquisition': {
                k: v for k, v in vars(self.acquisition).items()
            },
            'processing': {
                k: v if not isinstance(v, Enum) else v.value
                for k, v in vars(self.processing).items()
            },
            'metadata': self.metadata
        }

        with open(path, 'w') as f:
            yaml.safe_dump(config_dict, f, default_flow_style=False)

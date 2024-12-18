# src/pyisi/core/types/config_types.py
"""Configuration type definitions."""
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

class ProcessingMode(Enum):
    """Processing mode options."""
    CPU = auto()
    GPU = auto()
    HYBRID = auto()

    def __str__(self) -> str:
        return self.name.lower()

class StorageFormat(Enum):
    """Data storage format options."""
    NUMPY = auto()
    HDF5 = auto()
    TIFF = auto()

    def __str__(self) -> str:
        return self.name.lower()

@dataclass(frozen=True)
class ProcessingConfig:
    """Processing configuration."""
    mode: ProcessingMode
    parallel_workers: int = field(default=1)
    gpu_device: Optional[int] = field(default=None)

    def __post_init__(self) -> None:
        if self.parallel_workers < 1:
            raise ValueError("parallel_workers must be >= 1")
        if self.mode == ProcessingMode.GPU and self.gpu_device is None:
            raise ValueError("GPU mode requires gpu_device to be specified")

@dataclass(frozen=True)
class StorageConfig:
    """Storage configuration."""
    format: StorageFormat
    compression: bool = field(default=False)
    base_path: Path = field(default_factory=lambda: Path.cwd())

    def __post_init__(self) -> None:
        if not self.base_path.exists():
            raise ValueError(f"Base path does not exist: {self.base_path}")

@dataclass(frozen=True)
class ExperimentConfig:
    """Configuration settings for an ISI experiment."""
    animal_id: str
    session_id: str
    stimulus_repeats: int
    sampling_rate: float
    pixels_per_mm: float
    wavelength: float
    stimulus_period: float
    date: str
    experimenter: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.stimulus_repeats < 1:
            raise ValueError("stimulus_repeats must be >= 1")
        if self.sampling_rate <= 0:
            raise ValueError("sampling_rate must be > 0")
        if self.pixels_per_mm <= 0:
            raise ValueError("pixels_per_mm must be > 0")
        if self.wavelength <= 0:
            raise ValueError("wavelength must be > 0")
        if self.stimulus_period <= 0:
            raise ValueError("stimulus_period must be > 0")
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError("date must be in YYYY-MM-DD format") from e

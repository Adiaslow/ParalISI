# pyisi/core/types/experiment.py
from dataclasses import dataclass
from typing import Optional

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

@dataclass(frozen=True)
class ProcessingParameters:
    """Parameters for signal processing."""
    lowpass_cutoff: float = 0.1
    highpass_cutoff: float = 30.0
    spatial_sigma: float = 2.0
    temporal_sigma: float = 1.0
    baseline_window: tuple[float, float] = (0.0, 1.0)
    response_window: tuple[float, float] = (1.0, 5.0)

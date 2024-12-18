# src/paralisi/core/configurations/acquisition_config.py

from dataclasses import dataclass

@dataclass
class AcquisitionConfig:
    sampling_rate: float
    frames_per_trial: int
    image_width: int
    image_height: int
    pixel_size: float

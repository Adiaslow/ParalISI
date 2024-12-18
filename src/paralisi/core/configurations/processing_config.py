# src/paralisi/core/configurations/processing_config.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class ProcessingConfig:
    mode: str = "cpu"
    filter_type: str = "gaussian"
    filter_kernel_size: int = 5
    high_pass_cutoff: Optional[float] = None
    low_pass_cutoff: Optional[float] = None
    parallel_workers: int = 1

# src/paralisi/core/configurations/filter_config.py
from typing import Optional, Tuple
from dataclasses import dataclass
from ..types import KernelType

@dataclass
class FilterConfiguration:
    """Configuration for spatial filter creation."""
    high_pass_params: Optional[Tuple[float, KernelType]] = None  # (width, type)
    low_pass_params: Optional[Tuple[float, KernelType]] = None   # (width, type)
    normalize: bool = True

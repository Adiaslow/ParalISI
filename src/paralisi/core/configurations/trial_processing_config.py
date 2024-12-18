# src/paralisis/core/configurations/trial_processing_config.py

from typing import Tuple
from dataclasses import dataclass

@dataclass
class TrialProcessingConfig:
    """Configuration for trial processing"""
    time_window: Tuple[int, int]  # Analysis time window
    baseline_window: Tuple[int, int]  # Baseline time window
    normalize: bool = True  # Whether to normalize by baseline
    split_trials: bool = True  # Whether to split odd/even trials
    compute_variance: bool = False  # Whether to compute trial variance

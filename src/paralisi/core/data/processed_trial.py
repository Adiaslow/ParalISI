# src/paralisi/core/data/processed_trial.py

from dataclasses import dataclass
from typing import Dict
from .masks import MaskData
from .data import ProcessedData
from .trial_metadata import TrialMetadata

@dataclass(frozen=True)
class ProcessedTrial:
    """Immutable container for processed trial data."""
    processed_data: ProcessedData
    masks: Dict[str, MaskData]
    metadata: TrialMetadata

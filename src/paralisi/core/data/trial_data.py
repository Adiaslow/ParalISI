# src/paralisi/core/data/trial_data.py

from dataclasses import dataclass
from .data import RawData
from .trial_metadata import TrialMetadata

@dataclass(frozen=True)
class TrialData:
    """Immutable container for trial data."""
    raw_data: RawData
    metadata: TrialMetadata

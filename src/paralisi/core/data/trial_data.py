# src/paralisi/core/data/trial_data.py

from dataclasses import dataclass
from .data import RawData
from .trial_metadata import TrialMetadata

@dataclass(frozen=True)
class TrialData:
    """Immutable container for trial data.

    Attributes:
        raw_data (RawData): The raw data of the trial.
        metadata (TrialMetadata): Metadata associated with the trial data.
    """
    raw_data: RawData
    metadata: TrialMetadata

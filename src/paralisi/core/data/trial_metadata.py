# src/paralisi/core/data/trial_metadata.py

from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class TrialMetadata:
    """Immutable container for trial metadata."""
    trial_id: int
    condition: str
    parameters: Dict[str, Any]

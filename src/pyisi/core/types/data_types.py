# src/PyISI/core/types/data_types.py
"""Core data type definitions."""

from dataclasses import dataclass
from typing import Dict, Any
import numpy as np
from numpy.typing import NDArray

RawData = NDArray[np.float64]
ProcessedData = NDArray[np.float64]
MaskData = NDArray[np.bool_]

@dataclass(frozen=True)
class TrialMetadata:
    """Immutable container for trial metadata."""
    trial_id: int
    condition: str
    parameters: Dict[str, Any]

@dataclass(frozen=True)
class TrialData:
    """Immutable container for trial data."""
    raw_data: RawData
    metadata: TrialMetadata

@dataclass(frozen=True)
class ProcessedTrial:
    """Immutable container for processed trial data."""
    processed_data: ProcessedData
    masks: Dict[str, MaskData]
    metadata: TrialMetadata

# src/paralisi/core/data/analyzer_data.py

"""Container for analyzer file data"""

from dataclasses import dataclass
from typing import Dict, Any
import numpy as np

@dataclass
class AnalyzerData:
    """Container for analyzer file data"""
    animal_id: str
    experiment_id: str
    params: Dict[str, Any]
    metadata: Dict[str, Any]
    conditions: Dict[str, Any]
    timestamps: np.ndarray

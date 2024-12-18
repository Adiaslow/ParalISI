# src/paralisi/core/interfaces/writer.py

from pathlib import Path
from typing import Dict, Any, Optional, Protocol
import numpy as np

class DataWriter(Protocol):
    """Interface for data writers."""

    def save_processed_data(
        self,
        data: Dict[str, np.ndarray],
        metadata: Dict[str, Any],
        animal_id: str,
        experiment_id: str,
        format: str = 'hdf5'
    ) -> Path:
        """Save processed experimental data."""
        ...

    def save_params(
        self,
        params: Dict[str, Any],
        identifier: str,
        description: Optional[str] = None
    ) -> Path:
        """Save parameters to JSON file."""
        ...

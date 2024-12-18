# src/paralisi/core/interfaces/writer.py
#
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np

class IDataWriter(ABC):
    """Interface for data writers."""

    @abstractmethod
    def save_processed_data(
        self,
        data: Dict[str, np.ndarray],
        metadata: Dict[str, Any],
        animal_id: str,
        experiment_id: str,
        format: str = 'hdf5'
    ) -> Path:
        """Save processed experimental data."""
        pass

    @abstractmethod
    def save_params(
        self,
        params: Dict[str, Any],
        identifier: str,
        description: Optional[str] = None
    ) -> Path:
        """Save parameters to JSON file."""
        pass

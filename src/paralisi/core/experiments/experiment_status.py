# src/paralisi/core/experiments/experiment_status.py

from enum import Enum, auto

class ExperimentStatus(Enum):
    """Status tracking for experiment processing."""
    INITIALIZED = auto()
    LOADING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()

    def __str__(self) -> str:
        return self.name.lower()

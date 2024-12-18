# src/paralisi/core/managers/data_manager.py

from pathlib import Path
from typing import Optional, Dict
import logging
from ..interfaces.data_loader import DataLoader
from ..data import TrialData, TrialMetadata
from ..exceptions import DataLoadingError

logger = logging.getLogger(__name__)

class DataManager:
    """Manages loading and storing trial data."""

    def __init__(self, data_loader: DataLoader, base_path: Path):
        """Initialize data manager.

        Args:
            data_loader: Data loading interface
            base_path: Base path for data files

        Raises:
            ValueError: If arguments are invalid
        """
        if not base_path.exists():
            raise ValueError(f"Base path does not exist: {base_path}")

        self.data_loader = data_loader
        self.base_path = base_path
        self._trial_data: Dict[int, TrialData] = {}

        logger.info(f"Initialized DataManager with base_path={base_path}")

    def load_trial(self, trial_id: int, force_reload: bool = False) -> Optional[TrialData]:
        """Load trial data, optionally forcing reload from disk.

        Args:
            trial_id: ID of trial to load
            force_reload: Whether to force data reload

        Returns:
            Loaded trial data if successful, None otherwise

        Raises:
            DataLoadingError: If data loading fails
        """
        if not force_reload and trial_id in self._trial_data:
            return self._trial_data[trial_id]

        trial_path = self.base_path / f"trial_{trial_id}.npy"
        try:
            raw_data = self.data_loader.load(trial_path)
            trial_metadata = self._load_metadata(trial_id)
            trial_data = TrialData(raw_data=raw_data, metadata=trial_metadata)
            self._trial_data[trial_id] = trial_data
            logger.info(f"Successfully loaded trial {trial_id}")
            return trial_data

        except Exception as e:
            logger.error(f"Error loading trial {trial_id}: {str(e)}")
            raise DataLoadingError(f"Failed to load trial {trial_id}") from e

    def _load_metadata(self, trial_id: int) -> TrialMetadata:
        """Load metadata for a specific trial.

        Args:
            trial_id: ID of trial to load metadata for

        Returns:
            Loaded trial metadata
        """
        # Implement metadata loading logic here
        return TrialMetadata(
            trial_id=trial_id,
            condition="",  # Set appropriate condition
            parameters={}  # Set appropriate parameters
        )

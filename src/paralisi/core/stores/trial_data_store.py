# src/paralisi/core/stores/trial_data_store.py

from pathlib import Path
from typing import Optional
from ..interfaces.data_loader import DataLoader
from ..interfaces.cache_strategy import CacheStrategy
from ..data.trial_data import TrialData
from ..data.trial_metadata import TrialMetadata

class TrialDataStore:
    """Manages trial data storage and retrieval."""

    def __init__(self, loader: DataLoader, cache: CacheStrategy[TrialData]):
        self.loader = loader
        self.cache = cache

    def get_trial(self, trial_id: int, path: Path, force_reload: bool = False) -> Optional[TrialData]:
        """Get trial data, using cache if available."""
        cache_key = f"{path}:{trial_id}"

        if not force_reload:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached

        if not self.loader.supports_format(path):
            raise ValueError(f"Unsupported data format: {path}")

        raw_data = self.loader.load(path)
        metadata = TrialMetadata(
            trial_id=trial_id,
            condition="",  # Set appropriate condition
            parameters={}  # Set appropriate parameters
        )

        trial_data = TrialData(raw_data=raw_data, metadata=metadata)
        self.cache.put(cache_key, trial_data)

        return trial_data

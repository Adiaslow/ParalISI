# src/paralisi/core/stores/metadata_store.py

import json
from pathlib import Path
from typing import Dict, Any
from ..types.data_types import TrialMetadata

class MetadataStore:
    """Manages trial metadata storage and retrieval."""

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def get_metadata(self, trial_id: int) -> TrialMetadata:
        """Retrieve metadata for a specific trial."""
        # Implement metadata loading logic here
        # For example, loading from a JSON file
        metadata_path = self.base_path / f"trial_{trial_id}_metadata.json"
        with open(metadata_path) as f:
            metadata = json.load(f)

        return TrialMetadata(
            trial_id=trial_id,
            condition=metadata.get("condition", ""),
            parameters=metadata.get("parameters", {})
        )

    def save_metadata(self, trial_id: int, metadata: Dict[str, Any]) -> None:
        """Save metadata for a specific trial."""
        metadata_path = self.base_path / f"trial_{trial_id}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)

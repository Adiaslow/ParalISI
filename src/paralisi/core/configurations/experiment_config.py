# src/paralisi/core/configurations/experiment_config.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional
from .acquisition_config import AcquisitionConfig
from .processing_config import ProcessingConfig

@dataclass
class ExperimentConfig:
    name: str
    data_path: Path
    output_path: Path
    acquisition: AcquisitionConfig
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.data_path, str):
            self.data_path = Path(self.data_path)
        if isinstance(self.output_path, str):
            self.output_path = Path(self.output_path)
        if not self.data_path.exists():
            raise ValueError(f"Data path does not exist: {self.data_path}")

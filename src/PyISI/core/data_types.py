# src/PyISI/core/data_types.py

@dataclass
class ExperimentMetadata:
    """Experiment configuration and metadata"""
    animal_id: str
    session_date: datetime
    parameters: Dict[str, Any]

class ISIDataset:
    """Main data container with lazy loading"""

    def __init__(self,
                 data_path: Path,
                 metadata: ExperimentMetadata):
        self.data_path = data_path
        self.metadata = metadata
        self._cache = {}

    def get_trial_data(self,
                      trial_idx: int,
                      force_reload: bool = False) -> NDArray:
        """Cached trial data access"""
        ...

# src/paralisi/core/managers/experiment_manager.py

from pathlib import Path
from typing import Optional, List, Dict
import logging
from concurrent.futures import ThreadPoolExecutor
from ..interfaces.data_processor import DataProcessor
from ..data import ProcessedTrial, TrialData
from ..stores import TrialDataStore
from ..exceptions import ProcessingError

logger = logging.getLogger(__name__)

class ExperimentManager:
    """Coordinates experiment components with improved error handling and logging."""

    def __init__(
        self,
        data_store: TrialDataStore,
        processor: DataProcessor,
        base_path: Path,
        max_workers: int = 1
    ):
        """Initialize experiment manager.

        Args:
            data_store: Data storage interface
            processor: Data processing interface
            base_path: Base path for experiment data
            max_workers: Maximum number of parallel workers

        Raises:
            ValueError: If arguments are invalid
        """
        if not base_path.exists():
            raise ValueError(f"Base path does not exist: {base_path}")
        if max_workers < 1:
            raise ValueError("max_workers must be >= 1")

        self.data_store = data_store
        self.processor = processor
        self.base_path = base_path
        self.max_workers = max_workers
        self._processed_trials: Dict[int, ProcessedTrial] = {}

        logger.info(f"Initialized ExperimentManager with base_path={base_path}")

    def process_trial(
        self,
        trial_id: int,
        force_reload: bool = False
    ) -> Optional[ProcessedTrial]:
        """Process a single trial with improved error handling.

        Args:
            trial_id: ID of trial to process
            force_reload: Whether to force data reload

        Returns:
            Processed trial data if successful, None if trial not found

        Raises:
            ProcessingError: If processing fails
            DataLoadingError: If data loading fails
        """
        logger.debug(f"Processing trial {trial_id}")

        try:
            # Get trial data
            trial_path = self.base_path / f"trial_{trial_id}.npy"
            trial_data = self.data_store.get_trial(trial_id, trial_path, force_reload)

            if trial_data is None:
                logger.warning(f"Trial {trial_id} not found")
                return None

            # Validate and process
            if not self.processor.validate(trial_data.raw_data):
                raise ProcessingError(f"Invalid data for trial {trial_id}")

            processed_data = self.processor.process(trial_data.raw_data)
            processed_trial = ProcessedTrial(
                processed_data=processed_data,
                masks=self._generate_masks(processed_data),
                metadata=trial_data.metadata
            )

            self._processed_trials[trial_id] = processed_trial
            logger.info(f"Successfully processed trial {trial_id}")
            return processed_trial

        except Exception as e:
            logger.error(f"Error processing trial {trial_id}: {str(e)}")
            raise ProcessingError(f"Failed to process trial {trial_id}") from e

    def process_trials(
        self,
        trial_ids: List[int],
        parallel: bool = False
    ) -> Dict[int, ProcessedTrial]:
        """Process multiple trials, optionally in parallel.

        Args:
            trial_ids: List of trial IDs to process
            parallel: Whether to process in parallel

        Returns:
            Dictionary mapping trial IDs to processed trials
        """
        if parallel and self.max_workers > 1:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    trial_id: executor.submit(self.process_trial, trial_id)
                    for trial_id in trial_ids
                }
                return {
                    trial_id: future.result()
                    for trial_id, future in futures.items()
                    if future.result() is not None
                }
        else:
            return {
                trial_id: processed
                for trial_id in trial_ids
                if (processed := self.process_trial(trial_id)) is not None
            }

    def _generate_masks(self, processed_data: TrialData) -> Dict[str, Any]:
        """Generate masks for processed data.

        To be implemented based on specific masking requirements.
        """
        return {}  # Implement specific masking logic

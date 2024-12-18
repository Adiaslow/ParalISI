# src/PyISI/processing/trial_processor.py

import numpy as np
from numpy.typing import NDArray
from typing import Dict, List, Tuple
from ..core.configurations.trial_processing_config import TrialProcessingConfig
from ..core.exceptions import ProcessingError

class ConditionProcessor:
    """Processes trial data grouped by experimental conditions"""

    def __init__(self, image_size: Tuple[int, int]):
        self.image_size = image_size

    def process_condition_data(
        self,
        trials: List[NDArray],
        config: TrialProcessingConfig
    ) -> Dict[str, NDArray]:
        """Process all trials for a condition.

        Parameters
        ----------
        trials : List[NDArray]
            List of trial data arrays
        config : TrialProcessingConfig
            Processing configuration

        Returns
        -------
        Dict[str, NDArray]
            Processed data including means and optional variance
        """
        try:
            # Split trials if requested
            if config.split_trials:
                odd_trials = trials[::2]
                even_trials = trials[1::2]

                odd_mean = self._process_trial_set(odd_trials, config)
                even_mean = self._process_trial_set(even_trials, config)

                result = {
                    'odd_mean': odd_mean,
                    'even_mean': even_mean
                }

                # Compute variance if requested
                if config.compute_variance:
                    odd_var = self._compute_trial_variance(odd_trials, odd_mean, config)
                    even_var = self._compute_trial_variance(even_trials, even_mean, config)
                    result.update({
                        'odd_variance': odd_var,
                        'even_variance': even_var
                    })
            else:
                # Process all trials together
                mean = self._process_trial_set(trials, config)
                result = {'mean': mean}

                if config.compute_variance:
                    variance = self._compute_trial_variance(trials, mean, config)
                    result['variance'] = variance

            return result

        except Exception as e:
            raise ProcessingError(f"Condition processing failed: {str(e)}") from e

    def _process_trial_set(
        self,
        trials: List[NDArray],
        config: TrialProcessingConfig
    ) -> NDArray:
        """Process a set of trials and compute their mean."""

        processed_trials = []
        for trial in trials:
            # Extract time windows
            trial_data = trial[slice(*config.time_window)]
            baseline = trial[slice(*config.baseline_window)]

            # Compute baseline
            baseline_mean = np.mean(baseline, axis=0)

            # Apply baseline correction
            if config.normalize:
                processed = (trial_data - baseline_mean) / baseline_mean
            else:
                processed = trial_data - baseline_mean

            processed_trials.append(processed)

        return np.mean(processed_trials, axis=0)

    def _compute_trial_variance(
        self,
        trials: List[NDArray],
        mean: NDArray,
        config: TrialProcessingConfig
    ) -> NDArray:
        """Compute variance across trials relative to mean."""

        squared_diff_sum = np.zeros(self.image_size)
        n_trials = len(trials)

        for trial in trials:
            # Extract analysis window
            trial_data = trial[slice(*config.time_window)]

            # Apply baseline correction if needed
            if config.normalize:
                baseline = np.mean(trial[slice(*config.baseline_window)], axis=0)
                trial_data = (trial_data - baseline) / baseline

            # Add squared difference from mean
            squared_diff_sum += (trial_data - mean) ** 2

        return squared_diff_sum / n_trials

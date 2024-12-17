# src/PyISI/io/readers.py

from pathlib import Path
import h5py
import numpy as np
import json
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from ..core.exceptions import IOError

@dataclass
class AnalyzerData:
    """Container for analyzer file data"""
    animal_id: str
    experiment_id: str
    params: Dict[str, Any]
    metadata: Dict[str, Any]
    conditions: Dict[str, Any]
    timestamps: np.ndarray

class AnalyzerReader:
    """Reads and parses analyzer files.

    This class handles loading and parsing of analyzer files, providing a Python
    interface to the MATLAB analyzer format.

    Parameters
    ----------
    base_path : Union[str, Path]
        Base path for data files
    """

    def __init__(self, base_path: Union[str, Path]):
        self.base_path = Path(base_path)

    def load_analyzer(
        self,
        animal_id: str,
        experiment_id: str
    ) -> AnalyzerData:
        """Load analyzer file for given animal and experiment.

        Parameters
        ----------
        animal_id : str
            Animal identifier
        experiment_id : str
            Experiment identifier

        Returns
        -------
        AnalyzerData
            Parsed analyzer data

        Raises
        ------
        IOError
            If file cannot be loaded or parsed
        """
        try:
            # Construct file path
            file_name = f"{animal_id}_{experiment_id}.analyzer"
            file_path = self.base_path / file_name

            if not file_path.exists():
                raise FileNotFoundError(f"Analyzer file not found: {file_path}")

            # Load MATLAB file
            with h5py.File(file_path, 'r') as f:
                # Extract core data
                params = self._load_params(f)
                metadata = self._load_metadata(f)
                conditions = self._load_conditions(f)
                timestamps = self._load_timestamps(f)

            return AnalyzerData(
                animal_id=animal_id,
                experiment_id=experiment_id,
                params=params,
                metadata=metadata,
                conditions=conditions,
                timestamps=timestamps
            )

        except Exception as e:
            raise IOError(f"Failed to load analyzer file: {str(e)}") from e

    def _load_params(self, f: h5py.File) -> Dict[str, Any]:
        """Load experimental parameters"""
        params = {}
        param_group = f.get('Analyzer/P', None)
        if param_group is not None:
            for key in param_group.keys():
                params[key] = param_group[key][()]
        return params

    def _load_metadata(self, f: h5py.File) -> Dict[str, Any]:
        """Load experiment metadata"""
        metadata = {}
        meta_group = f.get('Analyzer/M', None)
        if meta_group is not None:
            for key in meta_group.keys():
                metadata[key] = meta_group[key][()]
        return metadata

    def _load_conditions(self, f: h5py.File) -> Dict[str, Any]:
        """Load experimental conditions"""
        conditions = {}
        cond_group = f.get('Analyzer/loops/conds', None)
        if cond_group is not None:
            for i in range(len(cond_group)):
                cond_data = cond_group[f'{i}'][()]
                conditions[f'condition_{i}'] = cond_data
        return conditions

    def _load_timestamps(self, f: h5py.File) -> np.ndarray:
        """Load timing information"""
        time_data = f.get('Analyzer/timeStamps', None)
        if time_data is not None:
            return np.array(time_data)
        return np.array([])

class ExperimentReader:
    """Reads experimental data and parameters.

    This class provides functionality for loading experimental parameters
    and data files.
    """

    def __init__(self, data_path: Union[str, Path]):
        self.data_path = Path(data_path)

    def load_params(
        self,
        unit: str,
        experiment: str,
        param_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """Load experimental parameters.

        Parameters
        ----------
        unit : str
            Unit identifier
        experiment : str
            Experiment identifier
        param_file : Optional[str]
            Override default parameter file name

        Returns
        -------
        Dict[str, Any]
            Parameter dictionary
        """
        try:
            # Default parameter file name if not specified
            if param_file is None:
                param_file = f"{unit}_{experiment}_params.json"

            file_path = self.data_path / param_file

            if not file_path.exists():
                raise FileNotFoundError(f"Parameter file not found: {file_path}")

            # Load and parse parameters
            with open(file_path, 'r') as f:
                params = json.load(f)

            return params

        except Exception as e:
            raise IOError(f"Failed to load parameters: {str(e)}") from e

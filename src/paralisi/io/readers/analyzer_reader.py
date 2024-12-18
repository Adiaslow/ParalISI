# src/paralisi/io/readers/analyzer_reader.py

"""Analyzer file reader."""

from pathlib import Path
import h5py
import numpy as np
from typing import Dict, Any, Union, Optional
from ...core.exceptions.io_exceptions import IOError
from ...core.data.analyzer_data import AnalyzerData

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
        if isinstance(param_group, h5py.Group):
            for key in param_group.keys():
                param_dataset = param_group.get(key)
                if isinstance(param_dataset, h5py.Dataset):
                    params[key] = param_dataset[()]
        return params

    def _load_metadata(self, f: h5py.File) -> Dict[str, Any]:
        """Load experiment metadata"""
        metadata = {}
        meta_group = f.get('Analyzer/M', None)
        if isinstance(meta_group, h5py.Group):
            for key in meta_group.keys():
                meta_dataset = meta_group.get(key)
                if isinstance(meta_dataset, h5py.Dataset):
                    metadata[key] = meta_dataset[()]
        return metadata

    def _load_conditions(self, f: h5py.File) -> Dict[str, Any]:
        """Load experimental conditions"""
        conditions = {}
        cond_group = f.get('Analyzer/loops/conds', None)
        if isinstance(cond_group, h5py.Group):
            for i in range(len(cond_group)):
                cond_data = cond_group.get(f'{i}')
                if isinstance(cond_data, h5py.Dataset):
                    conditions[f'condition_{i}'] = cond_data[()]
        return conditions

    def _load_timestamps(self, f: h5py.File) -> np.ndarray:
        """Load timing information"""
        time_data = f.get('Analyzer/timeStamps', None)
        if time_data is not None and isinstance(time_data, h5py.Dataset):
            return np.array(time_data)
        return np.array([])

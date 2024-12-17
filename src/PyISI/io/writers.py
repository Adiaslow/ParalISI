# src/PyISI/io/writers.py

import numpy as np
import h5py
import json
from pathlib import Path
from typing import Dict, Any, Union, Optional
from datetime import datetime
from ..core.exceptions import IOError

class DataWriter:
    """Handles data export and saving.

    This class provides methods for saving processed data, parameters,
    and results in various formats.

    Parameters
    ----------
    output_path : Union[str, Path]
        Base path for output files
    """

    def __init__(self, output_path: Union[str, Path]):
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def save_processed_data(
        self,
        data: Dict[str, np.ndarray],
        metadata: Dict[str, Any],
        animal_id: str,
        experiment_id: str,
        format: str = 'hdf5'
    ) -> Path:
        """Save processed experimental data.

        Parameters
        ----------
        data : Dict[str, np.ndarray]
            Dictionary of data arrays to save
        metadata : Dict[str, Any]
            Metadata to include with saved data
        animal_id : str
            Animal identifier
        experiment_id : str
            Experiment identifier
        format : str, optional
            Output format ('hdf5' or 'npz'), by default 'hdf5'

        Returns
        -------
        Path
            Path to saved file
        """
        try:
            # Create output filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{animal_id}_{experiment_id}_{timestamp}"

            if format == 'hdf5':
                return self._save_hdf5(filename, data, metadata)
            else:
                return self._save_npz(filename, data, metadata)

        except Exception as e:
            raise IOError(f"Failed to save data: {str(e)}") from e

    def _save_hdf5(
        self,
        filename: str,
        data: Dict[str, np.ndarray],
        metadata: Dict[str, Any]
    ) -> Path:
        """Save data in HDF5 format"""
        file_path = self.output_path / f"{filename}.h5"

        with h5py.File(file_path, 'w') as f:
            # Save data arrays
            data_group = f.create_group('data')
            for key, array in data.items():
                data_group.create_dataset(key, data=array)

            # Save metadata
            meta_group = f.create_group('metadata')
            for key, value in metadata.items():
                if isinstance(value, (list, dict)):
                    meta_group.create_dataset(
                        key,
                        data=np.void(json.dumps(value).encode())
                    )
                else:
                    meta_group.create_dataset(key, data=value)

        return file_path

    def _save_npz(
        self,
        filename: str,
        data: Dict[str, np.ndarray],
        metadata: Dict[str, Any]
    ) -> Path:
        """Save data in NPZ format"""
        file_path = self.output_path / f"{filename}.npz"

        # Combine data and metadata
        save_dict = {
            **data,
            'metadata': np.array(json.dumps(metadata).encode())
        }

        np.savez_compressed(file_path, **save_dict)
        return file_path

    def save_params(
        self,
        params: Dict[str, Any],
        identifier: str,
        description: Optional[str] = None
    ) -> Path:
        """Save parameters to JSON file"""
        file_path = self.output_path / f"{identifier}_params.json"

        # Add metadata
        params['_metadata'] = {
            'saved_at': datetime.now().isoformat(),
            'description': description
        }

        with open(file_path, 'w') as f:
            json.dump(params, f, indent=2)

        return file_path

# Example usage
if __name__ == "__main__":
    # Initialize readers
    analyzer_reader = AnalyzerReader("/path/to/analyzer/files")
    experiment_reader = ExperimentReader("/path/to/data/files")

    # Load analyzer data
    analyzer_data = analyzer_reader.load_analyzer("animal_1", "exp_001")

    # Load parameters
    params = experiment_reader.load_params("unit_1", "exp_001")

    # Initialize writer
    writer = DataWriter("/path/to/output")

    # Save some processed data
    processed_data = {
        'array1': np.random.randn(100, 100),
        'array2': np.random.randn(50, 50)
    }
    metadata = {
        'processing_date': datetime.now().isoformat(),
        'parameters': params
    }

    # Save in HDF5 format
    output_path = writer.save_processed_data(
        processed_data,
        metadata,
        "animal_1",
        "exp_001",
        format='hdf5'
    )
    print(f"Data saved to: {output_path}")

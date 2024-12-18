import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, Union, Optional
from datetime import datetime
from ...core.exceptions.io_exceptions import IOError
from ...core.interfaces.data_writer import IDataWriter
from ...io.savers.hdf5_saver import HDF5Saver
from ...io.savers.npz_saver import NPZSaver

class DataWriter(IDataWriter):
    """Handles data export and saving.

    This class provides methods for saving processed data, parameters,
    and results in various formats.

    Parameters
    ----------
    output_path : Union[str, Path]
        Base path for output files
    """

    def __init__(self, output_path: Union[str, Path], saver: Optional[Union[HDF5Saver, NPZSaver]] = None):
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.saver = saver or HDF5Saver()

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
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{animal_id}_{experiment_id}_{timestamp}"

            if format == 'hdf5':
                self.saver = HDF5Saver()
            else:
                self.saver = NPZSaver()

            return self.saver.save(filename, data, metadata, self.output_path)

        except Exception as e:
            raise IOError(f"Failed to save data: {str(e)}") from e  # Use custom exception

    def save_params(
        self,
        params: Dict[str, Any],
        identifier: str,
        description: Optional[str] = None
    ) -> Path:
        """Save parameters to JSON file"""
        file_path = self.output_path / f"{identifier}_params.json"

        params['_metadata'] = {
            'saved_at': datetime.now().isoformat(),
            'description': description
        }

        with open(file_path, 'w') as f:
            json.dump(params, f, indent=2)

        return file_path

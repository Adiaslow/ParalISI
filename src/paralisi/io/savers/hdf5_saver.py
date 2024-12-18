# src/paralisi/io/savers/hdf5_saver.py

"""Module for saving data in HDF5 format."""

import h5py
import json
from pathlib import Path
from typing import Dict, Any
import numpy as np

class HDF5Saver:
    """Saves data in HDF5 format."""

    def save(self, filename: str, data: Dict[str, np.ndarray], metadata: Dict[str, Any], output_path: Path) -> Path:
        file_path = output_path / f"{filename}.h5"
        with h5py.File(file_path, 'w') as f:
            data_group = f.create_group('data')
            for key, array in data.items():
                data_group.create_dataset(key, data=array)

            meta_group = f.create_group('metadata')
            for key, value in metadata.items():
                if isinstance(value, (list, dict)):
                    meta_group.create_dataset(key, data=np.void(json.dumps(value).encode()))
                else:
                    meta_group.create_dataset(key, data=value)

        return file_path

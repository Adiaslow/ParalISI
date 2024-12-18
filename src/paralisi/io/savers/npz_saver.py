# src/paralisi/io/savers/npz_saver.py

import json
from pathlib import Path
from typing import Dict, Any
import numpy as np

class NPZSaver:
    """Saves data in NPZ format."""

    def save(self, filename: str, data: Dict[str, np.ndarray], metadata: Dict[str, Any], output_path: Path) -> Path:
        file_path = output_path / f"{filename}.npz"
        save_dict = {**data, 'metadata': np.array(json.dumps(metadata).encode())}
        np.savez_compressed(file_path, **save_dict)
        return file_path

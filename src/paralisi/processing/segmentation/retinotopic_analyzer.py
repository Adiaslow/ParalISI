# src/paralisi/processing/segmentation/retinotopic_analyzer.py

import numpy as np
from numpy.typing import NDArray
from typing import Dict
import torch
from ...core.exceptions.processing_exceptions import ProcessingError
from ...core.interfaces.retinotopic_mapper import RetinotopicMapper
from .phase_map_computer import PhaseMapComputer
from .sign_map_generator import SignMapGenerator

class RetinotopicAnalyzer(RetinotopicMapper):
    """Performs comprehensive retinotopic analysis."""

    def __init__(self, cuda_enabled: bool = True, precision: str = 'float32'):
        self.phase_map_computer = PhaseMapComputer(cuda_enabled, precision)
        self.sign_map_generator = SignMapGenerator()

    def analyze_retinotopy(self, horizontal_responses: NDArray, vertical_responses: NDArray) -> Dict[str, NDArray]:
        """Perform complete retinotopic analysis."""
        try:
            h_resp = torch.from_numpy(horizontal_responses).to(self.phase_map_computer.device)
            v_resp = torch.from_numpy(vertical_responses).to(self.phase_map_computer.device)
            h_phase, h_mag, h_snr = self.phase_map_computer.compute_phase_maps(h_resp)
            v_phase, v_mag, v_snr = self.phase_map_computer.compute_phase_maps(v_resp)
            sign_map = self.sign_map_generator.generate_sign_map(h_phase.cpu().numpy(), v_phase.cpu().numpy())
            return {
                'phase_horizontal': h_phase.cpu().numpy(),
                'phase_vertical': v_phase.cpu().numpy(),
                'magnitude_horizontal': h_mag.cpu().numpy(),
                'magnitude_vertical': v_mag.cpu().numpy(),
                'snr_horizontal': h_snr.cpu().numpy(),
                'snr_vertical': v_snr.cpu().numpy(),
                'sign_map': sign_map
            }
        except Exception as e:
            raise ProcessingError(f"Retinotopic analysis failed: {str(e)}") from e

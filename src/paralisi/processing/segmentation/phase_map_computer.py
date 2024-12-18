# src/paralisi/processing/segmentation/phase_map_computer.py

import torch
from numpy.typing import NDArray
from typing import Tuple
from ...utils.decorators import validate_input, requires_cuda

class PhaseMapComputer:
    """Handles computation of phase maps using Fourier-based analysis."""

    def __init__(self, cuda_enabled: bool = True, precision: str = 'float32'):
        self.device = torch.device('cuda' if cuda_enabled and torch.cuda.is_available() else 'cpu')
        self.dtype = getattr(torch, precision)
        self._setup_filters()

    def _setup_filters(self) -> None:
        """Initialize signal processing filters."""
        self.hamming = torch.hamming_window(
            window_length=256,
            periodic=True,
            dtype=self.dtype,
            device=self.device
        )

    @torch.jit.script
    def compute_phase_maps(self, responses: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Compute phase maps from periodic responses using FFT."""
        responses = responses.to(device=self.device, dtype=self.dtype)
        responses = responses * self.hamming.view(-1, 1, 1)
        fft_result = torch.fft.rfft(responses, dim=0)
        stim_freq_idx = self._find_stimulus_frequency(fft_result)
        phase = torch.angle(fft_result[stim_freq_idx])
        magnitude = torch.abs(fft_result[stim_freq_idx])
        noise_floor = torch.median(torch.abs(fft_result), dim=0).values
        snr = magnitude / noise_floor
        snr_threshold = 2.0
        phase_masked = torch.where(snr > snr_threshold, phase, torch.nan)
        return phase_masked, magnitude, snr

    def _find_stimulus_frequency(self, fft_result: torch.Tensor) -> int:
            """Find the stimulus frequency component in FFT result."""
            power_spectrum = torch.mean(torch.abs(fft_result) ** 2, dim=(1, 2))
            peak_idx = torch.argmax(power_spectrum[1:]) + 1
            return int(peak_idx.item())

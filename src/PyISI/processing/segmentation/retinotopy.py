# src/PyISI/processing/segmentation/retinotopy.py

import numpy as np
import torch
import torch.fft
from numpy.typing import NDArray
from typing import Tuple, Optional, Dict
from dataclasses import dataclass
from scipy.ndimage import gaussian_filter
from ...core.exceptions import ProcessingError
from ...utils.decorators import validate_input, requires_cuda

@dataclass
class PhaseMapResults:
    """Container for phase map computation results"""
    phase_horizontal: torch.Tensor
    phase_vertical: torch.Tensor
    magnitude_horizontal: torch.Tensor
    magnitude_vertical: torch.Tensor
    snr_horizontal: torch.Tensor
    snr_vertical: torch.Tensor

class RetinotopicMapper:
    """Handles retinotopic map computation and analysis.

    This class implements Fourier-based analysis of periodic visual stimulation
    responses to generate retinotopic maps and compute visual field sign maps.

    Parameters
    ----------
    cuda_enabled : bool, optional
        Whether to use GPU acceleration, by default True
    precision : str, optional
        Numerical precision ('float32' or 'float64'), by default 'float32'
    """

    def __init__(
        self,
        cuda_enabled: bool = True,
        precision: str = 'float32'
    ):
        self.device = torch.device('cuda' if cuda_enabled and torch.cuda.is_available() else 'cpu')
        self.dtype = getattr(torch, precision)
        self._setup_filters()

    def _setup_filters(self) -> None:
        """Initialize signal processing filters"""
        # Hamming window for temporal filtering
        self.hamming = torch.hamming_window(
            window_length=256,  # Adjustable based on typical data length
            periodic=True,
            dtype=self.dtype,
            device=self.device
        )

    @torch.jit.script
    def compute_phase_maps(
        self,
        responses: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute phase maps from periodic responses using FFT.

        Parameters
        ----------
        responses : torch.Tensor
            Response time series of shape (time, height, width)

        Returns
        -------
        Tuple[torch.Tensor, torch.Tensor]
            Horizontal and vertical phase maps
        """
        # Ensure input is on correct device and type
        responses = responses.to(device=self.device, dtype=self.dtype)

        # Apply temporal filtering
        responses = responses * self.hamming.view(-1, 1, 1)

        # Compute FFT
        fft_result = torch.fft.rfft(responses, dim=0)

        # Find stimulus frequency component
        stim_freq_idx = self._find_stimulus_frequency(fft_result)

        # Extract phase and magnitude at stimulus frequency
        phase = torch.angle(fft_result[stim_freq_idx])
        magnitude = torch.abs(fft_result[stim_freq_idx])

        # Calculate SNR
        noise_floor = torch.median(torch.abs(fft_result), dim=0).values
        snr = magnitude / noise_floor

        # Create masked phase maps
        snr_threshold = 2.0  # Adjustable threshold
        phase_masked = torch.where(snr > snr_threshold, phase, torch.nan)

        return phase_masked, magnitude, snr

    def _find_stimulus_frequency(
        self,
        fft_result: torch.Tensor
    ) -> int:
        """Find the stimulus frequency component in FFT result"""
        # Average power across spatial dimensions
        power_spectrum = torch.mean(torch.abs(fft_result) ** 2, dim=(1, 2))

        # Find peak frequency excluding DC
        peak_idx = torch.argmax(power_spectrum[1:]) + 1

        return peak_idx

    def generate_sign_map(
        self,
        phase_hor: NDArray,
        phase_vert: NDArray,
        smoothing_sigma: float = 1.0
    ) -> NDArray:
        """Create visual field sign map from phase maps.

        Parameters
        ----------
        phase_hor : NDArray
            Horizontal phase map
        phase_vert : NDArray
            Vertical phase map
        smoothing_sigma : float, optional
            Gaussian smoothing sigma, by default 1.0

        Returns
        -------
        NDArray
            Visual field sign map (-1 or 1)
        """
        # Convert to numpy if needed
        if torch.is_tensor(phase_hor):
            phase_hor = phase_hor.cpu().numpy()
        if torch.is_tensor(phase_vert):
            phase_vert = phase_vert.cpu().numpy()

        # Apply smoothing
        phase_hor_smooth = gaussian_filter(phase_hor, smoothing_sigma)
        phase_vert_smooth = gaussian_filter(phase_vert, smoothing_sigma)

        # Compute gradients
        dhdx, dhdy = np.gradient(phase_hor_smooth)
        dvdx, dvdy = np.gradient(phase_vert_smooth)

        # Calculate visual field sign
        gradh = dhdx + 1j * dhdy
        gradv = dvdx + 1j * dvdy

        # Compute angle between gradients
        angle = np.angle(gradh * np.conj(gradv))

        # Convert to sign map
        sign_map = np.sign(angle)

        # Mask out low SNR regions
        sign_map[np.isnan(phase_hor) | np.isnan(phase_vert)] = np.nan

        return sign_map

    def analyze_retinotopy(
        self,
        horizontal_responses: NDArray,
        vertical_responses: NDArray
    ) -> Dict[str, NDArray]:
        """Perform complete retinotopic analysis.

        Parameters
        ----------
        horizontal_responses : NDArray
            Responses to horizontal stimulus
        vertical_responses : NDArray
            Responses to vertical stimulus

        Returns
        -------
        Dict[str, NDArray]
            Dictionary containing computed maps and metrics
        """
        try:
            # Convert inputs to tensors
            h_resp = torch.from_numpy(horizontal_responses).to(self.device)
            v_resp = torch.from_numpy(vertical_responses).to(self.device)

            # Compute phase maps
            h_phase, h_mag, h_snr = self.compute_phase_maps(h_resp)
            v_phase, v_mag, v_snr = self.compute_phase_maps(v_resp)

            # Generate sign map
            sign_map = self.generate_sign_map(h_phase.cpu().numpy(),
                                            v_phase.cpu().numpy())

            # Return results
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

# Example usage:
if __name__ == "__main__":
    # Create mapper instance
    mapper = RetinotopicMapper(cuda_enabled=True)

    # Load example data
    hor_data = np.load("sample_horizontal_responses.npy")
    vert_data = np.load("sample_vertical_responses.npy")

    # Run analysis
    results = mapper.analyze_retinotopy(hor_data, vert_data)

    # Print summary
    print("Analysis complete:")
    print(f"Mean horizontal SNR: {np.nanmean(results['snr_horizontal']):.2f}")
    print(f"Mean vertical SNR: {np.nanmean(results['snr_vertical']):.2f}")

# src/PyISI/processing/registration.py

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Callable
import numpy as np
import torch
import torch.nn.functional as F
from numpy.typing import NDArray
from ..core.exceptions import RegistrationError
from ..utils.decorators import validate_input, requires_cuda

class RegistrationMethod(Enum):
    """Supported registration methods"""
    RIGID = "rigid"
    AFFINE = "affine"
    ELASTIC = "elastic"

@dataclass
class RegistrationResult:
    """Container for registration results"""
    transformed_image: NDArray
    transform_params: Dict[str, NDArray]
    convergence_metric: float
    iteration_count: int
    success: bool

class ImageRegistration:
    """Handles image registration and alignment.

    This class implements various registration methods for aligning images,
    with support for different transformation types and optimization strategies.

    Parameters
    ----------
    method : RegistrationMethod
        Registration method to use
    cuda_enabled : bool, optional
        Whether to use GPU acceleration, by default True
    precision : str, optional
        Numerical precision ('float32' or 'float64'), by default 'float32'
    """

    def __init__(
        self,
        method: RegistrationMethod = RegistrationMethod.RIGID,
        cuda_enabled: bool = True,
        precision: str = 'float32'
    ):
        self.method = method
        self.device = torch.device('cuda' if cuda_enabled and torch.cuda.is_available() else 'cpu')
        self.dtype = getattr(torch, precision)
        self._setup_optimizer()

    def _setup_optimizer(self) -> None:
        """Initialize optimization parameters"""
        self.max_iterations = 1000
        self.convergence_threshold = 1e-6
        self.learning_rate = 0.1

    @validate_input
    def register_images(
        self,
        source: NDArray,
        target: NDArray,
        initial_transform: Optional[Dict[str, NDArray]] = None,
        mask: Optional[NDArray] = None,
        progress_callback: Optional[Callable[[int, float], None]] = None
    ) -> RegistrationResult:
        """Register source image to target image.

        Parameters
        ----------
        source : NDArray
            Source image to be transformed
        target : NDArray
            Target image to align with
        initial_transform : Optional[Dict[str, NDArray]], optional
            Initial transformation parameters
        mask : Optional[NDArray], optional
            Mask for weighted registration
        progress_callback : Optional[Callable[[int, float], None]], optional
            Callback for reporting progress

        Returns
        -------
        RegistrationResult
            Registration results including transformed image
        """
        try:
            # Convert inputs to tensors
            source_tensor = torch.from_numpy(source).to(device=self.device, dtype=self.dtype)
            target_tensor = torch.from_numpy(target).to(device=self.device, dtype=self.dtype)

            if mask is not None:
                mask_tensor = torch.from_numpy(mask).to(device=self.device, dtype=self.dtype)
            else:
                mask_tensor = None

            # Initialize transform parameters
            params = self._initialize_transform(initial_transform)

            # Optimize transformation
            result = self._optimize_transform(
                source_tensor,
                target_tensor,
                params,
                mask_tensor,
                progress_callback
            )

            return result

        except Exception as e:
            raise RegistrationError(f"Registration failed: {str(e)}") from e

    def _initialize_transform(
        self,
        initial_transform: Optional[Dict[str, NDArray]]
    ) -> Dict[str, torch.Tensor]:
        """Initialize transformation parameters"""
        if initial_transform is None:
            if self.method == RegistrationMethod.RIGID:
                return {
                    'rotation': torch.tensor(0.0, device=self.device, dtype=self.dtype),
                    'translation': torch.zeros(2, device=self.device, dtype=self.dtype)
                }
            elif self.method == RegistrationMethod.AFFINE:
                return {
                    'matrix': torch.eye(3, device=self.device, dtype=self.dtype)
                }
            else:  # Elastic
                return {
                    'displacement': torch.zeros((2, *source.shape), device=self.device, dtype=self.dtype)
                }
        else:
            return {k: torch.tensor(v, device=self.device, dtype=self.dtype)
                    for k, v in initial_transform.items()}

    def _optimize_transform(
        self,
        source: torch.Tensor,
        target: torch.Tensor,
        params: Dict[str, torch.Tensor],
        mask: Optional[torch.Tensor],
        progress_callback: Optional[Callable[[int, float], None]]
    ) -> RegistrationResult:
        """Optimize transformation parameters"""
        # Make parameters require gradients
        params = {k: v.requires_grad_() for k, v in params.items()}

        # Setup optimizer
        optimizer = torch.optim.Adam(params.values(), lr=self.learning_rate)

        prev_loss = float('inf')
        best_params = None
        best_loss = float('inf')

        for iteration in range(self.max_iterations):
            optimizer.zero_grad()

            # Apply current transform
            transformed = self._apply_transform(source, params)

            # Calculate loss
            loss = self._compute_loss(transformed, target, mask)

            if loss.item() < best_loss:
                best_loss = loss.item()
                best_params = {k: v.detach().clone() for k, v in params.items()}

            # Check convergence
            if abs(prev_loss - loss.item()) < self.convergence_threshold:
                break

            # Backpropagate
            loss.backward()
            optimizer.step()

            prev_loss = loss.item()

            if progress_callback:
                progress_callback(iteration, loss.item())

        # Apply best transform to get final result
        final_transformed = self._apply_transform(source, best_params)

        return RegistrationResult(
            transformed_image=final_transformed.cpu().numpy(),
            transform_params={k: v.cpu().detach().numpy() for k, v in best_params.items()},
            convergence_metric=best_loss,
            iteration_count=iteration + 1,
            success=best_loss < 1.0  # Threshold can be adjusted
        )

    def _apply_transform(
        self,
        image: torch.Tensor,
        params: Dict[str, torch.Tensor]
    ) -> torch.Tensor:
        """Apply transformation to image"""
        if self.method == RegistrationMethod.RIGID:
            return self._apply_rigid_transform(image, params)
        elif self.method == RegistrationMethod.AFFINE:
            return self._apply_affine_transform(image, params)
        else:
            return self._apply_elastic_transform(image, params)

    def _compute_loss(
        self,
        transformed: torch.Tensor,
        target: torch.Tensor,
        mask: Optional[torch.Tensor]
    ) -> torch.Tensor:
        """Compute registration loss"""
        diff = transformed - target
        if mask is not None:
            diff = diff * mask
        return torch.mean(diff ** 2)

    def _apply_rigid_transform(
        self,
        image: torch.Tensor,
        params: Dict[str, torch.Tensor]
    ) -> torch.Tensor:
        """Apply rigid transformation"""
        # Create affine matrix from rotation and translation
        theta = params['rotation']
        tx, ty = params['translation']

        cos_t = torch.cos(theta)
        sin_t = torch.sin(theta)

        matrix = torch.tensor([
            [cos_t, -sin_t, tx],
            [sin_t, cos_t, ty]
        ], device=self.device, dtype=self.dtype)

        # Add batch dimension
        image = image.unsqueeze(0)
        matrix = matrix.unsqueeze(0)

        # Apply transform
        grid = F.affine_grid(matrix, image.size(), align_corners=False)
        transformed = F.grid_sample(image, grid, align_corners=False)

        return transformed.squeeze(0)

# Example usage:
if __name__ == "__main__":
    # Create registration instance
    registration = ImageRegistration(
        method=RegistrationMethod.RIGID,
        cuda_enabled=True
    )

    # Load example images
    source_img = np.load("source_image.npy")
    target_img = np.load("target_image.npy")

    # Register images
    result = registration.register_images(
        source=source_img,
        target=target_img,
        progress_callback=lambda i, l: print(f"Iteration {i}: Loss = {l:.6f}")
    )

    print("\nRegistration complete:")
    print(f"Final loss: {result.convergence_metric:.6f}")
    print(f"Iterations: {result.iteration_count}")
    print(f"Success: {result.success}")

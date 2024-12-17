# src/PyISI/processing/segmentation/areas.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import torch
from numpy.typing import NDArray
from scipy import ndimage
from ...core.exceptions import SegmentationError
from ...utils.decorators import validate_input, requires_cuda

@dataclass
class AreaInfo:
    """Information about a detected visual area"""
    id: int
    name: str
    boundary: NDArray  # Boolean mask of area boundary
    center: Tuple[float, float]  # Center of mass coordinates
    sign: float  # Visual field sign (1 or -1)
    size: float  # Area size in mm²
    neighbors: List[int]  # IDs of neighboring areas

class VisualAreaSegmenter:
    """Segments visual areas from retinotopic maps using gradient-based detection.

    This is a modern Python implementation of the MATLAB getMouseAreasX.m logic,
    with added GPU acceleration and robust error handling.

    Parameters
    ----------
    smoothing_sigma : float, optional
        Gaussian smoothing sigma for gradient computation, by default 1.0
    min_area_size : float, optional
        Minimum area size in mm², by default 0.01
    boundary_threshold : float, optional
        Threshold for boundary detection, by default 0.5
    use_gpu : bool, optional
        Whether to use GPU acceleration when available, by default True
    """

    def __init__(
        self,
        smoothing_sigma: float = 1.0,
        min_area_size: float = 0.01,
        boundary_threshold: float = 0.5,
        use_gpu: bool = True
    ):
        self.smoothing_sigma = smoothing_sigma
        self.min_area_size = min_area_size
        self.boundary_threshold = boundary_threshold
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = torch.device('cuda' if self.use_gpu else 'cpu')

    @validate_input
    def segment_areas(
        self,
        kmap_hor: NDArray,
        kmap_vert: NDArray,
        pixpermm: float
    ) -> Dict[str, AreaInfo]:
        """Segment visual areas from horizontal and vertical retinotopic maps.

        Parameters
        ----------
        kmap_hor : NDArray
            Horizontal retinotopic phase map
        kmap_vert : NDArray
            Vertical retinotopic phase map
        pixpermm : float
            Pixels per millimeter scale factor

        Returns
        -------
        Dict[str, AreaInfo]
            Dictionary of detected areas with their properties

        Raises
        ------
        SegmentationError
            If segmentation fails or produces invalid results
        """
        # Validate input shapes and types
        if kmap_hor.shape != kmap_vert.shape:
            raise ValueError("Horizontal and vertical maps must have same shape")

        try:
            # Convert to tensors if using GPU
            if self.use_gpu:
                kmap_hor = torch.from_numpy(kmap_hor).to(self.device)
                kmap_vert = torch.from_numpy(kmap_vert).to(self.device)

            # Compute gradients
            grad_h, grad_v = self._compute_gradients(kmap_hor, kmap_vert)

            # Generate sign map
            sign_map = self._compute_sign_map(grad_h, grad_v)

            # Detect boundaries
            boundaries = self._detect_boundaries(grad_h, grad_v, sign_map)

            # Extract and label areas
            areas = self._extract_areas(boundaries, sign_map, pixpermm)

            # Post-process and validate results
            areas = self._post_process_areas(areas)

            return areas

        except Exception as e:
            raise SegmentationError(f"Area segmentation failed: {str(e)}") from e

    def _compute_gradients(
        self,
        kmap_hor: NDArray,
        kmap_vert: NDArray
    ) -> Tuple[NDArray, NDArray]:
        """Compute smoothed gradients of the retinotopic maps."""
        # Apply Gaussian smoothing
        kmap_hor = ndimage.gaussian_filter(kmap_hor, self.smoothing_sigma)
        kmap_vert = ndimage.gaussian_filter(kmap_vert, self.smoothing_sigma)

        # Compute gradients
        grad_h_y, grad_h_x = np.gradient(kmap_hor)
        grad_v_y, grad_v_x = np.gradient(kmap_vert)

        return (grad_h_x + 1j * grad_h_y, grad_v_x + 1j * grad_v_y)

    def _compute_sign_map(
        self,
        grad_h: NDArray,
        grad_v: NDArray
    ) -> NDArray:
        """Compute visual field sign map from gradients."""
        # Calculate angle between gradients
        angle = np.angle(grad_h * np.conj(grad_v))

        # Convert to visual field sign (-1 or 1)
        return np.sign(angle)

    def _detect_boundaries(
        self,
        grad_h: NDArray,
        grad_v: NDArray,
        sign_map: NDArray
    ) -> NDArray:
        """Detect area boundaries using gradient magnitude and sign changes."""
        # Compute gradient magnitudes
        mag_h = np.abs(grad_h)
        mag_v = np.abs(grad_v)

        # Find sign map transitions
        sign_edges = ndimage.generic_gradient_magnitude(sign_map, ndimage.sobel)

        # Combine evidence for boundaries
        boundaries = (
            (mag_h > self.boundary_threshold) |
            (mag_v > self.boundary_threshold) |
            (sign_edges > 0)
        )

        return boundaries

    def _extract_areas(
        self,
        boundaries: NDArray,
        sign_map: NDArray,
        pixpermm: float
    ) -> Dict[str, AreaInfo]:
        """Extract individual areas from boundary map."""
        # Label connected components
        labels, num_labels = ndimage.label(~boundaries)

        areas = {}
        for label_id in range(1, num_labels + 1):
            # Get area mask
            mask = labels == label_id

            # Calculate area properties
            area_size = np.sum(mask) / (pixpermm ** 2)

            # Skip if too small
            if area_size < self.min_area_size:
                continue

            # Get dominant sign
            sign = np.sign(np.mean(sign_map[mask]))

            # Calculate center of mass
            cy, cx = ndimage.center_of_mass(mask)

            # Find neighbors
            dilated = ndimage.binary_dilation(mask)
            neighbor_ids = set(labels[dilated & ~mask]) - {0, label_id}

            # Create AreaInfo object
            area_info = AreaInfo(
                id=label_id,
                name=f"Area_{label_id}",
                boundary=mask,
                center=(float(cx), float(cy)),
                sign=float(sign),
                size=float(area_size),
                neighbors=sorted(neighbor_ids)
            )

            areas[f"Area_{label_id}"] = area_info

        return areas

    def _post_process_areas(
        self,
        areas: Dict[str, AreaInfo]
    ) -> Dict[str, AreaInfo]:
        """Post-process detected areas to clean up results."""
        # Add V1 identification
        v1_id = self._identify_v1(areas)
        if v1_id:
            areas[v1_id].name = "V1"

        # Clean up small artifacts
        areas = {k: v for k, v in areas.items()
                if v.size >= self.min_area_size}

        return areas

    def _identify_v1(
        self,
        areas: Dict[str, AreaInfo]
    ) -> Optional[str]:
        """Identify the V1 area based on size and location."""
        # Find largest area near image center
        max_size = 0
        v1_id = None

        for area_id, area in areas.items():
            if area.size > max_size:
                max_size = area.size
                v1_id = area_id

        return v1_id

# Example usage:
if __name__ == "__main__":
    # Load sample data
    kmap_hor = np.load("sample_horizontal_map.npy")
    kmap_vert = np.load("sample_vertical_map.npy")

    # Create segmenter
    segmenter = VisualAreaSegmenter(
        smoothing_sigma=1.0,
        min_area_size=0.01,
        boundary_threshold=0.5
    )

    # Run segmentation
    areas = segmenter.segment_areas(
        kmap_hor=kmap_hor,
        kmap_vert=kmap_vert,
        pixpermm=10.0
    )

    # Print results
    print(f"Found {len(areas)} visual areas:")
    for name, area in areas.items():
        print(f"{name}: {area.size:.2f} mm², sign={area.sign}")

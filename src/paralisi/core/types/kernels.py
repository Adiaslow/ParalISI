from enum import Enum

class KernelType(Enum):
    """Types of spatial filter kernels."""
    GAUSSIAN = "gaussian"
    HANN = "hann"
    DISK = "disk"

# Contributing to ParalISI

First off, thank you for considering contributing to ParalISI!

## Project Vision

ParalISI is modernizing a MATLAB-based Intrinsic Signal Imaging (ISI) analysis pipeline for visual cortex experiments. Our goal is to create a high-performance, maintainable Python implementation that preserves the scientific validity of the original while incorporating modern software engineering practices.

### Core Objectives
- Maintain scientific accuracy of the original MATLAB implementation
- Achieve significant performance improvements through GPU acceleration
- Create a clean, maintainable codebase following SOLID principles
- Provide comprehensive test coverage and validation
- Support modern Python development practices

### Technical Focus Areas
1. **Code Quality**
   - Type hints throughout the codebase
   - Adherence to Google Python Style Guide
   - Clear separation of concerns
   - Modern Python packaging standards

2. **Performance**
   - GPU acceleration via CUDA
   - Vectorized operations using NumPy/CuPy
   - Memory-efficient data structures
   - Parallelized processing where applicable

3. **Scientific Validity**
   - Validated results against original implementation
   - Comprehensive testing of numerical accuracy
   - Clear documentation of algorithms and methods
   - Reproducible analysis pipeline

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Style](#code-style)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct (see CODE_OF_CONDUCT.md). Please report any unacceptable behavior to [project maintainer email].

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone git@github.com:your-username/ParalISI.git
cd ParalISI
```
3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
4. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Development Environment

### Required Tools
- Python 3.10+
- Git
- A suitable IDE (we recommend VS Code with Python extensions)
- CUDA Toolkit 11.0+ (for GPU development)

### Optional Tools
- `pre-commit` for automated style checking
- `black` for code formatting
- `mypy` for type checking

### Environment Setup
```bash
# Install pre-commit hooks
pre-commit install

# Install additional development tools
pip install black mypy pytest pytest-cov
```

## Code Style

We strictly follow the Google Python Style Guide with additional requirements for scientific computing:

1. **Type Hints**: All code must use type hints
```python
from typing import Optional, Tuple
import numpy as np
import torch

def process_retinotopy(
    data: np.ndarray,
    threshold: float = 0.5,
    use_gpu: bool = False
) -> Tuple[np.ndarray, np.ndarray]:
    """Process retinotopic mapping data.

    Args:
        data: Raw imaging data array of shape (T, H, W)
        threshold: Signal threshold for processing
        use_gpu: Whether to use GPU acceleration

    Returns:
        Tuple containing:
            - Altitude map array of shape (H, W)
            - Azimuth map array of shape (H, W)

    Raises:
        ValueError: If data dimensions are invalid
    """
    # Implementation
```

2. **Documentation**: All functions and classes must have detailed docstrings following NumPy style
3. **Vectorization**: Prefer vectorized operations over loops
```python
# Good
result = np.mean(data, axis=0)

# Avoid
result = np.zeros(data.shape[1:])
for i in range(data.shape[1]):
    for j in range(data.shape[2]):
        result[i,j] = np.mean(data[:,i,j])
```

4. **GPU Support**: Include GPU implementations where beneficial
```python
def compute_phase_map(
    data: Union[np.ndarray, torch.Tensor],
    use_gpu: bool = False
) -> Union[np.ndarray, torch.Tensor]:
    if use_gpu and isinstance(data, np.ndarray):
        data = torch.from_numpy(data).cuda()
    # Implementation
```

[Rest of the content remains the same as the previous version...]

## Testing

We use pytest for testing. All code must include tests that validate both functionality and scientific accuracy:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=paralisi

# Run GPU-specific tests
pytest tests/gpu/
```

### Test Requirements
- Unit tests for all functionality
- Integration tests for processing pipelines
- Validation tests against MATLAB implementation
- GPU compatibility tests
- Performance benchmarks
- Edge cases and error conditions

### Scientific Validation
- Include test data from published results
- Validate numerical accuracy against MATLAB version
- Document and test assumptions about data formatting
- Verify preservation of scientific validity

[Rest of the content remains the same...]

## Questions?

If you have questions about contributing, feel free to:
1. Open an issue
2. Contact the maintainers
3. Ask in our developer chat

Thank you for contributing to ParalISI!

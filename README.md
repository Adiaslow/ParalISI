# PyISI: Python Intrinsic Signal Imaging Analysis

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PyISI is a modern Python library for analyzing intrinsic signal imaging (ISI) data from visual cortex experiments. This project is a complete modernization of a legacy MATLAB codebase, rebuilt with contemporary software engineering practices and performance optimizations.

## Features

- **Complete ISI Analysis Pipeline**
  - Robust data loading and preprocessing
  - Advanced signal processing and filtering
  - Retinotopic mapping and visualization
  - Visual area segmentation and analysis
  - Orientation and direction map processing
  - Quality assessment and validation

- **Modern Implementation**
  - Type-annotated codebase (Python 3.10+)
  - GPU acceleration via CUDA
  - Vectorized operations with NumPy/CuPy
  - Memory-efficient data handling
  - Comprehensive test suite
  - Clean, maintainable architecture following SOLID principles

## Installation

```bash
# Basic installation
pip install pyisi

# With GPU support
pip install pyisi[cuda]
```

### Requirements

- Python 3.10+
- NumPy
- SciPy
- PyTorch
- CuPy (optional, for GPU support)
- CUDA Toolkit 11.0+ (optional, for GPU support)

<!--
## Quick Start

```python
from pyisi.core import Experiment
from pyisi.processing import TrialProcessor
from pyisi.analysis import OrientationAnalyzer

# Load experimental data
experiment = Experiment.from_analyzer("path/to/analyzer/file")

# Process trials
processor = TrialProcessor()
processed_data = processor.process_condition_data(experiment)

# Analyze orientation maps
analyzer = OrientationAnalyzer()
orientation_maps = analyzer.analyze_orientation_map(processed_data)
```
-->
## Documentation

Comprehensive documentation is available at [docs.pyisi.org](https://docs.pyisi.org), including:
- Detailed API reference
- Usage tutorials and examples
- Migration guide from MATLAB
- Performance optimization tips
- Best practices for ISI analysis

## Key Improvements Over MATLAB Version

- **Performance**: GPU acceleration and vectorized operations provide significant speedups
- **Reliability**: Comprehensive testing and validation ensure reproducible results
- **Maintainability**: Modern Python architecture with clear separation of concerns
- **Extensibility**: Modular design allows easy addition of new analysis methods
- **User Experience**: Improved error handling and informative feedback
- **Memory Efficiency**: Optimized data structures and processing pipeline

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Setting up the development environment
- Running tests
- Code style guidelines
- Submission process

## Citation

If you use PyISI in your research, please cite:

```bibtex
@software{pyisi2024,
  title = {PyISI: Python Intrinsic Signal Imaging Analysis},
  year = {2024},
  url = {https://github.com/username/pyisi},
  version = {0.1.0}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project builds upon the original MATLAB ISI analysis codebase developed by [Original Authors]. We thank the contributors and maintainers of the original codebase for their foundational work in ISI analysis.

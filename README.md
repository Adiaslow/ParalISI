# ParalISI: Modern Python Implementation of Intrinsic Signal Imaging Analysis

[![PyPI version](https://img.shields.io/pypi/v/paralisi.svg)](https://pypi.org/project/paralisi/)
[![Documentation Status](https://readthedocs.org/projects/paralisi/badge/?version=latest)](https://paralisi.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://github.com/Adiaslow/ParalISI/workflows/Python%20package/badge.svg)](https://github.com/Adiaslow/ParalISI/actions)
[![Code Coverage](https://codecov.io/gh/Adiaslow/ParalISI/branch/main/graph/badge.svg)](https://codecov.io/gh/Adiaslow/ParalISI)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

ParalISI is a modern Python library implementing the intrinsic signal imaging (ISI) analysis protocol described in [Juavinett et al. (2016)](https://doi.org/10.1038/nprot.2016.158). Developed in the [Kim Laboratory]([https://mcd.ucsc.edu/faculty/kim-e.html](https://www.ejkimlab.com/)) at UC Santa Cruz, this project modernizes the original MATLAB codebase with contemporary software engineering practices, improved performance, and enhanced usability.

## Features

### Core ISI Analysis
- Complete retinotopic mapping pipeline from raw imaging data
- Automated visual area segmentation based on field sign reversals
- Generation of altitude and azimuth maps
- Blood vessel artifact removal
- Customizable filtering and signal processing
- Support for both episodic and continuous stimulation paradigms

### Technical Improvements
- **Performance**: GPU acceleration via CUDA for intensive computations
- **Modularity**: Clean separation between data loading, processing, and visualization
- **Validation**: Comprehensive test suite ensuring accurate reproduction of published methods
- **Extensibility**: Modern Python architecture allowing easy addition of new analysis methods
- **Automation**: Streamlined workflow requiring minimal manual intervention

## Installation

```bash
# Basic installation
pip install paralisi

# With GPU support
pip install paralisi[cuda]
```

### Requirements
- Python 3.10+
- NumPy
- SciPy
- PyTorch
- CuPy (optional, for GPU support)
- CUDA Toolkit 11.0+ (optional, for GPU support)

## Quick Start

```python
import paralisi
from pathlib import Path

try:
    # Robust path handling
    data_path = Path("/path/to/data").resolve()

    # Load and preprocess imaging data
    data = paralisi.load_data(data_path)
    preprocessed = paralisi.preprocess(data)

    # Generate retinotopic maps
    alt_map, az_map = paralisi.compute_retinotopy(preprocessed)

    # Segment visual areas
    areas = paralisi.segment_areas(alt_map, az_map)

    # Visualize results
    paralisi.plot_visual_areas(areas)

except FileNotFoundError:
    print("Data file not found. Please check the path.")
except paralisi.exceptions.ProcessingError as e:
    print(f"Processing error: {e}")
```

## Key Components

### Data Processing
- `paralisi.io`: Efficient data loading and management
- `paralisi.processing`: Core signal processing algorithms
- `paralisi.analysis`: Advanced analysis tools
- `paralisi.visualization`: Publication-quality plotting

### GPU Acceleration
- Parallel processing of large imaging datasets
- CUDA-optimized filtering operations
- Memory-efficient handling of time series data

### Quality Control
- Automated artifact detection
- Signal quality assessment
- Validation against published results

## Documentation

Full documentation is available at [docs.paralisi.org](https://docs.paralisi.org), including:
- Detailed API reference
- Step-by-step tutorials
- Best practices for ISI analysis
- Migration guide from MATLAB
- Performance optimization tips

## Research Team

### Project Leadership
- **Dr. Euiseok Kim** (Principal Investigator) - UC Santa Cruz
- **Adam Murray** (Lead Developer) - UC Santa Cruz
- **Matthew Jacobs** (Scientific Advisor) - UC Santa Cruz
- **Hylen James** (Hardware Development) - UC Santa Cruz

For detailed information about project contributors, see [AUTHORS.md](AUTHORS.md) and [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Contributing

Contributions are welcome! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on:
- Setting up the development environment
- Running tests
- Code style guidelines
- Submission process

## Citation

If you use ParalISI in your research, please cite both the original protocol and this implementation:

```bibtex
@article{juavinett2016automated,
    title={Automated identification of mouse visual areas with intrinsic signal imaging},
    author={Juavinett, Ashley L and Nauhaus, Ian and Garrett, Marina E and Zhuang, Jun and Callaway, Edward M},
    journal={Nature protocols},
    volume={12},
    number={1},
    pages={32--43},
    year={2016}
}

@software{murray2024paralisi,
    title={ParalISI: Python Implementation of Intrinsic Signal Imaging Analysis},
    author={Murray, Adam M},
    year={2024},
    url={https://github.com/Adiaslow/ParalISI},
    version={0.1.0}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was developed in the Kim Laboratory at UC Santa Cruz, which investigates the organizational logic of long-distance cortical circuits and molecular mechanisms of their development. We thank the authors of the original protocol for their foundational work in automated visual area identification. For detailed acknowledgments, see [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md).

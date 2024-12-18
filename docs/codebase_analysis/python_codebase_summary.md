# Python Codebase Summary

Generated on: 2024-12-17 18:28:07

## Summary Statistics
- Total Python files: 52
- Total functions: 150

---


## Directory: pyisi


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---


## Directory: pyisi/visualization


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### interactive.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### maps.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### plots.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---


## Directory: pyisi/core


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### config.py
**File Statistics:**
- Total lines: 173
- Non-empty lines: 146
- Number of functions: 5

**File Description:**
Configuration management for ISI experiments.

This module provides configuration classes and utilities for managing
Intrinsic Signal Imaging (ISI) experimental parameters and settings.

**Functions:**
```python
def __post_init__
def __post_init__
def __post_init__
def from_yaml
def save
```
---

### exceptions.py
**File Statistics:**
- Total lines: 46
- Non-empty lines: 34
- Number of functions: 0

---

### experiment.py
**File Statistics:**
- Total lines: 283
- Non-empty lines: 223
- Number of functions: 13

**File Description:**
Core experiment handling for ISI analysis.

This module provides the main experiment class for handling Intrinsic Signal Imaging
(ISI) experiments, including data loading, processing, and analysis.

**Functions:**
```python
def __str__
def __init__
def _validate_config
def load_data
def _load_trials
def process_trials
def _validate_trial_range
def _process_trial_range
def save_results
def _update_status
def _handle_error
def progress
def get_trial_data
```
---

### factories.py
**File Statistics:**
- Total lines: 51
- Non-empty lines: 40
- Number of functions: 2

**File Description:**
Factories for creating PyISI components.

**Functions:**
```python
def create
def create
```
---

### interfaces.py
**File Statistics:**
- Total lines: 78
- Non-empty lines: 58
- Number of functions: 13

**File Description:**
Core interfaces and protocols for the PyISI package.

**Functions:**
```python
def load
def supports_format
def process
def validate
def get
def put
def clear
def apply
def register
def process
def compute
def analyze
def test
```
---

### managers.py
**File Statistics:**
- Total lines: 134
- Non-empty lines: 111
- Number of functions: 4

**File Description:**
Experiment management for PyISI.

**Functions:**
```python
def __init__
def process_trial
def process_trials
def _generate_masks
```
---

### stores.py
**File Statistics:**
- Total lines: 49
- Non-empty lines: 38
- Number of functions: 2

**File Description:**
Data stores for PyISI.

**Functions:**
```python
def __init__
def get_trial
```
---

### trial.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### validation.py
**File Statistics:**
- Total lines: 292
- Non-empty lines: 240
- Number of functions: 9

**Functions:**
```python
def __init__
def validate_experiment
def _validate_data_integrity
def _validate_sync_signal
def _detect_motion_artifacts
def _calculate_snr
def _check_photobleaching
def __init__
def validate_batch
```
---


## Directory: pyisi/core/types


### __init__.py
**File Statistics:**
- Total lines: 31
- Non-empty lines: 28
- Number of functions: 0

**File Description:**
Type definitions for PyISI core functionality.

---

### config_types.py
**File Statistics:**
- Total lines: 80
- Non-empty lines: 69
- Number of functions: 5

**File Description:**
Configuration type definitions.

**Functions:**
```python
def __str__
def __str__
def __post_init__
def __post_init__
def __post_init__
```
---

### data_types.py
**File Statistics:**
- Total lines: 32
- Non-empty lines: 26
- Number of functions: 0

**File Description:**
Core data type definitions.

---

### experiment.py
**File Statistics:**
- Total lines: 27
- Non-empty lines: 24
- Number of functions: 0

---


## Directory: pyisi/core/protocols


### __init__.py
**File Statistics:**
- Total lines: 17
- Non-empty lines: 14
- Number of functions: 0

**File Description:**
Protocol definitions for PyISI core functionality.

---

### caching.py
**File Statistics:**
- Total lines: 22
- Non-empty lines: 15
- Number of functions: 3

**File Description:**
Caching protocols.

**Functions:**
```python
def get
def put
def clear
```
---

### loading.py
**File Statistics:**
- Total lines: 18
- Non-empty lines: 13
- Number of functions: 2

**File Description:**
Data loading protocols.

**Functions:**
```python
def load
def supports_format
```
---

### processing.py
**File Statistics:**
- Total lines: 17
- Non-empty lines: 12
- Number of functions: 2

**File Description:**
Data processing protocols.

**Functions:**
```python
def process
def validate
```
---

### storage.py
**File Statistics:**
- Total lines: 18
- Non-empty lines: 13
- Number of functions: 2

**File Description:**
Data storage protocols.

**Functions:**
```python
def save
def exists
```
---

### validation.py
**File Statistics:**
- Total lines: 17
- Non-empty lines: 12
- Number of functions: 2

**File Description:**
Data validation protocols.

**Functions:**
```python
def validate
def get_validation_errors
```
---


## Directory: pyisi/analysis


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### maps.py
**File Statistics:**
- Total lines: 254
- Non-empty lines: 205
- Number of functions: 7

**Functions:**
```python
def __init__
def process_orientation_map
def process_direction_map
def process_color_map
def __init__
def compute_selectivity_stats
def compute_preference_distribution
```
---

### metrics.py
**File Statistics:**
- Total lines: 137
- Non-empty lines: 113
- Number of functions: 7

**Functions:**
```python
def __init__
def compute_response_metrics
def _calculate_snr
def _calculate_reliability
def _calculate_amplitude
def _calculate_latency
def _calculate_variance
```
---

### orientation.py
**File Statistics:**
- Total lines: 218
- Non-empty lines: 181
- Number of functions: 7

**Functions:**
```python
def __init__
def analyze_orientation_map
def _compute_orientation_gradient
def _compute_local_uniformity
def _detect_pinwheels
def _estimate_domain_size
def get_analysis_summary
```
---

### quality.py
**File Statistics:**
- Total lines: 158
- Non-empty lines: 131
- Number of functions: 7

**Functions:**
```python
def __init__
def assess_quality
def _detect_motion
def _calculate_noise
def _assess_signal
def _detect_artifacts
def _determine_quality
```
---

### statistics.py
**File Statistics:**
- Total lines: 157
- Non-empty lines: 134
- Number of functions: 4

**Functions:**
```python
def __init__
def compare_conditions
def _run_ttest
def _run_wilcoxon
```
---


## Directory: pyisi/processing


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### filters.py
**File Statistics:**
- Total lines: 134
- Non-empty lines: 112
- Number of functions: 6

**Functions:**
```python
def __init__
def create_kernel
def _create_base_kernel
def _create_gaussian
def _create_hann
def _create_disk
```
---

### pipeline.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### registration.py
**File Statistics:**
- Total lines: 272
- Non-empty lines: 229
- Number of functions: 8

**Functions:**
```python
def __init__
def _setup_optimizer
def register_images
def _initialize_transform
def _optimize_transform
def _apply_transform
def _compute_loss
def _apply_rigid_transform
```
---

### signal.py
**File Statistics:**
- Total lines: 38
- Non-empty lines: 32
- Number of functions: 2

**Functions:**
```python
def normalize_by_baseline
def average_across_time
```
---

### trial_processor.py
**File Statistics:**
- Total lines: 129
- Non-empty lines: 103
- Number of functions: 4

**Functions:**
```python
def __init__
def process_condition_data
def _process_trial_set
def _compute_trial_variance
```
---


## Directory: pyisi/processing/filters


### gaussian.py
**File Statistics:**
- Total lines: 27
- Non-empty lines: 21
- Number of functions: 3

**Functions:**
```python
def __init__
def apply
def _create_kernel
```
---


## Directory: pyisi/processing/segmentation


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### areas.py
**File Statistics:**
- Total lines: 266
- Non-empty lines: 218
- Number of functions: 8

**Functions:**
```python
def __init__
def segment_areas
def _compute_gradients
def _compute_sign_map
def _detect_boundaries
def _extract_areas
def _post_process_areas
def _identify_v1
```
---

### retinotopy.py
**File Statistics:**
- Total lines: 225
- Non-empty lines: 183
- Number of functions: 6

**Functions:**
```python
def __init__
def _setup_filters
def compute_phase_maps
def _find_stimulus_frequency
def generate_sign_map
def analyze_retinotopy
```
---


## Directory: pyisi/io


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### loaders.py
**File Statistics:**
- Total lines: 45
- Non-empty lines: 35
- Number of functions: 2

**File Description:**
Data loading implementations.

**Functions:**
```python
def load
def supports_format
```
---

### readers.py
**File Statistics:**
- Total lines: 173
- Non-empty lines: 143
- Number of functions: 8

**Functions:**
```python
def __init__
def load_analyzer
def _load_params
def _load_metadata
def _load_conditions
def _load_timestamps
def __init__
def load_params
```
---

### writers.py
**File Statistics:**
- Total lines: 168
- Non-empty lines: 140
- Number of functions: 5

**Functions:**
```python
def __init__
def save_processed_data
def _save_hdf5
def _save_npz
def save_params
```
---


## Directory: pyisi/utils


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### cuda_setup.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### decorators.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### parallel.py
**File Statistics:**
- Total lines: 21
- Non-empty lines: 16
- Number of functions: 2

**Functions:**
```python
def __init__
def process_batch
```
---


## Directory: gui


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---


## Directory: gui/widgets


### __init__.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

### main_window.py
**File Statistics:**
- Total lines: 1
- Non-empty lines: 0
- Number of functions: 0

---

# src/paralisi/core/results/validation_result.py

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ValidationResult:
    """Container for validation results"""
    passed: bool
    metrics: Dict[str, float]
    issues: List[str]
    recommendations: List[str]

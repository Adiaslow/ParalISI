# tests/test_processing/test_pipeline.py

import pytest

from PyISI.core.data_types import ISIDataset
from PyISI.processing.pipeline import AnalysisPipeline

def test_full_processing_pipeline():
    """Test complete analysis pipeline"""
    dataset = ISIDataset(test_data_path)
    processor = AnalysisPipeline()
    results = processor.run_analysis(dataset)
    validate_results(results)

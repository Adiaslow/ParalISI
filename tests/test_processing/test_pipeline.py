# tests/test_processing/test_pipeline.py

def test_full_processing_pipeline():
    """Test complete analysis pipeline"""
    dataset = ISIDataset(test_data_path)
    processor = AnalysisPipeline()
    results = processor.run_analysis(dataset)
    validate_results(results)

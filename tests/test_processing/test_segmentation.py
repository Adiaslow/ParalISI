# tests/test_processing/test_segmentation.py

def test_area_detection_accuracy():
    """Test area detection against known ground truth"""
    segmenter = VisualAreaSegmenter()
    result = segmenter.detect_areas(test_data)
    assert_allclose(result.area_boundaries, expected_boundaries)

@pytest.mark.gpu
def test_phase_map_computation():
    """Test phase map calculation with GPU acceleration"""
    mapper = RetinotopicMapper(cuda_enabled=True)
    phase_maps = mapper.compute_phase_maps(test_responses)
    assert torch.allclose(phase_maps, expected_maps)

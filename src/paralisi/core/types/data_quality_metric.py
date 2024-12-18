# src/paralisi/core/types/data_quality_metric.py

from enum import Enum

class DataQualityMetric(Enum):
    """Common data quality metrics"""
    SNR = "signal_to_noise"
    MOTION = "motion_artifact"
    SYNC_QUALITY = "sync_quality"
    BLEACHING = "photobleaching"
    CONTRAST = "contrast"

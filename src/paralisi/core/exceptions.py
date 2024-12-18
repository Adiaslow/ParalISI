# src/PyISI/core/exceptions.py

class ProcessingError(Exception):
    """Base exception for processing-related errors in PyISI"""
    pass

class ValidationError(Exception):
    """Exception raised when data validation fails"""
    pass

class ConfigurationError(Exception):
    """Exception raised when there's an issue with configuration settings"""
    pass

class IOError(Exception):
    """Exception raised for input/output operations"""
    pass

class DataError(Exception):
    """Exception raised for data-related errors"""
    pass

class AnalysisError(Exception):
    """Exception raised for analysis-related errors"""
    pass

class PlottingError(Exception):
    """Exception raised for plotting-related errors"""
    pass

class QualityError(Exception):
    """Exception raised for data quality issues"""
    pass

class StatisticsError(Exception):
    """Exception raised for statistical errors"""
    pass

class RegistrationError(Exception):
    """Exception raised for registration errors"""
    pass

class SegmentationError(Exception):
    """Exception raised for segmentation errors"""
    pass

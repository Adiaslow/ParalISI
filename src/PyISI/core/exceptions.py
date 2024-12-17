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

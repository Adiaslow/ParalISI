# src/paralisi/core/exceptions/processing_exceptions.py

class ProcessingError(Exception):
    """Exception raised for errors in the data processing."""
    def __init__(self, message: str):
        super().__init__(message)

class ValidationError(Exception):
    """Exception raised for validation errors."""
    def __init__(self, message: str):
        super().__init__(message)

class SegmentationError(Exception):
    """Exception raised for errors in the data segmentation."""
    def __init__(self, message: str):
        super().__init__(message)

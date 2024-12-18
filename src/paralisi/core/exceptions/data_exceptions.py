# src/paralisi/core/exceptions/data_exceptions.py

class DataLoadingError(Exception):
    """Exception raised for errors in the data loading process."""
    def __init__(self, message: str):
        super().__init__(message)

class MetadataError(Exception):
    """Exception raised for errors in metadata handling."""
    def __init__(self, message: str):
        super().__init__(message)

class ConfigurationError(Exception):
    """Exception raised for errors in the configuration process."""
    def __init__(self, message: str):
        super().__init__(message)

# src/paralisi/core/exceptions/storage_exceptions.py

class StorageError(Exception):
    """Exception raised for errors in the data storage process."""
    def __init__(self, message: str):
        super().__init__(message)

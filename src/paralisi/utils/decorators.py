# src/paralisi/utils/decorators.py

"""Module for custom decorators."""

from functools import wraps
import time

def validate_input(func):
    """Decorator to validate the input of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Add your validation logic here
        for arg in args:
            if arg is None:
                raise ValueError("None value found in the arguments.")
        return func(*args, **kwargs)
    return wrapper

def requires_cuda(func):
    """Decorator to ensure that a function is run only if CUDA is available."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import torch
        if not torch.cuda.is_available():
            raise EnvironmentError("CUDA is not available.")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    """Decorator to measure the execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} executed in {elapsed_time:.4f} seconds.")
        return result
    return wrapper

def retry_on_exception(max_retries=3):
    """Decorator to retry a function if an exception occurs."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Exception occurred: {e}. Retrying {retries + 1}/{max_retries}...")
                    retries += 1
            raise Exception(f"Function {func.__name__} failed after {max_retries} retries.")
        return wrapper
    return decorator

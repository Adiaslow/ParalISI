# src/PyISI/utils/parallel.py

class BatchProcessor:
    """Handles parallel processing of multiple sessions"""

    def __init__(self,
                 n_workers: int = -1,
                 chunk_size: str = '100MB'):
        self.n_workers = n_workers
        self.chunk_size = chunk_size

    def process_batch(self,
                     data_paths: List[Path],
                     processing_fn: Callable,
                     **kwargs) -> List[Any]:
        """Parallel batch processing with progress tracking"""
        ...

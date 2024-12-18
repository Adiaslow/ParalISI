# src/paralisi/core/validation/validator.py

from typing import Dict
from numpy.typing import NDArray
from ..interfaces.validator import Validator as ValidatorProtocol
from ..exceptions import ValidationError
from . import DataIntegrityValidator, MotionArtifactsValidator, PhotobleachingValidator, SNRValidator, SyncSignalValidator

class Validator:
    """Encapsulates all validation methods."""

    def __init__(self):
        self.data_integrity_validator = DataIntegrityValidator()
        self.sync_signal_validator = SyncSignalValidator()
        self.motion_artifacts_validator = MotionArtifactsValidator()
        self.snr_validator = SNRValidator()
        self.photobleaching_validator = PhotobleachingValidator()

    def validate_data_integrity(self, data: NDArray, metadata: Dict) -> None:
        self.data_integrity_validator.validate(data, metadata)

    def validate_sync_signal(self, sync_signal: NDArray) -> float:
        return self.sync_signal_validator.validate(sync_signal, {})

    def detect_motion_artifacts(self, data: NDArray) -> float:
        return self.motion_artifacts_validator.validate(data, {})

    def calculate_snr(self, data: NDArray) -> float:
        return self.snr_validator.validate(data, {})

    def check_photobleaching(self, data: NDArray) -> float:
        return self.photobleaching_validator.validate(data, {})

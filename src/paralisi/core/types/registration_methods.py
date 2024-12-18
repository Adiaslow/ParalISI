# src/paralisi/core/types/registration_method.py

from enum import Enum

class RegistrationMethod(Enum):
    """Supported registration methods"""
    RIGID = "rigid"
    AFFINE = "affine"
    ELASTIC = "elastic"

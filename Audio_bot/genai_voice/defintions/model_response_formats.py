"""Response Formats for Models"""
from enum import IntEnum


class ModelResponseFormat(IntEnum):
    """Describe the output format for AI models"""

    TEXT = 1
    JSON = 2
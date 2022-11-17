from enum import Enum


class GenericErrors(Enum):
    INVALID_FILE_LENGTH = 0


class ErrorData:
    def __init__(self, error_type, repair_instructions):
        self.error_type = error_type
        self.repair_instructions = repair_instructions


class ErrorType(Enum):
    INVALID_VALUE = 0
    DATA_MISSING = 1


from enum import Enum


class GenericErrors(Enum):
    INVALID_FILE_LENGTH = 0
    MISSING_TERMINATOR = 1
    INVALID_ENTRY_AMOUNT = 2
    INVALID_SORTING = 3


class ErrorType(Enum):
    INVALID_VALUE = 0
    DATA_MISSING = 1


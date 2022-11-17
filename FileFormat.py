from abc import ABC, abstractmethod

from Error import Error
from ErrorType import ErrorType


class FileFormat(ABC):
    def __init__(self, expected_size, file_enum, id):
        self.expected_size = expected_size
        self.errors = list()
        self.id = id
        self.file_enum = file_enum
        self.all = list()

    @abstractmethod
    def resolve_error(self, error):
        pass

    @abstractmethod
    def read_write_instructions(self, field, buffer, read_mode, *args):
        pass

    @abstractmethod
    def write(self):
        pass

    def list_error(self):
        for error in self.errors:
            print('\t%s\n\t\t%s\n\t\t%s' % (error.enum.name, error.type.name, error.text))

    def get_errors(self):
        errors = list()
        for field in list(self.file_enum):
            if self.all[field] is None:
                errors.append(Error(field, ErrorType.DATA_MISSING, "%s: Value Missing" % field.name))

        return errors

    def resolve_errors(self):
        for error in self.errors:
            self.resolve_error(error)

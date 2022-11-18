from abc import ABC, abstractmethod

from Buffer import Buffer
from Error import Error
from ErrorType import ErrorType, GenericErrors


class StrictFileFormat(ABC):
    def __init__(self, expected_size, file_enum, buffer, id):
        self.expected_size = expected_size
        self.errors = list()
        self.id = id
        self.file_enum = file_enum
        self.fields = list()

        self.read(buffer)

    @abstractmethod
    def resolve_error(self, error):
        pass

    @abstractmethod
    def read_write_action(self, field, buffer, *args, read_mode):
        pass

    def list_error(self):
        for error in self.errors:
            print('\t%s\n\t\t%s\n\t\t%s' % (error.enum.name, error.type.name, error.text))

    def get_errors(self):
        errors = list()
        for field in list(self.file_enum):
            if self.fields[field] is None:
                errors.append(Error(field, ErrorType.DATA_MISSING, "%s: Value Missing" % field.name))

        return errors

    def resolve_errors(self):
        for error in self.errors:
            self.resolve_error(error)

    def read(self, buffer):
        if len(buffer.data) > self.expected_size:
            self.errors.append(Error(GenericErrors.INVALID_FILE_LENGTH, ErrorType.INVALID_VALUE, "File has extra data"))
        else:  # len <= expected size
            for field in list(self.file_enum):
                self.fields.append(self.read_write_action(field, buffer, read_mode=True))

    def write(self):
        buffer = Buffer(bytearray(self.expected_size), write=True)
        for field in list(self.file_enum):
            self.read_write_action(field, buffer, self.fields[field], read_mode=False)

        return buffer.data


class FlexibleFileFormat(ABC):
    def __init__(self, file_enum, entry_class, id):
        self.errors = list()
        self.id = id
        self.file_enum = file_enum
        self.entry_class = entry_class
        self.entries = list()
        self.num_entries = 0
        self.max_entries = 0

    @abstractmethod
    def resolve_error(self, error):
        pass

    @abstractmethod
    def read_write_action(self, field, buffer, *args, read_mode):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def read(self, buffer):
        pass

    @abstractmethod
    def read_entry(self, buffer):
        pass

    @abstractmethod
    def get_errors(self):
        pass

    def list_error(self):
        for error in self.errors:
            print('\t%s\n\t\t%s\n\t\t%s' % (error.enum.name, error.type.name, error.text))

    def resolve_errors(self):
        for error in self.errors:
            self.resolve_error(error)

    def read_entries(self, buffer):
        for num in range(self.num_entries):
            self.read_entry(buffer)


from abc import ABC, abstractmethod

from Buffer import Buffer
from workshop.errors.Error import Error
from workshop.errors.ErrorType import ErrorType, GenericErrors


class StrictFileFormat(ABC):
    def __init__(self, expected_size, file_enum, buffer, name, id):
        self.name = name
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

    def list_errors(self):
        if len(self.errors) > 0:
            print('%s #%i (%i errors)' % (self.name, self.id, len(self.errors)))
        for i in range(len(self.errors)):
            error = self.errors[i]
            if not error.resolved:
                print('%i: %s (%s) \"%s\"' % (i, error.enum.name, error.type.name, error.text))

    def get_errors(self):
        errors = list()
        for field in list(self.file_enum):
            if self.fields[field.value] is None:
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
            self.read_write_action(field, buffer, self.fields[field.value], read_mode=False)

        return buffer.data


class FlexibleFileFormat(ABC):
    def __init__(self, file_enum, entry_class, max_entries, name, id):
        self.name = name
        self.errors = list()
        self.id = id
        self.file_enum = file_enum
        self.entry_class = entry_class
        self.entries = list()
        self.num_entries = 0
        self.max_entries = max_entries
        self.entries_to_remove = list()


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
    def write_entry(self, buffer, entry):
        pass

    @abstractmethod
    def resolve_error(self, error):
        pass

    @abstractmethod
    def get_errors(self):
        pass

    def list_errors(self):
        if len(self.errors) > 0:
            print('%s #%i (%i errors)' % (self.name, self.id, len(self.errors)))
        for i in range(len(self.errors)):
            error = self.errors[i]
            if not error.resolved:
                print('%i: %s (%s) \"%s\"' % (i, error.enum.name, error.type.name, error.text))

    def resolve_errors(self):
        for error in self.errors:
            self.resolve_error(error)

    def read_entries(self, buffer):
        for num in range(self.num_entries):
            self.read_entry(buffer)

    def write_entries(self, buffer):
        for entry in self.entries:
            self.write_entry(buffer, entry)


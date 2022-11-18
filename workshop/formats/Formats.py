import random

from Buffer import Buffer
from workshop.errors.Error import Error
from workshop.formats.BaseFormats import StrictFileFormat, FlexibleFileFormat
from workshop.formats.FormatEnums import PersonalFields, LevelUpLearnsetFields
from workshop.errors.ErrorType import ErrorType, GenericErrors


class Personal(StrictFileFormat):
    def __init__(self, buffer, id):
        expected_size = 44
        super().__init__(expected_size, PersonalFields, buffer, id)
        # hp = buffer.read_u8()
        # atk = buffer.read_u8()
        # defence = buffer.read_u8()
        # spe = buffer.read_u8()
        # spatk = buffer.read_u8()
        # spdef = buffer.read_u8()
        # type_1 = buffer.read_u8()
        # type_2 = buffer.read_u8()
        # catch_rate = buffer.read_u8()
        # base_exp = buffer.read_u8()
        # evs = buffer.read_u16()
        # item_uncommon = buffer.read_u16()
        # item_rare = buffer.read_u16()
        # gender_ratio = buffer.read_u8()
        # hatch_multiplier = buffer.read_u8()
        # base_happiness = buffer.read_u8()
        # exp_rate = buffer.read_u8()
        # egg_group_1 = buffer.read_u8()
        # egg_group_2 = buffer.read_u8()
        # ability_1 = buffer.read_u8()
        # ability_2 = buffer.read_u8()
        # run_chance = buffer.read_u8()
        # color = buffer.read_u8()
        # tm = buffer.read_bytes(16)
        #
        # self.all = [hp, atk, defence, spe, spatk, spdef, type_1, type_2,
        #             catch_rate, base_exp, evs, item_uncommon, item_rare, gender_ratio,
        #             hatch_multiplier, base_happiness, exp_rate, egg_group_1, egg_group_2,
        #             ability_1, ability_2, run_chance, color, tm]

        self.errors = self.get_errors()

    def get_errors(self):
        errors = super().get_errors()

        if self.fields[PersonalFields.TYPE_1.value] > 17:
            errors.append(
                Error(PersonalFields.TYPE_1, ErrorType.INVALID_VALUE, "Type 1: Value greater than vanilla type limit"))
        if self.fields[PersonalFields.TYPE_2.value] > 17:
            errors.append(
                Error(PersonalFields.TYPE_2, ErrorType.INVALID_VALUE, "Type 2: Value greater than vanilla type limit"))
        if (self.fields[PersonalFields.EVS.value] >> 12) != 0:
            errors.append(Error(PersonalFields.EVS, ErrorType.INVALID_VALUE,
                                "EVs: Invalid data where there should be empty padding"))

        return errors

    def resolve_error(self, error):
        if not error.resolved:
            if error.enum == PersonalFields.EVS and error.enum == ErrorType.INVALID_VALUE:
                self.fields[PersonalFields.EVS.value] &= 0xFFF
                error.resolved = True
            else:
                for field in list(self.file_enum):
                    if error.enum == field:
                        self.fields[field] = 0

    def read_write_action(self, field, buffer, *args, read_mode):
        # read_mode is True when reading, False when writing
        if not read_mode and len(args) == 0:
            raise Exception('Invalid data provided for write mode')

        if field == PersonalFields.EVS or field == PersonalFields.ITEM_RARE or field == PersonalFields.ITEM_UNCOMMON:
            return buffer.read_u16() if read_mode else buffer.write_u16(args[0])
        elif field == PersonalFields.TMS:
            return buffer.read_bytes(16) if read_mode else buffer.write_bytes(args[0])
        else:
            return buffer.read_u8() if read_mode else buffer.write_u8(args[0])


"""
START OF LEARNSETS
"""


class LearnsetEntry:
    def __init__(self, val):
        self.move_id = val & 0x1FF
        self.level = (val >> 9) & 0x7F
        self.identifier = random.random() * 2000


def learnset_sort_helper(entry):
    return entry.level


class LevelUpLearnset(FlexibleFileFormat):
    def __init__(self, buffer, id):
        max_entries = 20
        super().__init__(LevelUpLearnsetFields, LearnsetEntry, max_entries, id)
        self.read(buffer)

    def read(self, buffer):
        buffer.seek_global(len(buffer.data) - 4)
        last = buffer.read_bytes(4)
        if last == bytearray([0xFF, 0xFF, 0, 0]):
            self.num_entries = int((len(buffer.data) - 4) / 2)
        else:
            buffer.seek_global(len(buffer.data) - 2)
            last = buffer.read_bytes(2)
            if last == bytearray([0xFF, 0xFF]):
                self.num_entries = int((len(buffer.data) - 2) / 2)
            else:
                self.num_entries = int(len(buffer.data) / 2)
                self.errors.append(
                    Error(GenericErrors.MISSING_TERMINATOR, ErrorType.DATA_MISSING, "Missing terminator", resolved=True))

        if self.num_entries > self.max_entries:
            self.num_entries = self.max_entries
            self.errors.append(
                Error(GenericErrors.INVALID_ENTRY_AMOUNT, ErrorType.INVALID_VALUE, "Too many entries", resolved=True))

        buffer.seek_global(0)
        self.read_entries(buffer)

    def read_entry(self, buffer):
        self.entries.append(LearnsetEntry(self.read_write_action(None, buffer, read_mode=True)))

    def read_write_action(self, field, buffer, *args, read_mode):
        if not read_mode and len(args) == 0:
            raise Exception('Invalid data provided for write mode')

        if read_mode:
            return buffer.read_u16()
        else:
            buffer.write_u16(args[0])

    def write(self):
        size = self.num_entries * 2
        if self.num_entries % 2 == 0:
            size += 4
        else:
            size += 2

        buffer = Buffer(bytearray(size), write=True)
        self.write_entries(buffer)

        if self.num_entries % 2 == 0:
            buffer.write_bytes([0xFF, 0xFF, 0, 0])
        else:
            buffer.write_bytes([0xFF, 0xFF])

        return buffer.data

    def write_entry(self, buffer, entry):
        value = ((entry.level & 0x7f) << 9) | (entry.move_id & 0x1ff)
        self.read_write_action(None, buffer, value, read_mode=False)

    def get_errors(self):
        levels = []
        for entry in self.entries:
            levels.append(entry.level)
            if entry.move_id > 467:
                self.errors.append(
                    Error(LevelUpLearnsetFields.MOVE_ID, ErrorType.INVALID_VALUE, "Invalid move id: %s" % entry.move_id,
                          entry.identifier))
            if entry.level > 100:
                self.errors.append(
                    Error(LevelUpLearnsetFields.LEVEL, ErrorType.INVALID_VALUE, "Invalid level: %s" % entry.level,
                          entry.identifier))
            for level in levels:
                if level > entry.level:
                    self.errors.append(
                        Error(GenericErrors.INVALID_SORTING, ErrorType.INVALID_VALUE, "Invalid sort", entry.identifier))

    def resolve_error(self, error):
        if not error.resolved:
            if error.enum == GenericErrors.INVALID_ENTRY_AMOUNT and self.num_entries > self.max_entries:
                self.num_entries = self.max_entries
                while len(self.entries) != self.num_entries:
                    self.entries.pop(len(self.entries - 1))
                error.resolved = True
            elif error.enum == LevelUpLearnsetFields.MOVE_ID:
                for entry in self.entries:
                    if entry.identifier == error.instructions:
                        self.entries.remove(entry)
                        error.resolved = True
                        break
            elif error.enum == LevelUpLearnsetFields.LEVEL:
                for entry in self.entries:
                    if entry.identifier == error.instructions:
                        entry.level = 100
                        error.resolved = True
                        break
            elif error.enum == GenericErrors.INVALID_SORTING:
                self.entries.sort(key=learnset_sort_helper)
                error.resolved = True

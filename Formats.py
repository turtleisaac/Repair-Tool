from Buffer import Buffer
from Error import Error
from FileFormat import FileFormat
from FormatEnums import PersonalFields
from ErrorType import ErrorType, GenericErrors


class Personal(FileFormat):
    def __init__(self, buffer, id):
        expected_size = 44
        super().__init__(expected_size, PersonalFields, id)

        if len(buffer) > self.expected_size:
            self.errors.append(Error(GenericErrors.INVALID_FILE_LENGTH, ErrorType.INVALID_VALUE, "File has extra data"))
        else:  # len <= 44
            for field in list(self.file_enum):
                self.all.append(self.read_write_instructions(field, buffer, read_mode=True))
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

        self.id = id
        self.errors = self.get_errors()

    def get_errors(self):
        errors = super().get_errors()

        if self.all[PersonalFields.TYPE_1.value] > 17:
            errors.append(Error(PersonalFields.TYPE_1, ErrorType.INVALID_VALUE, "Type 1: Value greater than vanilla type limit"))
        if self.all[PersonalFields.TYPE_2.value] > 17:
            errors.append(Error(PersonalFields.TYPE_2, ErrorType.INVALID_VALUE, "Type 2: Value greater than vanilla type limit"))
        if (self.all[PersonalFields.EVS.value] >> 12) != 0:
            errors.append(Error(PersonalFields.EVS, ErrorType.INVALID_VALUE, "EVs: Invalid data where there should be empty padding"))

        return errors

    def resolve_error(self, error):
        for field in list(self.file_enum):
            if error.enum == field:
                # if self.
                pass

    def read_write_instructions(self, field, buffer, read_mode, *args):
        # read_mode is True when reading, False when writing
        if field == PersonalFields.EVS or field == PersonalFields.ITEM_RARE or field == PersonalFields.ITEM_UNCOMMON:
            return buffer.read_u16() if read_mode else buffer.write_u16(args[0])
        elif field == PersonalFields.TMS:
            return buffer.read_bytes(16) if read_mode else buffer.write_bytes(args[0])
        else:
            return buffer.read_u8() if read_mode else buffer.write_u8(args[0])


    def write(self):
        buffer = Buffer(bytearray(self.expected_size), write=True)

        # buffer.write_u8(self.hp)
        # buffer.write_u8(self.atk)
        # buffer.write_u8(self.defence)
        # buffer.write_u8(self.spe)
        # buffer.write_u8(self.spatk)
        # buffer.write_u8(self.spdef)
        # buffer.write_u8(self.type_1)
        # buffer.write_u8(self.type_2)
        # buffer.write_u8(self.catch_rate)
        # buffer.write_u8(self.base_exp)
        # buffer.write_u16(self.evs)
        # buffer.write_u16(self.item_uncommon)
        # buffer.write_u16(self.item_rare)
        # buffer.write_u8(self.gender_ratio)
        # buffer.write_u8(self.hatch_multiplier)
        # buffer.write_u8(self.base_happiness)
        # buffer.write_u8(self.exp_rate)
        # buffer.write_u8(self.egg_group_1)
        # buffer.write_u8(self.egg_group_2)
        # buffer.write_u8(self.ability_1)
        # buffer.write_u8(self.ability_2)
        # buffer.write_u8(self.run_chance)
        # buffer.write_u8(self.color)
        # buffer.write_bytes(self.tm)

        return buffer.data



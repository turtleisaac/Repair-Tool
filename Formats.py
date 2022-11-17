class Personal:
    def __init__(self, buffer, id):
        self.errors = list()
        if len(buffer) > 44:
            self.errors.append("File has extra data")
        else:  # len <= 44
            self.hp = buffer.read_u8()
            self.atk = buffer.read_u8()
            self.defence = buffer.read_u8()
            self.spe = buffer.read_u8()
            self.spatk = buffer.read_u8()
            self.spdef = buffer.read_u8()
            self.type_1 = buffer.read_u8()
            self.type_2 = buffer.read_u8()
            self.catch_rate = buffer.read_u8()
            self.base_exp = buffer.read_u8()
            self.evs = buffer.read_u16()
            self.item_uncommon = buffer.read_u16()
            self.item_rare = buffer.read_u16()
            self.gender_ratio = buffer.read_u8()
            self.hatch_multiplier = buffer.read_u8()
            self.base_happiness = buffer.read_u8()
            self.exp_rate = buffer.read_u8()
            self.egg_group_1 = buffer.read_u8()
            self.egg_group_2 = buffer.read_u8()
            self.ability_1 = buffer.read_u8()
            self.ability_2 = buffer.read_u8()
            self.run_chance = buffer.read_u8()
            self.color = buffer.read_u8()
            self.tm = buffer.read_bytes(16)

        self.id = id

    # def list_errors:



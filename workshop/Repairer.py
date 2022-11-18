import ndspy.rom
import ndspy.narc

class Repairer:
    def __init__(self, rom_path):
        self.rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
        self.game_code = self.rom.idCode

    def repair(self):
        pass
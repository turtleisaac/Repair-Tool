import ndspy.rom
import ndspy.narc

from Buffer import Buffer
from workshop.formats.Formats import Personal, LevelUpLearnset, Evolutions


class Repairer:
    def __init__(self, rom_path):
        self.rom = ndspy.rom.NintendoDSRom.fromFile(rom_path)
        self.game_code = self.rom.idCode

        self.valid = True
        if self.game_code != b'CPUE' and self.game_code != b'IPKE' and self.game_code != b'IPGE':
            self.valid = False
            return
        elif self.game_code == b'CPUE':
            self.personal_path = '/poketool/personal/pl_personal.narc'
            self.learnsets_path = '/poketool/personal/wotbl.narc'
            self.evolutions_path = '/poketool/personal/evo.narc'
        elif self.game_code == b'IPKE':
            self.personal_path = '/a/0/0/2'
            self.learnsets_path = '/a/0/3/3'
            self.evolutions_path = '/a/0/3/4'
        self.personal_narc = ndspy.narc.NARC(self.rom.getFileByName(self.personal_path))
        self.learnsets_narc = ndspy.narc.NARC(self.rom.getFileByName(self.learnsets_path))
        self.evolutions_narc = ndspy.narc.NARC(self.rom.getFileByName(self.evolutions_path))

    def repair(self):
        if not self.valid:
            return

        for i in range(len(self.personal_narc.files)):
            entry = Personal(Buffer(self.personal_narc.files[i]), i)
            entry.list_errors()
            entry.resolve_errors()
            self.personal_narc.files[i] = entry.write()
        print('---Personal End---')

        for i in range(len(self.learnsets_narc.files)):
            entry = LevelUpLearnset(Buffer(self.learnsets_narc.files[i]), i)
            entry.list_errors()
            entry.resolve_errors()
            self.learnsets_narc.files[i] = entry.write()
        print('---Level-Up Learnsets End---')

        for i in range(len(self.evolutions_narc.files)):
            entry = Evolutions(Buffer(self.evolutions_narc.files[i]), i)
            entry.list_errors()
            entry.resolve_errors()
            self.evolutions_narc.files[i] = entry.write()
        print('---Evolutions End---')

        print('-----All programmed formats parsed, Program End-----')

    def write(self, output_path):
        self.rom.setFileByName(self.personal_path, self.personal_narc.save())
        self.rom.setFileByName(self.learnsets_path, self.learnsets_narc.save())
        self.rom.setFileByName(self.evolutions_path, self.evolutions_narc.save())
        self.rom.saveToFile(output_path)


if __name__ == "__main__":
    repairer = Repairer("../RenPlat_Repaired.nds")
    repairer.repair()

from .constants import game_file, data_file
from .directory_entry import DirectoryEntry
from typing import List

class VmuFile:
    def __init__(self, all_blocks, block_refs, dir_entry: DirectoryEntry):
        self.blocks: List[bytearray] = []
        self.dir_entry = dir_entry
        self.is_valid = True
        self.is_japanese = False

        for block_ref in block_refs:
            self.blocks.append(all_blocks[block_ref])

        self.is_game = dir_entry.file_type == game_file
        self.is_data = dir_entry.file_type == data_file

        try:
            self.desc = self.blocks[dir_entry.header_offset][0:16].decode('ascii')
            if(str(dir_entry.file_name) != "ICONDATA_VMS"):
                self.desc_long = self.blocks[dir_entry.header_offset][16:48].decode('ascii')
                self.application = self.blocks[dir_entry.header_offset][48:64].decode('ascii')
        except:
            # Some Japanese games not encoded with ASCII, can be used to identify Japanese saves?
            try:
                self.desc = self.blocks[dir_entry.header_offset][0:16].decode('shift_jis')
                if(str(dir_entry.file_name) != "ICONDATA_VMS"):
                    self.desc_long = self.blocks[dir_entry.header_offset][16:48].decode('shift_jis')
                    self.application = self.blocks[dir_entry.header_offset][48:64].decode('shift_jis')
                self.is_japanese = True
            except:
                self.is_valid = False
        self.num_blocks = len(self.blocks)
        # desc/desc_long padded with spaces so .strip() to remove whitespace, application padded with \x00 so .rstrip("\x00") to remove whitespace
        # 64:66 Number of Icons
        # 66:68 Icon animation speed
        # 68:70 Graphic Eyecatch Type
        # 70:72 CRC
        self.crc = self.blocks[dir_entry.header_offset][70:72]
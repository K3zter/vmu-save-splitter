from .directory_entry import DirectoryEntry
from .constants import block_size

directory_entry_size = 32
zero_byte_array = bytearray(directory_entry_size)
entries_per_block = int(block_size / directory_entry_size)

class Directory:
    def __init__(self, blocks, root):
        self.entries = []
        dir_start = root.dir_location
        dir_end = root.dir_location - root.dir_size

        for i in range(dir_start, dir_end, -1):
            for j in range(0, entries_per_block):
                block_start = j * directory_entry_size
                block_end = block_start + directory_entry_size
                self.entries.append(blocks[i][block_start:block_end])
                
        self.start = dir_start
        self.end = dir_end

    def get_first_empty(self):
        for index, entry in enumerate(self.entries):
            if(entry == zero_byte_array):
                return index

    def get_entry(self, index: int):
        return DirectoryEntry(self.entries[index], index)
    
    def add_entry(self, entry: DirectoryEntry):
        index = self.get_first_empty()
        self.entries[index] = entry.to_bytes()

    def to_blocks(self):
        blocks = []
        dir_size = self.start - self.end
        for i in range(0, dir_size):
            block_data = bytearray(0)
            for j in range(0, entries_per_block):
                current_entry = i * entries_per_block + j
                block_data += self.entries[current_entry]

            blocks.append(block_data)
        return blocks
            
     
    def files(self) -> list[DirectoryEntry]:
        entries = self.entries

        files = []
        for index, entry in enumerate(entries):
            if entry != zero_byte_array:
                entry_object = DirectoryEntry(entry, index)
                files.append(entry_object)

        return files

    def list(self):
        entries = self.entries

        table_line = "+-------+----------------+--------+-----+"

        print(table_line)
        print("| Index | Name           | Blocks | 1st |")
        print(table_line)

        for index, entry in enumerate(entries):
            if entry != zero_byte_array:
                entry_object = DirectoryEntry(entry, index)
                print("| " + str(index).ljust(6) + "| " + entry_object.file_name.ljust(15)  + "| " + f"{str(entry_object.num_blocks):<7}" + "| " + str(entry_object.first_block).ljust(4) + "|")

        print(table_line)

    def file_exists(self, file_name):
        for index, entry in enumerate(self.entries):
            if entry != zero_byte_array:
                entry_object = DirectoryEntry(entry, index)
                if(entry_object.file_name == file_name):
                    return True

        return False
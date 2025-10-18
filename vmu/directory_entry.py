import datetime

def bcd_decode(data: bytes, decimals: int):
    '''
    Decode BCD number
    '''
    res = 0
    for n, b in enumerate(reversed(data)):
        res += (b & 0x0F) * 10 ** (n * 2 - decimals)
        res += (b >> 4) * 10 ** (n * 2 + 1 - decimals)
    return res

def parse_date(date_sequence):
    try:
        year = bcd_decode(date_sequence[0:2], 0)
        month = bcd_decode(date_sequence[2:3], 0)
        day = bcd_decode(date_sequence[3:4], 0)
        hour = bcd_decode(date_sequence[4:5], 0)
        minute = bcd_decode(date_sequence[5:6], 0)
        second = bcd_decode(date_sequence[6:7], 0)

        return datetime.datetime(year, month, day, hour, minute, second)
    except:
        return None

class DirectoryEntry:
    def __init__(self, data, index):
        self.index = index
        self.file_type = data[0:1]
        self.copy_protect = data[1:2]
        self.first_block = int.from_bytes(data[2:4], "little")
        self.decode_file_name(data)
        self.bcd_created = data[16:24]
        self.created = parse_date(self.bcd_created)
        self.num_blocks = int.from_bytes(data[24:26], "little")
        self.header_offset = int.from_bytes(data[26:28], "little")

    def decode_file_name(self, data):
        self.file_name=""
        for i in range(4,16,1):
            try:
                char = data[i:i+1].decode("ascii")
                self.file_name += char
            except:
                self.file_name += "?"

    def to_bytes(self):
        data = bytearray(0)
        data += self.file_type
        data += self.copy_protect
        data += self.first_block.to_bytes(2, "little")
        data += self.file_name.encode("ascii")
        data += self.bcd_created
        data += self.num_blocks.to_bytes(2, "little")
        data += self.header_offset.to_bytes(2, "little")
        data += bytearray(4)

        return data
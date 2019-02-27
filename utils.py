import struct
from sys import argv

LUA_LONG_STR_LENGTH = 254
LUA_NIL = 0
LUA_BOOLEAN = 1
LUA_NUMBER = 3
LUA_INTEGER = 19
LUA_SHORT_STR = 4
LUA_LONG_STR = 20


class StructField:
    def __init__(self, format, offset):
        self.format = format
        self.offset = offset

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            r = struct.unpack_from(self.format, instance._buffer, self.offset)
            return r[0] if len(r) == 1 else r


class StructureMeta(type):
    def __init__(self, clsname, bases, clsdict):
        fields = getattr(self, '_fields_', [])
        byte_order = ''
        offset = 0
        for format, fieldname in fields:
            if format.startswith(('<', '>', '!', '@')):
                byte_order = format[0]
                format = format[1:]
            format = byte_order + format
            setattr(self, fieldname, StructField(format, offset))
            offset += struct.calcsize(format)
        setattr(self, 'struct_size', offset)


class Structure(metaclass=StructureMeta):
    def __init__(self, bytedata):
        self._buffer = bytedata

    @classmethod
    def from_file(cls, f):
        return cls(f.read(cls.struct_size))


class SizedRecord:
    def __init__(self, bytedata, item_fmt):
        self._buffer = memoryview(bytedata)
        self._item_fmt = item_fmt

    @classmethod
    def readString(cls, f, size_fmt, item_fmt: str, includes_size=True):
        sz_nbytes = struct.calcsize(size_fmt)
        sz_item_fmt = struct.calcsize(item_fmt)
        sz_bytes = f.read(sz_nbytes)
        sz, = struct.unpack(size_fmt, sz_bytes)
        if sz == LUA_NIL:
            return ''
        elif sz == LUA_LONG_STR_LENGTH:
            sz = readValue('=d')
        buf = f.read(sz * sz_item_fmt - includes_size * sz_nbytes)
        return cls(buf, item_fmt)

    @classmethod
    def from_file(cls, f, size_fmt: str, item_fmt: str, includes_size=True):
        sz_nbytes = struct.calcsize(size_fmt)
        sz_item_fmt = struct.calcsize(item_fmt)
        sz_bytes = f.read(sz_nbytes)
        sz, = struct.unpack(size_fmt, sz_bytes)
        buf = f.read(sz * sz_item_fmt - includes_size * sz_nbytes)
        return cls(buf, item_fmt)

    def iter(self):
        if isinstance(self._item_fmt, str):
            s = struct.Struct(self._item_fmt)
            for off in range(0, len(self._buffer), s.size):
                yield s.unpack_from(self._buffer, off)
        elif isinstance(self._item_fmt, StructureMeta):
            size = self._item_fmt.struct_size
            for off in range(0, len(self._buffer), size):
                data = self._buffer[off:off + size]
                yield self._item_fmt(data)


class LuaHeader(Structure):
    _fields_ = [
        ('=4s', 'sig'),
        ('c', 'version'),
        ('c', 'form'),
        ('6s', 'luac_Data'),
        ('c', 'cintSize'),
        ('c', 'sizetSize'),
        ('c', 'instructSize'),
        ('c', 'luaIntSize'),
        ('c', 'luaNumSize'),
        ('q', 'luac_Int'),
        ('d', 'luac_Float')
    ]


def readValue(f, fmt: str, num: int = 0):
    if num is 0:
        r = struct.unpack_from(fmt, f.read(struct.calcsize(fmt)), 0)
        return r[0] if len(r) == 1 else r
    elif num > 0:
        return (struct.unpack_from(fmt, f.read(struct.calcsize(fmt)), 0)[0] for i in range(num))
    else:
        raise IndexError('num must >= 0')


if __name__ == '__main__':
    if len(argv) < 2:
        raise AssertionError('not enough parameter')
    elif len(argv) == 2:
        f = open(argv[1], 'rb')
        phead = LuaHeader.from_file(f)
        readValue(f, '=B')
        source_name_record = SizedRecord.readString(f, '=B', '=c')
        source_name = "".join([bytes.decode(i[0]) for i in source_name_record.iter()])
        line_def, last_line_def = readValue(f, '=I', 2)
        numParms = readValue(f, '=B')
        isVararg = readValue(f, '=?')
        maxStackSize = readValue(f, '=B')
        code_num_record = SizedRecord.from_file(f, '=I', '=I', includes_size=False)
        code = [i[0] for i in code_num_record.iter()]

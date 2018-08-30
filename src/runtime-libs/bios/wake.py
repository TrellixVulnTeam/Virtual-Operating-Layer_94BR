"""The First function within the bios boot.
The BIOS memoory is first assigned using a given hard-coded key.

Once assigned the wak _produces_ a memory allocation and assigns the first
key values to the BIOS memory slot.

The POST commands are read and the instructions load the next memory
slots for the enviroment.

    Open Mmap volatile TAPE.

        Any middleman information for the TAPE should write here. Such as
        bios RAM encryption layers.

    COLD or WARM boot.
    Write a print function.
    clean open space
    load memory references
    load base lib
    load memory config
    load state

BIOS RAM STATE
    0   unallocated / not installed
        Nothing in the ram, no protection mode, no instructions.

"""

import sys, builtins
import mmap, os
import time

TAPE_EXISTS = -1
TAPE_MISSING = -2
BEEP = "\x07"


HEADER = { 'debug': None }


def c_mem_clear(string):
    import ctypes
    location = id(string) + 20
    size     = sys.getsizeof(string) - 20
    ''' msvcrt
        fclose
        fopen
        freopen
        fwrite
        kbhit
        memcmp
        memcpy
        memmove
        memset
        rand
        scanf
        sprintf
        srand
        system
        time
    '''
    memset =  ctypes.cdll.msvcrt.memset
    # For Linux, use the following. Change the 6 to whatever it is on your computer.
    # memset =  ctypes.CDLL("libc.so.6").memset

    puts( "Clearing 0x%08x size %i bytes" % (location, size))

    memset(location, 0, size)


puts = getattr(__builtins__, 'print')

class IO:

    def __init__(self):
        print('wake IO')
        self.record_io()

    def record_io(self, root_fileno=100):
        io_d = dict()

        _found_atty = False
        print('Recording IO')
        for _fileno in range(0, root_fileno + 1):
            try:
                io_d[_fileno] = (os.isatty(_fileno), os.stat(_fileno), )
            except OSError:
                break
        stdio = (sys.stdin, sys.stdout, sys.stderr,)
        print('discovered {} BASE IO'.format(len(io_d)))

        writable = dict()
        print('Testing for Output')
        for io in stdio:

            if io.writable() is False:
                continue

            iof = io.fileno()
            #print('discovered', iof, io.name)
            iodo = io_d[iof]
            writable[iof] = io

            #print('discovered', iof, io.name, 'isatty', iodo[0])
            if ('out' in io.name) and (iodo[0] is True):
                #print('Found IO out hook item', iodo[1])
                self.hook(io, iodo[1])
                _found_atty = True

        if _found_atty is False:
            print('Attempting any IO Hook')
            for num in writable:
                item = writable[num]
                # print('Looking at', item, sys.stdout)
                if  sys.stdout == item:
                    iodo = io_d[item.fileno()]
                    self.hook(item, iodo[1])
                _found_atty = True


    def hook(self, stdio, stat):
        global puts
        self.stdout = stdio
        puts = self.print_hook# self.stdout.write
        puts(BEEP + 'Hello Spoon')

    def print_hook(self, *a, newline=None, level=1):
        if HEADER['debug'] is False and level > 1:
            # silence
            return

        self.stdout.write(' '.join(map(str, a)) + '\n')


class BIOS_TAPE:
    """Read a tape an execute functionality"""

    def __init__(self):
        """In an expected env:
            0  readable
        """
        self.uuid_radix_name = 'a8e46d52-d125-4cb6-8f6e-c84b0ce25e8c'
        print('testing path with')
        _os = os
        print('OS', _os)
        _path = os.path
        print('path', _path)
        _exists = os.path.exists
        print('exists', _exists)
        print('uuid', self.uuid_radix_name)
        try:

            pr = _exists(self.uuid_radix_name)
            print('Function: {}'.format(pr))
        except Exception as e:
            print('An error {}'.format(e))
            pr = False
        print('New Tape')

        if pr is False:

            print('No Root Tape in fileno:', self.uuid_radix_name)
            self.new_tape()
            time.sleep(.3)

        print('Complete existence of', self.uuid_radix_name)

        root_tape, fileno = self.init_tape()

        if root_tape is False:
            puts('Created new tape')
            root_tape, fileno = self.init_tape()
            puts('New tape', root_tape, fileno)

        if root_tape is False:
            puts('!! No BIOS Tape.')

        self.tape_data = self.read_tape(fileno)

    def init_tape(self):
        """Open the existing tape if available, returning (boolean, fileno)"""
        print( 'ATTEMPT BIOS_TAPE', self.uuid_radix_name, 'with 32914')
        fileno = self.open(self.uuid_radix_name, 32914)
        print('TAPE fileno', fileno)
        # return if BIOS Tape file exists at the gven location,
        # this should load for instructions
        return fileno != TAPE_MISSING, fileno

    def open(self, tape_id, access_id):
        """Open a file descriptor to the HOST RAM given a tape_id to
        assist compilation of the data asset
        """

        # Open bios tape at current source location (ugly.)
        # and read the input strategy.
        try:
            puts('Opening', tape_id, 'with access', access_id)
            bios_tape_stream = os.open(tape_id, access_id)
            return bios_tape_stream
        except FileNotFoundError:
            puts('Tape missing')
            return TAPE_MISSING
        except Exception as e:
            puts('!! Catastrophic failure with bios tape', str(e))
            return TAPE_MISSING

    def new_tape(self):
        """Produce a new BIOD RAM tape using the given ID. The mandatory BIOS
        inatructions are measured and set. A new tape is saved.

        Return the tape fileno

        This is a byte array for file access loadout"""
        puts('Creating new bios tape with 34193')
        try:
            vv = os.O_RDWR|os.O_RANDOM|os.O_BINARY|os.O_CREAT

            fileno = os.open(self.uuid_radix_name, vv)# mode='wb')
        except Exception as e:
            puts('Error with open', str(e))
            fileno = -2

        if fileno < 1:
            return False

        if os.path.exists(self.uuid_radix_name) is False:
            puts(BEEP + 'ERROR: Cannot produce BIOS Tape.')
            # sys.exit(1)

        puts('New Tape', fileno)
        self.write_new_tape(fileno)
        os.close(fileno)

    def read_tape(self, fileno):
        """Read in a bios tape and configure"""

        os.lseek(fileno, 0, 0)
        # Read as much as needed to capture the first
        # word within the string.
        first = os.read(fileno, 10)

        if len(first) == 0:
            puts('Corrupt tape. Delete => Renew')
            self.write_new_tape(fileno)
            time.sleep(.2)
            os.lseek(fileno, 0, 0)
            first = os.read(fileno, 10)

        puts('Inspecting:', first)
        size = ()
        for byte in first:
            # Capture first space
            if byte == 32:
                break
            size += (byte,)
        # string to int of bytes for the next cut
        puts('Reading tape size', size, 'of', first)
        incoming_bytes_len = int(bytes(size))
        puts('Bytes', incoming_bytes_len)

        os.lseek(fileno, 0, 0)
        bios_stamp = os.read(fileno, incoming_bytes_len)
        # remove the size header and [space]
        bios_stamp = bios_stamp[len(size) + 1:]
        result = {}

        # First byte
        result['wake_state'] = int(bytes([bios_stamp[0]]))
        # second byte.
        result['output_fd'] = int(bytes([bios_stamp[1]]))
        # 16 bytes for id
        result['uuid'] = bytes(bios_stamp[2:18])
        # Anything else is the version string
        result['version'] = bios_stamp[20:].decode('utf')

        #puts('bios_stamp:', bios_stamp)
        puts('wake_state:', result['wake_state'])
        puts('output_fd: ', result['output_fd'])
        puts('uuid:      ', result['uuid'])
        puts('version:   ', result['version'])

        result['lib_names'] = self.get_lib(fileno, incoming_bytes_len)
        puts('importing: ', result['lib_names'])
        return result

    def get_lib(self, fileno, init_byte):
        os.lseek(fileno, init_byte, 0)
        first = os.read(fileno, 10)

        size = ()
        for byte in first:
            # Capture first space
            if byte == 32:
                break
            size += (byte,)
        # string to int of bytes for the next cut
        incoming_bytes_len = int(bytes(size))

        os.lseek(fileno, init_byte + 1 + len(size), 0)
        lib_bytes = os.read(fileno, incoming_bytes_len)
        lib_splits = lib_bytes.decode('utf')
        return lib_splits.split('|')

    def write_new_tape(self, fileno):
        """write a new tape into the given tape fileno."""

        puts('Writing new tape')
        write = os.write
        lines = ()
        # vol phase state.
        lines += (b'0', )
        # Address pointer of the the ram file.
        # Booting in the same env this should be the same every time.
        lines += (bytes(str(fileno), 'utf'), )
        # 16 byte given uuid of the BIOS - templated in.
        lines += (b'\xa8\xe4mR\xd1%L\xb6\x8fn\xc8K\x0c\xe2^\x8c', )
        # selected kernel
        kernel_version = b"Kerbechet-(0, 0, 1)"
        # The amount of bytes for a pointer when reading the kernel string.
        lines += (bytes(str(len(kernel_version)), 'utf'), )
        lines += (kernel_version, )

        # write in STDOUT fileno
        total = sum(map(len, lines))
        len_total = len(bytes(str(total), 'utf'))
        total += len_total + 1
        os.write(fileno,  bytes("{} ".format( str(total)), 'utf') )

        # os.write(b'\x00')
        for bv in lines:
            os.write(fileno, bv)

        os.lseek(fileno, 0, 0)
        read_t = int(os.read(fileno, 2))
        assert total == read_t

        # Write a version string
        os.lseek(fileno, total - len(kernel_version), 0)
        read_kernel = os.read(fileno, len(kernel_version))
        assert read_kernel == kernel_version

        puts('Writing libs')
        os.lseek(fileno, total, 0)
        libline = bytes("|".join(list(('bios_os',))), 'utf')
        #os.write(fileno, bytes(str(len(libline)), 'utf'))
        os.write(fileno,  bytes("{} ".format( len(libline)), 'utf') )
        os.write(fileno, libline)
        puts('Complete')


class Tape(BIOS_TAPE):
    pass


"""A new ram tape file has:
    state   int for vol wakeup
    pointer - the filedescriptor pointer - stored and verified later
    uuid - For verification
    kernel -
"""

import marshal


class Config:

    def find(self):
        if os.path.exists('HEADER'):
            puts('discovered configure "HEADER"')
            data = self.read('HEADER')
            return data

    def write(self, value):
        vv=compile('{}\n'.format(value), 'HEADER', 'eval')
        ff=open('HEADER', 'wb')
        marshal.dump(vv, ff)
        ff.close()

    def read(self, name):
        stream = open(name, 'rb')
        br = b''
        for line in stream.readlines():
            br += line
        result = eval(marshal.loads(br))
        stream.close()
        return result




def WAKE():
    global tape
    global HEADER

    io = IO()
    config = Config()
    # tape = BIOS_TAPE()
    HEADER = config.find()
    puts('WAKE')

# Import cold or warm state.

WAKE()
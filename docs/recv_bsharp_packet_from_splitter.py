import struct
import socket
import time
import select
import sys

def flush_readable(readable):

    read_list = [readable]
    write_list = []
    err_list = []

    while True:
        main_buf, writables, errored = select.select(read_list, write_list, err_list, 0.001)
        if len(main_buf) == 0:
            return
        else:
            junk_data = main_buf[0].recv(4096)

def read_n(readable, n):
    byte_buffer = b''
    total_read = 0
    
    while total_read < n:
        curr_buffer = readable.recv(n-total_read)
        curr_read = len(curr_buffer)
        byte_buffer = byte_buffer+curr_buffer
        total_read = total_read + curr_read

    return byte_buffer

BSHARP_ADDR = '127.0.0.1'
BSHARP_PORT = 13002

bsharp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bsharp_socket.connect((BSHARP_ADDR, BSHARP_PORT))

print("Connected to {}", BSHARP_ADDR)

error_line = "No errors"
status_line_template = "Frame #: {: 10d} Length: {: 6d} # Reads: {: 4d} Status: 0x{:08x} Ch1: 0x{: 11d} Check: 0x{:02x}";

socket_flush_count = 0
frame_num = 0;
status = 0
num_read = 0
length_val = 0
chan_1_data = 0
checksum_val = 0
while True:
    error_code = 0
    error_line = "No errors"
    cmd_buffer = read_n(bsharp_socket, 2)

    if (error_code == 0):
        if cmd_buffer != b'B\x01':
            error_code = 1
            socket_flush_count = socket_flush_count + 1
            error_line = "Invalid data header.  Flushing buffer. Flush count: {:10d}".format(socket_flush_count)
            flush_readable(bsharp_socket)

    if (error_code == 0):
        length_bytes = read_n(bsharp_socket, 2)
        length_val, = struct.unpack('>h', length_bytes)

    if (error_code == 0):
        payload_bytes = read_n(bsharp_socket, length_val-1)
        checksum_bytes = read_n(bsharp_socket, 1)

        frame_num, status, num_read = struct.unpack('>III', payload_bytes[:12])
        chan_1_data, = struct.unpack('>I', payload_bytes[12:16])
        if checksum_bytes != b'*':
            error_code = 2
            error_line = "Invalid checksum"

        checksum_val, = struct.unpack('B', checksum_bytes)

    # Time to print out statuses
    sys.stdout.write("\033[2F")
    sys.stdout.write(error_line)
    sys.stdout.write("\033[1E")
    out_status_line = status_line_template.format(frame_num, length_val, num_read, status, chan_1_data, checksum_val);
    sys.stdout.write(out_status_line)
    sys.stdout.flush()

    
        

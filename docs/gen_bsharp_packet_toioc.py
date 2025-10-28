import struct
import socket
import time
import random

header_bytes = b'B\x01'
len_bytes = struct.pack('>h',4109)
read_data = b'0'*4096
end_byte = b'*'
random.seed(1)

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(('', 13002))
my_socket.listen(5)

(cli_sock, cli_addr) = my_socket.accept()

frame_num = -1
frame_val = 0
while True:
    frame_num = frame_num+1
    frame_val = frame_val+2000
    if (frame_val > 500000):
        frame_val = 2000
    read_array = []
    read_bytes = b''
    for read_idx in range(1024):
        curr_read_val = frame_val + read_idx
        curr_read_bytes = struct.pack('>I', curr_read_val)
        read_bytes = read_bytes + curr_read_bytes
    read_data = read_bytes
    payload_bytes = struct.pack('>III', frame_num, 0, 256)
    payload_array = payload_bytes + read_data
    full_packet = header_bytes+len_bytes+payload_array+end_byte
    cli_sock.send(full_packet)
    time.sleep(0.05)

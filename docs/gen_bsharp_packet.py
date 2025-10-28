import struct
import socket
import time
import random

header_bytes = b'bb1>B\x01'
len_bytes = struct.pack('>h',4109)
read_data = b'0'*4096
end_byte = b'*'
random.seed(1)

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(('127.0.0.1', 13000))
my_socket.listen(5)

(cli_sock, cli_addr) = my_socket.accept()

frame_num = -1
while True:
    frame_num = frame_num+1
    read_data = random.randbytes(4096)
    payload_bytes = struct.pack('>III', frame_num, 0, 256)
    payload_array = payload_bytes + read_data
    full_packet = header_bytes+len_bytes+payload_array+end_byte
    cli_sock.send(full_packet)
    time.sleep(0.02)

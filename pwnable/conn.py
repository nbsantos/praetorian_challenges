import binascii
import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 2888))
try:
    s.recv(4096)
    s.recv(4096)
except:
    pass
s.sendall(b'A' * 400)
res = s.recv(4096)


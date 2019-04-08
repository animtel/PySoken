import ctypes
import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# result = sock.connect_ex(('127.0.0.1',1234))
# print(ctypes.windll.shell32.IsUserAnAdmin())
# if result == 0:
#    print ("Port is open")
# else:
#    print ("Port is not open")
# sock.close()

import socket

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 5000              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('test')
    s.listen(1)
    print('test')
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
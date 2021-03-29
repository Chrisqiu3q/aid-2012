"""
http
"""
from socket import *

sock = socket()
sock.bind(("0.0.0.0", 9527))
sock.listen(5)

connfd, addr = sock.accept()
print("Connect from", addr)

data = connfd.recv(1024)
print(data.decode())

response = """HTTP/1.1 200 OK
Content-Type:text/html

Hello Word
"""
connfd.send(response.encode())

connfd.close()
sock.close()

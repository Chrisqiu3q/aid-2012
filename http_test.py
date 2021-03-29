"""
http请求响应 演示
"""
from socket import *

sock = socket()
sock.bind(("0.0.0.0",8888))
sock.listen(5)

# 接收浏览器连接请求
connfd,addr = sock.accept()
print("Connect from",addr)

# 接收到了浏览器发送的http请求
request = connfd.recv(1024)
print(request.decode())

# 组织ｈｔｔｐ响应格式
response = """HTTP/1.1 200 OK
Content-Type:text/html

Hello World
"""
#　发送给浏览器
connfd.send(response.encode())

connfd.close()
sock.close()
from socket import *
from select import select


class WebServer:
    def __init__(self, host="", port=8000, html=None):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.html = html
        self._rlist = []
        self.sock = self._create_socket()

    def _create_socket(self):
        sock = socket()
        sock.bind(self.address)
        sock.setblocking(False)
        return sock

    def _connect(self):
        connfd, addr = self.sock.accept()
        connfd.setblocking(False)
        self._rlist.append(connfd)

    def start(self):
        self.sock.listen(5)
        print("Listen the port%d" % self.port)
        self._rlist.append(self.sock)
        while True:
            rs, ws, xs = select(self._rlist, [], [])
            for r in rs:
                if r is self.sock:
                    self._connect()
                else:
                    try:
                        self._handle(r)
                    except Exception as e:
                        print(e)
                    finally:
                        self._rlist.remove(r)
                        r.close()

    def _handle(self, connfd):
        request = connfd.recv(1024)
        if not request:
            raise Exception
            # 解析出请求内容
        info = request.decode().split(' ')[1]
        print("请求内容:", info)
        self._send_response(connfd, info)

        # 发送响应

    def _send_response(self, connfd, info):
        if info == '/':
            filename = self.html + "/index.html"
        else:
            filename = self.html + info
        # 组织响应
        try:
            file = open(filename, 'rb')
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            with open(self.html + "/404.html", 'rb') as f:
                data = f.read()
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            data = file.read()
        finally:
            response = response.encode() + data
            connfd.send(response)  # 发送给浏览器


if __name__ == '__main__':
    httpd = WebServer(host="0.0.0.0", port=8000, html="./static")
    httpd.start()

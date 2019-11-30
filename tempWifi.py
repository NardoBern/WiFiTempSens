from threading import Timer
import time
import socket
from time import sleep
UDP_PORT = 64123
UDP_IP = ""
MESSAGE = "sveglia"
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))
sock.sendto(MESSAGE, ("10.0.1.108", 64123))


while (True):
    try:
        sock.settimeout(5.0)
        print("Aspetto dei dati")
        data, addr = sock.recvfrom(1024)
        print(data)
    except socket.timeout:
        sock.settimeout(None)
        print("Time-out di comunicazione")
    MESSAGE = "STOP"
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP,UDP_PORT))
    sock.sendto(MESSAGE, ("10.0.1.108", 64123))
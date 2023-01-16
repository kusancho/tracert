import select
import socket
import struct
import time

from icmp_header_utils import calculate_checksum


class Tracer:
    PORT = 1
    # tries per udp packet with concrete ttl
    TRIES = 1

    def __init__(self, destination: str, hops: int = 30):
        self.__destination = destination
        self.__hops = hops

    def __send(self, sender, ttl):
        initial_header = struct.pack("bbHHh", 8, 0, 0, ttl, 1)
        calculated_checksum = calculate_checksum(initial_header)
        header = struct.pack("bbHHh", 8, 0, calculated_checksum, ttl, 1)
        sender.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        sender.sendto(header, (self.__destination, Tracer.PORT))

    @staticmethod
    def __receive_address(receiver):
        try:
            socketResponseReady = select.select([receiver], [], [], 1)
            if not socketResponseReady[0]:
                return None

            return receiver.recvfrom(1024)[1]
        except socket.error:
            return None

    @staticmethod
    def __format_output(address, evaluation_time):
        if not address:
            print("*", end=' ')
            return
        try:
            address_name = socket.gethostbyaddr(address[0])[0]
        except socket.error:
            address_name = address[0]
        print(address_name, f"({address[0]})", evaluation_time, 'ms', end=' ')

    def run(self):
        try:
            # str -> IP adress
            dest_address = socket.gethostbyname(self.__destination)
        except socket.error:
            raise Exception(f"{self.__destination}: Name or service not known")

        print(f'traceroute to {dest_address} ({self.__destination}), {self.__hops} hops max')
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        for ttl in range(1, self.__hops + 1):
            print(f'{ttl:<3}', end=' ')
            for _ in range(Tracer.TRIES):
                time_start = time.perf_counter_ns()
                self.__send(sender=sock, ttl=ttl)
                address = self.__receive_address(sock)
                time_end = time.perf_counter_ns()
                self.__format_output(address, (time_end - time_start) // 1e6)
                if address and address[0] == dest_address:
                    print()
                    return 0

            print()

        print(f'Could not reach {dest_address} ({self.__destination})\nTry to increase number of hops')
        return 0

import sys
from pathlib import Path

def checksum(pseudo_header, tcp_data):
    data = pseudo_header + tcp_data

    if len(data) % 2 == 1:
        data += b'\x00'

    total = 0

    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        total += word
        total = (total & 0xffff) + (total >> 16)

    return (~total) & 0xffff

def zero_out_checksum(tcp_data):
    front = tcp_data[:16]
    zero_byte = b"\x00\x00"
    back = tcp_data[18:]

    return front + zero_byte + back

def get_checksum_from_tcp_header(tcp_header):
    return int.from_bytes(tcp_header[16:18], "big")

def generate_pseudo_header(src_ip_bytes, dest_ip_bytes, tcp_data):
    tcp_length_byte = len(tcp_data).to_bytes(2, "big")
    reserved_byte = b"\x00"
    protocol_byte = b"\x06"

    pseudo_header = (src_ip_bytes + dest_ip_bytes + reserved_byte +
                     protocol_byte + tcp_length_byte)

    return pseudo_header

def read_tcp_data(file):
    with open(file, "rb") as f:
        data = f.read()

    return data

def to_bytestrings(ip_str):
    ip_split = ip_str.split(".")
    int_list = [int(x) for x in ip_split]

    return bytes(int_list)

def get_source_and_destination_from_file(file) -> tuple[str, str]:
    with open(file, "r") as f:
        line = f.read()

    line = line.replace("\n", "")

    return line.split(" ")

def main() -> int:
    for i in range(10):

        addrs_file = f"./tcp_data/tcp_addrs_{i}.txt"
        data_file = f"./tcp_data/tcp_data_{i}.dat"

        print(f"Checking packet {i}...", end=" ")

        try:
            src_ip_str, dest_ip_str = get_source_and_destination_from_file(addrs_file)
            raw_tcp_data = read_tcp_data(data_file)

            src_ip_bytes = to_bytestrings(src_ip_str)
            dest_ip_bytes = to_bytestrings(dest_ip_str)

            ori_checksum = get_checksum_from_tcp_header(raw_tcp_data)
            tcp_zero_checksum = zero_out_checksum(raw_tcp_data)

            pseudo_header = generate_pseudo_header(src_ip_bytes, dest_ip_bytes, raw_tcp_data)

            calculate_checksum = checksum(pseudo_header, tcp_zero_checksum)

            if ori_checksum == calculate_checksum:
                print("PASS")
            else:
                print("FAIL")

        except FileNotFoundError:
            print(f"File not found! Skipped.")

    return 0

if __name__ == "__main__":
    sys.exit(main())

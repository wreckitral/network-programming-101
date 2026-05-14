import sys
import socket

def main() -> int:
    args = sys.argv[1:]
    if len(args) > 1:
        port = int(args[1])

    host = args[0]
    port = 80
    req_string = (
        "GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n\r\n"
    )
    req_in_bytes = req_string.encode("ISO-8859-1")

    response_bytes = bytearray()

    with socket.socket() as s:
        s.connect((host, port))
        s.sendall(req_in_bytes)

        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_bytes.extend(chunk)

    response_data = response_bytes.decode("ISO-8859-1")

    print(response_data)

    return 0

if __name__ == "__main__":
    sys.exit(main())

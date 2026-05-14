import sys
import socket
import json

def main() -> int:
    args = sys.argv[1:]
    port = int(args[1]) if len(args) > 1 else 80
    host = args[0]

    payload = {"message": "hello world!"}
    payload_string = json.dumps(payload)
    payload_bytes = payload_string.encode("utf-8")
    payload_length = len(payload_bytes)

    headers = (
        "GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {payload_length}\r\n"
        "Connection: close\r\n\r\n"
    )

    header_bytes = headers.encode("ISO-8859-1")

    request_bytes = header_bytes + payload_bytes

    response_bytes = bytearray()

    with socket.socket() as s:
        s.connect((host, port))

        s.sendall(request_bytes)

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

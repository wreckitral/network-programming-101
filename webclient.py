import sys
import socket
import json

def main() -> int:
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python webclient.py <host> [port] but port is optional")
        return 1

    host = args[0]
    port = int(args[1]) if len(args) > 1 else 80

    payload = {"message": "hello server!"}
    payload_bytes = json.dumps(payload).encode("utf-8")

    headers = (
        "POST / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(payload_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    header_bytes = headers.encode("ISO-8859-1")

    request_bytes = header_bytes + payload_bytes
    response_bytes = bytearray()

    with socket.socket() as s:
        try:
            s.connect((host, port))
            s.sendall(request_bytes)

            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_bytes.extend(chunk)
        except Exception as e:
            print(f"Network error: {e}")
            return 1

    if not response_bytes:
        print("Server closed connection without sending data.")
        return 1

    header_part, separator, body_part = response_bytes.partition(b"\r\n\r\n")

    print("--- HEADERS ---")
    print(header_part.decode("ISO-8859-1"))

    if body_part:
        print("\n--- BODY ---")
        try:
            print(body_part.decode("utf-8"))
        except UnicodeDecodeError:
            print("[Warning: Body is not valid UTF-8. Raw bytes below:]")
            print(body_part)

    return 0

if __name__ == "__main__":
    sys.exit(main())

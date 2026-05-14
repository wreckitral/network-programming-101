import sys
import socket
import json

def handle_client(conn: socket.socket, addr: tuple) -> None:
    try:
        request_bytes = b""

        while True:
            chunk = conn.recv(4096)
            if not chunk:
                return
            request_bytes += chunk
            if b"\r\n\r\n" in request_bytes:
                break

        if not request_bytes:
            return

        header_bytes, _, body_bytes = request_bytes.partition(b"\r\n\r\n")
        headers_lines = header_bytes.decode("ISO-8859-1").split("\r\n")

        request_line_parts = headers_lines[0].split(" ")
        if len(request_line_parts) < 2:
            print(f"[{addr}] Malformed request line: {headers_lines[0]}")
            return

        request_method = request_line_parts[0]
        request_path = request_line_parts[1]

        content_length = 0
        for line in headers_lines[1:]:
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())
                break

        if content_length > 0:
            while len(body_bytes) < content_length:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                body_bytes += chunk

        body = body_bytes.decode("utf-8") if body_bytes else "<no body>"
        print(f"[{addr}] {request_method} {request_path} | Body: {body}")

        payload = {"message": "hello client!", "path_requested": request_path}
        payload_bytes = json.dumps(payload).encode("utf-8")

        response_header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(payload_bytes)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")

        conn.sendall(response_header + payload_bytes)
        print(f"[{addr}] Served successfully.")

    except Exception as e:
        print(f"[{addr}] Error handling connection: {e}")


def main() -> int:
    args = sys.argv[1:]
    port = int(args[0]) if len(args) > 0 else 12399

    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen()
        print(f"Server listening on port {port}...")

        while True:
            conn, addr = s.accept()
            with conn:
                handle_client(conn, addr)

    return 0

if __name__ == "__main__":
    sys.exit(main())

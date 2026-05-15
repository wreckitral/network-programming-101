import sys
import socket
from pathlib import Path

PUBLIC_DIR = Path("public").resolve()

def handle_client(conn: socket.socket, addr: tuple) -> None:
    try:
        # read and parse request
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

        header_bytes, _, _ = request_bytes.partition(b"\r\n\r\n")
        headers_lines = header_bytes.decode("ISO-8859-1").split("\r\n")

        request_line_parts = headers_lines[0].split(" ")
        if len(request_line_parts) < 2:
            return

        request_method = request_line_parts[0]
        request_path = request_line_parts[1]

        print(f"[{addr}] {request_method} {request_path}")

        status_line = "HTTP/1.1 200 OK"
        content_type = "text/plain"
        response_body = b""

        match request_path:
            case "/":
                content_type = "text/html"
                response_body = b"<h1>Welcome to Faliux!</h1>"

            case _:
                # get only the filename
                clean_path = request_path.lstrip("/")

                # combine the filename with public_dir
                target_file = (PUBLIC_DIR / clean_path).resolve()

                # check if user is a bad kid
                if not target_file.is_relative_to(PUBLIC_DIR):
                    status_line = "HTTP/1.1 403 Forbidden"
                    response_body = b"403 - Forbidden: Stop trying to hack me!"

                # check if the file exist
                elif target_file.is_file():
                    # determine what file extension
                    if target_file.suffix == ".html":
                        content_type = "text/html"
                    elif target_file.suffix == ".css":
                        content_type = "text/css"
                    elif target_file.suffix in [".jpg", ".jpeg"]:
                        content_type = "image/jpeg"
                    else:
                        content_type = "text/plain"

                    # read and serve the file
                    with open(target_file, "rb") as f:
                        response_body = f.read()

                else:
                    status_line = "HTTP/1.1 404 Not Found"
                    response_body = b"404 - File Not Found"

        response_header = (
            f"{status_line}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ISO-8859-1")

        conn.sendall(response_header + response_body)
        print(f"[{addr}] Served {request_path} successfully.")

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

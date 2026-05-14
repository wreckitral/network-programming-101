import sys
import socket

def main() -> int:
    args = sys.argv[1:]
    port = int(args[0]) if len(args) > 0 else 12399


    request_body = bytearray()

    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen()

        while True:
            conn, addr = s.accept()

            with conn:
                request_bytes = b""

                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break

                    request_bytes += chunk


                    if b"\r\n\r\n" in request_bytes:
                        break

                if not request_bytes:
                    continue

                header_bytes, separator, body_bytes = request_bytes.partition(b"\r\n\r\n")

                headers_string = header_bytes.decode("ISO-8859-1")
                headers_lines = headers_string.split("\r\n")
                request_method = headers_lines[0].split(" ")[0]
                request_path = headers_lines[0].split(" ")[1]
                content_length = 0

                for line in headers_lines: # loop thru the header
                    if line.lower().startswith("content-length:"): # search for content length
                        content_length = int(line.split(":")[1].strip()) # get the value of content length
                        break

                while len(body_bytes) < content_length:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break

                    body_bytes += chunk

                response_header = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    f"Content-Length: {len(body_bytes)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                ).encode("ISO-8859-1")

                full_response = response_header + body_bytes

                conn.sendall(full_response)

                print(f"Served {request_path} to {addr}")


    return 0


if __name__ == "__main__":
    sys.exit(main())

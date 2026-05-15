import sys
import socket
import time

def main() -> int:

    with socket.socket() as s:
        try:
            s.connect(("time.nist.gov", 37))
            data = s.recv(4)

            print("NIST Time: ", int.from_bytes(data, "big"))
            print("System Time: ", system_seconds_since_1900())

            return 0

        except socket.timeout:
            print("error: Connection to NIST timed out.")
            return 1

        except Exception as e:
            print(f"error: {e}")
            return 1

def system_seconds_since_1900():
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch


if __name__ == "__main__":
    sys.exit(main())

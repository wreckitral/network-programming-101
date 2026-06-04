# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(("localhost", port))
    server.listen()

    sockets = [server]
    clients = {}

    print("waiting for connections")

    while True:
        readable, _, _ = select.select(sockets, [], [])

        for sock in readable:
            if sock is server:
                client, addr = server.accept()
                clients[client] = addr
                sockets.append(client)
                print(f"{addr}: connected")
            else:
                addr = clients[sock]
                data = sock.recv(1024)

                if not data:
                    print(f"{addr}: disconnected")
                    del clients[sock]
                    sockets.remove(sock)
                    sock.close()
                else:
                    print(f"{addr} {len(data)} bytes: {data}")

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

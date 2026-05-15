import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """
    global packet_buffer

    while True:
        if len(packet_buffer) >= WORD_LEN_SIZE:
            length_bytes = packet_buffer[:WORD_LEN_SIZE]

            word_length = int.from_bytes(length_bytes, "big")

            total_packet_size = WORD_LEN_SIZE + word_length

            if len(packet_buffer) >= total_packet_size:
                packet_data = packet_buffer[:total_packet_size]
                packet_buffer = packet_buffer[total_packet_size:]

                return packet_data

        chunk = s.recv(4096)

        if not chunk:
            return None

        packet_buffer += chunk


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    # TODO -- Write me!
    return word_packet[WORD_LEN_SIZE:].decode()


# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))

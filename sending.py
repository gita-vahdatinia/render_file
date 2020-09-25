import socket
import  tqdm
import os
import argparse

parser = argparse.ArgumentParser(description='Input files you wanna send')
parser.add_argument('files',
                   help='files to send', nargs='?')
# parser.add_argument('-i i',
#                   help='ip address to send to',)
args = parser.parse_args()


host = "192.168.1.22"
port = 5001
filename = args.files
filesize = os.path.getsize(filename)
s = socket.socket()
try:
    s.bind((host, port))
    s.listen(1)
except OSError as msg:
    s.close()
    s = None

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()

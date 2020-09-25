import socket
import tqdm
import os
import argparse
import requests

parser = argparse.ArgumentParser(description='Input files you wanna send')
parser.add_argument('files',
                   help='files to send')
parser.add_argument('name',
                  help='name to send to',)
args = parser.parse_args()


name = args.name
SERVER_HOST = "192.168.1.22"
r = requests.get(f"http://{SERVER_HOST}:5000/api/{name}")
host = r.json()
port = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
filename = args.files
filesize = os.path.getsize(filename)
s = socket.socket()
try:
    s.connect((host, port))
except OSError as msg:
    s.close()
    s = None

# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
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
s.close()

from socket import *

import random
import sys

if len(sys.argv) < 2:
    print('Usage: python server.py <port>')
    sys.exit()

port = int(sys.argv[1])
ip = ''

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((ip, port))


while True:
    message, address = serverSocket.recvfrom(30)
    message = message.upper()
    print(f'Recieve: {message}')

    if random.random() < 0.1:
        continue

    serverSocket.sendto(message, address)

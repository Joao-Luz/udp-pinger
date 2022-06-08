import random
from socket import *
import time
import sys

if len(sys.argv) < 2:
    print('Usage: python server.py <port>')
    sys.exit()

ip = '127.0.0.0'
port = int(sys.argv[1])

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((ip, port))

simulate_packet_loss = True
sleep_for_rand_response_times = True
simulate_protocol_error = True
simulate_delay_send = True

def get_time():
    return int(round(time.time() * 1000))

msg = None
addr = None
delay = False
while True:

    try:
        message, address = server_socket.recvfrom(1024)
        message = message.decode('utf-8')

        id = message[0:5]
        ping = message[5:6]
        timestamp = message[6:10]
        mssg = message[10:40]

        if simulate_packet_loss and int(id) != 8 and int(id) != 9:
            if random.random() < 0.1:
                print(message)
                print('Simulating packet loss')
                continue

        print(f'RECEIVED: {message}')

        if ping == '0':
            ping = '1'
        else:
            server_socket.sendto(message.encode('utf-8'), address)
            print('DROPPED: ping/pong error.')
            continue
        
        # protocol error
        if simulate_protocol_error and int(id) != 8:
            if random.random() < 0.2:
                pass
            elif random.random() < 0.2:
                ping = 'A'
                print('Simulating Ping/Pong error')
            elif random.random() < 0.2:
                timestamp = '0000'
                print('Simulating Timestamp error')

        print(f'id: {len(id)}/{id}  ping: {len(ping)}/{ping} timestamp: {len(timestamp)}/{timestamp} msg: {len(mssg)}/{mssg}')

        message = id + ping + timestamp + mssg

        # delay
        if int(id) < 5 and not delay and simulate_delay_send:
            if random.randint(0, 10) < 3:
                msg = message
                addr = address
                delay = True
                print('Simulating packet delay')
                continue
        
        # sending package
        if int(id) == 8 and delay and simulate_delay_send:
            server_socket.sendto(msg.encode('utf-8'), addr)
            print(f'SENT: {msg}')
            time.sleep(0.2)

        server_socket.sendto(message.encode('utf-8'), address)
        print(f'SENT: {message} ')

    except error:
        print(f'Error {error}')

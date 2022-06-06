import time
import sys
from socket import *
from statistics import mean, stdev

if len(sys.argv) != 3:
    print ('Usage: python UDPPingerClient <server ip address> <server port no>')
    sys.exit()

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1) # timeout of 1 second

ip = sys.argv[1]
port = int(sys.argv[2])

server_address = (ip, port)

rtts = []

for i in range(10):
    
    send = time.time()

    message = f'PING {i + 1} {time.strftime("%H:%M:%S")}'
    message = bytes(message, 'ascii')
    client_socket.sendto(message, server_address)
    
    try:
        data, server = client_socket.recvfrom(30)

        receive = time.time()
    
        rtt = 1000*(receive - send)
        rtts.append(rtt)
        print(f'Received {data} - rtt : {rtt:.4f}ms')
    
    except timeout:
        print(f'Timeout on packet {i}')

print(f'10 packets transmitted, {len(rtts)} received, {10*(10 - len(rtts))}% packet loss')
print(f'time - {sum(rtts):.4f}ms')
print(f'min - {min(rtts):.4f}ms')
print(f'avg - {mean(rtts):.4f}ms')
print(f'std - {stdev(rtts):.4f}ms')  
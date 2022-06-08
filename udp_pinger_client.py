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

def form_message(i : int, msg : str) -> str:
    # message has format 00001  0        2431          message00000000000000000000000
    #                    < id > < ping > < timestamp > <             msg            >
    id = str(i).rjust(5,'0')
    ping = '0'
    timestamp = str(int(time.time_ns()/1000000) % 10000)
    message = msg.ljust(30, '\0')

    return id + ping + timestamp + message

print(f'Sending 10 packages to {ip}:{port}...\n')

for i in range(10):
    
    senttime = time.time()

    # form message
    sentmsg = form_message(i, 'some message')

    # send message
    client_socket.sendto(sentmsg.encode(), server_address)

    # receive message
    try:
        recvmsg, sever = client_socket.recvfrom(40)
        recvmsg = recvmsg.decode()

        # check for:
        #   1- correct id
        recvid = int(recvmsg[0:5])
        while(recvid < i):
            #   1.1- discard message and keep waiting for the right one
            recvmsg, sever = client_socket.recvfrom(40)
            recvmsg = recvmsg.decode()
            recvid = int(recvmsg[0:5])
        
        recvtime = time.time()
        
        #   2- is a pong
        recvpong = recvmsg[5]
        if recvpong != '1':
            print(f'\t{i} - Invalid package: expected a pong!')
            continue

        #   3- messages match
        if (recvmsg[0:5] + recvmsg[6:]) != (sentmsg[0:5] + sentmsg[6:]):
            print(f'\t{i} - Invalid package: ping and pong don\'t match!')
            continue

        rtt = (recvtime - senttime)*10**4
        print(f'\t{i} - Received package - rtt: {rtt:.3f}ms')
        rtts.append(rtt)
        
    # if timeout, go to next message
    except timeout:
        print(f'\t{i} - Timeout')

print(f'\n--- {ip}:{port} ping statistics ---')
print(f'10 packets transmitted, {len(rtts)} received, {10*(10 - len(rtts))}% packet loss, time={sum(rtts):.0f}ms')
print(f'rtt min/avg/max/mdev = {min(rtts):.3f}/{mean(rtts):.3f}/{max(rtts):.3f}/{stdev(rtts):.3f} ms')
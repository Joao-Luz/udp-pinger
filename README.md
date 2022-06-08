# udp-pinger

This is a very simple implemetation of an UDP pinger. The client pings a fixed length message 10 times to the server and waits for the server to return the message. The client, then, calculates the RTT for each message and prints on the terminal (along with the min, max, mean and standard deviation of RTT times). The server simulates a few possible faults, such as:

- Packet loss
- Protocol errors
- Delayed response

The client treats all of these and only considers the propper packages when computing the statistics.

## Running

To run the server, do:

    pyhton udp_pinger_server <port>

Where `<port>` is the port that you want the server to occupy. For the client, run:

    python udp_pinger_client <server_ip> <server_port>

Where `<server_ip>` is the ip address for the server program and `<server_port>` is the respective port.

## Output

### Client
The client's output will look like:

    Sending 10 packages to <address>...
        0- <Package status>
        .
        .
        .
        9- <Package status>

    --- <address> ping statistics ---'
    10 packets transmitted, <n> received, n% packet loss, time=<full time>ms
    rtt min/avg/max/mdev = <min>/<avg>/<max>/<mdev> ms

Where `<package status>` might be:

- `Invalid package: expected a pong!`: the pong byte is not a `'1'`;
- `Invalid package: ping and pong don't match!`: received and sent messages don't match;
- `<id> - Received package - rtt: <rtt>ms`: Successful package transmission.

### Server
The server's output will log what happens with the incoming packages. I'll log things such as:

- `RECEIVED: <message>`: when receiving a message;
- `SENT: <message>`: when sendinG a message;
- `DROPPED: ping/pong error`: when the incoming message has a problem in the ping/pong byte;
- `Simulating <fault>`: when simulating some possible fault.

The 'sent' message will be modified according to the faults simulated. The modifications are visible on the `SENT: <message>` log.

## Example


### Client output
    $ python udp_pinger_client 127.0.0.0 3000

    Sending 10 packages to 127.0.0.0:3000...

        0 - Received package - rtt: 1.895ms
        1 - Received package - rtt: 1.647ms
        2 - Invalid package: expected a pong!
        3 - Timeout for package
        4 - Received package - rtt: 4.444ms
        5 - Received package - rtt: 3.943ms
        6 - Invalid package: expected a pong!
        7 - Invalid package: ping and pong don't match!
        8 - Received package - rtt: 2007.799ms
        9 - Received package - rtt: 3.824ms

    --- 127.0.0.0:3000 ping statistics ---
    10 packets transmitted, 6 received, 40% packet loss, time=2024ms
    rtt min/avg/max/mdev = 1.647/337.259/2007.799/818.395 ms

### Server output
    $ python udp_pinger_server 3000

    RECEIVED: 0000008971some message
    id: 5/00000  ping: 1/1 timestamp: 4/8971 msg: 30/some message
    SENT: 0000018971some message 
    RECEIVED: 0000108971some message
    id: 5/00001  ping: 1/1 timestamp: 4/8971 msg: 30/some message
    SENT: 0000118971some message 
    RECEIVED: 0000208971some message
    Simulating Ping/Pong error
    id: 5/00002  ping: 1/A timestamp: 4/8971 msg: 30/some message
    SENT: 00002A8971some message 
    RECEIVED: 0000308971some message
    id: 5/00003  ping: 1/1 timestamp: 4/8971 msg: 30/some message
    Simulating packet delay
    RECEIVED: 0000409973some message
    id: 5/00004  ping: 1/1 timestamp: 4/9973 msg: 30/some message
    SENT: 0000419973some message 
    RECEIVED: 0000509973some message
    id: 5/00005  ping: 1/1 timestamp: 4/9973 msg: 30/some message
    SENT: 0000519973some message 
    RECEIVED: 0000609974some message
    Simulating Ping/Pong error
    id: 5/00006  ping: 1/A timestamp: 4/9974 msg: 30/some message
    SENT: 00006A9974some message 
    RECEIVED: 0000709974some message
    Simulating Timestamp error
    id: 5/00007  ping: 1/1 timestamp: 4/0000 msg: 30/some message
    SENT: 0000710000some message 
    RECEIVED: 0000809974some message
    id: 5/00008  ping: 1/1 timestamp: 4/9974 msg: 30/some message
    SENT: 0000318971some message
    SENT: 0000819974some message 
    RECEIVED: 000090175some message
    id: 5/00009  ping: 1/1 timestamp: 4/175s msg: 29/ome message
    SENT: 000091175some message 
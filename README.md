# udp-pinger

This is a very simple implemetation of an UDP pinger. The client pings a fixed length message 10 times to the server and waits for the server to return the message. The client, then, calculates the RTT for each message and prints on the terminal (along with the min, max, mean and standard deviation of RTT times). The server simulates packet loss with a 10% chance of happening. The client will wait 1 second untill declaring packet loss.

## Running

To run the server, do:

    pyhton udp_pinger_server <port>

Where `<port>` is the port that you want the server to occupy. For the client, run:

    python udp_pinger_client <server_ip> <server_port>

Where `<server_ip>` is the ip address for the server program and `<server_port>` is the respective port.

### Example

    $ python udp_pinger_server 3000
    $ python udp_pinger_client 127.0.0.0 3000

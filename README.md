# MSCS-631-Python-Lab4

# ICMP Pinger Lab Assignment

This program implements an **ICMP Pinger** in Python. It sends ICMP Echo Requests (ping) to a specified host and receives ICMP Echo Replies, calculating the round-trip time (RTT) and displaying the results.

---

## **Requirements**

- Python 3.x
- Administrator/root privileges to run the program (for raw socket access)

---

## **How to Run**

### **On Linux/Mac**
1. Open the terminal.
2. Navigate to the directory containing `ping_client.py`.
3. Run the program with elevated privileges:
   ```bash
   sudo python3 ping_client.py
   
### **On Windows**
1. Open Command Prompt as Administrator.
2. Navigate to the directory containing ping_client.py.
3. Run the program:
	python ping_client.py

## Program input
1. You will be prompted to enter a host to ping
2. The program will continously ping the specified host, displaying results for each ping until you stop it. 

## Sample output
Enter the host to ping (e.g., google.com): www.google.com
Pinging 142.250.190.132 using Python:

Reply from 142.250.190.132: time=41.88 ms
Reply from 142.250.190.132: time=36.85 ms
Reply from 142.250.190.132: time=37.54 ms
Reply from 142.250.190.132: time=38.72 ms
Reply from 142.250.190.132: time=38.20 ms
^C
Ping test interrupted. Exiting...

## Features
1. Sends ICMP Echo Requests to a specified host.
2. Measures the round-trip time (RTT) for each ping.
3. Handles program interruption (Ctrl + C) gracefully, displaying a clean exit message.

## Explanation of Code

1. checksum(): Calculates the checksum for the ICMP packet.
2. sendOnePing(): Constructs and sends an ICMP Echo Request packet.
3. receiveOnePing(): Receives and processes the ICMP Echo Reply packet.
4. doOnePing(): Handles sending and receiving a single ping.
5. ping(): Continuously pings the specified host with a one-second delay between each ping.

## Testing Instructions

1. Test on localhost (127.0.0.1) to verify basic functionality.
2. Test on multiple hosts in different continents:
North America: google.com
Europe: bbc.co.uk
Asia: baidu.com
Australia: sydney.edu.au

#Author
Sandesh Pokharel





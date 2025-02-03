# ICMP Pinger Lab Assignment
# This script sends ICMP Echo Requests (pings) to a specified host and listens for Echo Replies (pong).
# It calculates the round-trip time (RTT), detects packet loss, and prints a summary of the statistics.
# The script uses raw sockets, so it may require admin/root privileges to run.
# Added exception handling to display a clean exit message when the program is interrupted (Ctrl+C).

from socket import *
import os
import sys
import struct
import time
import select

# Define the ICMP Echo Request type (8)
ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    """
    Calculate the checksum for the provided string.
    The checksum is a simple error-checking code used in network protocols.
    """
    csum = 0  # Initialize checksum
    count_to = (len(source_string) // 2) * 2  # Iterate over all pairs of bytes
    count = 0

    # Sum all 16-bit words in the string
    while count < count_to:
        # Combine two bytes to form a 16-bit word
        this_val = source_string[count + 1] * 256 + source_string[count]
        csum = csum + this_val  # Add the word to the checksum
        csum = csum & 0xffffffff  # Keep checksum within 32 bits
        count = count + 2  # Move to the next pair of bytes

    # If there's a leftover byte, add it to the checksum
    if count_to < len(source_string):
        csum = csum + source_string[len(source_string) - 1]

    # Finalize the checksum by folding high bits into low bits
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum  # Take the bitwise complement
    answer = answer & 0xffff  # Ensure the checksum is 16 bits
    answer = answer >> 8 | (answer << 8 & 0xff00)  # Swap bytes for network byte order

    return answer

def receiveOnePing(my_socket, ID, timeout, dest_addr):
    """
    Receive the ICMP reply (pong) from the target host.
    Extract the ICMP header and calculate the round-trip time (RTT).
    """
    time_left = timeout  # Time remaining to wait for a reply

    while True:
        # Record the time when waiting starts
        started_select = time.time()

        # Wait for the socket to become ready for reading (or timeout)
        what_ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = (time.time() - started_select)  # Measure wait time

        # Check if the timeout occurred
        if not what_ready[0]:
            return "Request timed out."

        # Receive the packet and record the time it was received
        time_received = time.time()
        rec_packet, _ = my_socket.recvfrom(1024)  # Receive up to 1024 bytes

        # Extract the ICMP header from the received packet
        icmp_header = rec_packet[20:28]  # ICMP header starts after 20-byte IP header
        type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)

        # Verify if the packet ID matches our request
        if packet_id == ID:
            # Extract the time the packet was sent
            bytes_in_double = struct.calcsize("d")  # Size of a double in bytes
            time_sent = struct.unpack("d", rec_packet[28:28 + bytes_in_double])[0]

            # Calculate round-trip time (RTT)
            rtt = (time_received - time_sent) * 1000  # Convert to milliseconds
            return f"Reply from {dest_addr}: time={rtt:.2f} ms"

        # Update the remaining time
        time_left = time_left - how_long_in_select
        if time_left <= 0:
            return "Request timed out."

def sendOnePing(my_socket, dest_addr, ID):
    """
    Send an ICMP Echo Request (ping) to the target host.
    """
    # Header is composed of type (8), code (8), checksum (16), ID (16), and sequence (16)
    my_checksum = 0  # Initialize checksum to 0

    # Create a dummy header with a 0 checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)

    # Add the current timestamp as the data payload
    data = struct.pack("d", time.time())

    # Calculate the checksum on the header and data
    my_checksum = checksum(header + data)

    # Convert checksum to network byte order
    my_checksum = htons(my_checksum)

    # Rebuild the header with the correct checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    packet = header + data  # Final packet = header + data

    # Send the packet to the destination address
    my_socket.sendto(packet, (dest_addr, 1))

def doOnePing(dest_addr, timeout):
    """
    Perform a single ping to the target host.
    """
    # Get the protocol number for ICMP
    icmp = getprotobyname("icmp")

    # Create a raw socket for sending and receiving ICMP packets
    my_socket = socket(AF_INET, SOCK_RAW, icmp)

    # Use the current process ID as the packet ID
    my_id = os.getpid() & 0xFFFF

    # Send a ping to the target host
    sendOnePing(my_socket, dest_addr, my_id)

    # Wait for the reply and calculate the delay
    delay = receiveOnePing(my_socket, my_id, timeout, dest_addr)

    # Close the socket
    my_socket.close()

    return delay

def ping(host, timeout=1):
    """
    Continuously ping the specified host and display the results.
    """
    # Resolve the hostname to an IP address
    dest = gethostbyname(host)
    print(f"Pinging {dest} using Python:\n")

    try:
        while True:
            # Perform one ping and print the result
            print(doOnePing(dest, timeout))
            time.sleep(1)  # Wait 1 second between pings

    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("\nPing test interrupted. Exiting...\n")

if __name__ == "__main__":
    # Allow the user to input the host to ping
    host = input("Enter the host to ping (e.g., google.com): ")
    ping(host)


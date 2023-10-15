from cgi import test
import DNSStarter
import ipaddress
import sys
import socket
from DNSStarter import DNSHeader, DNSQuestion, DNSDatagram, read_datagram, write_datagram, NameDecoder


# Check the number of command-line arguments
if len(sys.argv) < 2:
    print("You need to enter a domain.")
    sys.exit(1)

domain = sys.argv[1]

def resolve_domain(ipType):
    # Create a DNS query
    header = DNSHeader(12345, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)
    qname = domain.split(".")  # Use a list of strings here
    question = DNSQuestion(qname, ipType, 1)
    datagram = DNSDatagram(header, [question], [])

    datagram_bytes = write_datagram(datagram)

    # Send the DNS query to a DNS server (e.g., Google's DNS server)
    dns_server = ("8.8.8.8", 53)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(datagram_bytes, dns_server)

    # Receive and parse the DNS response
    response_bytes, _ = udp_socket.recvfrom(4096)
    response_datagram = read_datagram(response_bytes)

    # Process the answers and display the results
    for answer in response_datagram.answers:
        if answer.type == 1:  # IPv4
            print("IPv4 Address:", ".".join(map(str, answer.rdata)))
        elif answer.type == 28:  # IPv6
            ipv6_address = ":".join([f"{byte:02x}" for byte in answer.rdata])
            print("IPv6 Address:", ipv6_address)
        elif answer.type == 5:  # CNAME
            cNameFormat = ".".join(map(str, answer.cname_as_array_list(response_datagram)))
            print("CNAME format:", cNameFormat)

# Call the resolve_domain function for both IPv4 and IPv6
resolve_domain(1)  # IPv4
resolve_domain(28)  # IPv6
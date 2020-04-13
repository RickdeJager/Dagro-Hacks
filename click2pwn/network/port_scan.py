from socket import *
import nmap
import subprocess
import colorama

'''
    Performs a port scan to find web server's port.
    The web server runs on a port in the 20000-62000 range.
    23, 23456 and 34567 are reserved for other operations
'''

start, end = 20000, 62000

def find_web_server(ip_addr, args="--max-parallelism 1"):
    '''
    Uses the nmap import to find web server's port
    '''
    # Scan over ports 20000-62000
    nm = nmap.PortScanner()
    nm.scan(ip_addr, "%d-%d" % (start, end), arguments=args)

    # No results found
    if not ip_addr in nm.all_hosts():
        print(colorama.Fore.RED + "[!] The host at '%s' appears to be down." % (ip_addr))
        return

    # Loop over scan output to find port
    for port in nm[ip_addr]['tcp'].keys():
        if port not in (23, 23456, 34567) and \
                nm[ip_addr]['tcp'][port]['state'] == "open":
            return port

def get_local_ip(host="example.com", port=80):
    '''
    Finds the local IP adress of the attacker
    '''
    # Create socket and connect to socket
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect((host, port))
    
    # Local IP adress is first element of tuple
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

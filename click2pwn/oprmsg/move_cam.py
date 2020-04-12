import sys
import struct
import socket
import time

def send_request(payload, host, port=23456):
    """
    Sends a request and returns the response
    """
    print("[i] sending %r" % payload)

    # Create socket and connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(payload)
    time.sleep(0.5)
    sock.shutdown(socket.SHUT_WR)
    res = b""

    # Append received data and return it
    while True:
        data = sock.recv(1024)
        if not data:
            break
        res += data

    sock.close()
    print("[i] recv %r" % res)
    return res

def move_cam(host, command):
    """
    This function moves the camera in 4 possible directions
    """
    # 4294967291 is -5 in 2's complement
    commands = {
        'up':    (0, 5),
        'down':  (0, -5),
        'right': (5, 0),
        'left':  (-5, 0),
    }
    
    # Check if user input command is valid
    if command not in commands:
        return

    code = commands[command]

    # Based on https://github.com/ap-rose/php-ptz-controller
    request = struct.pack("<10I2i6I",
        0xffeeddcc, 0x4f77, 6886115, 18 * 4,
        0,
        1002869679, 21755657,
        1, 0, 0,
        *code,
        0, 0, 0, 0, 0, 0
    )

    # Send packed bytes
    send_request(request, host)

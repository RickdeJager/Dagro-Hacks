# Dagro-Hacks
This repo contains a PoC that can be used to gain a shell on several Dagro IP Cameras.

## TLDR

Our tool can be used to gain a root shell on a number of different IP Cameras. The only thing the user needs to enter is the IP of the camera.
![Hacking in progress](doc/res/shell_dark.gif)

## Installing

The exploit was developed on linux, and will require some minor changes to work on Windows. Our installation instructions assume you are running a fresh install of Ubuntu 18. 
  
We also provide a `Dockerfile`. Keep in mind that your docker host needs to support [the "host" networking driver](https://docs.docker.com/network/network-tutorial-host/#prerequisites) which is, at time of writing, only available on linux. Skip to [Docker](#Docker) for instructions.

You need the following tools to run this exploit:

### GCC toolchain

The camera we conducted our tests on was running armv5le. We used the `arm-linux-gnueabihf` toolchain to build our shellcode. It can be installed on Ubuntu using:
```bash
sudo apt install binutils-arm-linux-gnueabihf
```

### Python

We used python 3.7.5+ to build this tool. All requirements are contained in `requirements.txt`.  

  
The fastest way to setup your environment is to use `venv`:  
1. `python3 -m pip install --user virtualenv`
1. `python3 -m venv env`
1. `source env/bin/activate`
1. `pip install -r requirements.txt`  

When you want to leave this env, run `deactivate`.  

## Running the script
To run the script, navigate to the `click2pwn` directory, activate the `venv` and run:  
```bash
python main.py [target ip]
```
Typing `help` will show a full list of supported commands. The most interesting one being `shell`, which opens a reverse shell on the target host.

## Docker
Every modern repository comes with a Dockerfile and we did not want to fall behind. To run our tool using docker:  
1. `docker build . -t dagro-hacks`
1. `docker run --network=host -it dagro-hacks`

## FAQ / Troubleshooting

### The camera crashes before the port scan completes
Sadly, the model we tested with has a randomized port scan in the `20000-62000` range. This requires a large port scan which can overwhelm the camera. The nmap arguments can be changed in `network/port_scan.py`.

### The port scan is too slow
The port scan might take up to 5 minutes. In our experience, the scan is slightly slower in the docker container. We tried to balance speed against reliability. The port scan can be sped up by editing the nmap arguments.

### The webserver port of my camera is not in the scan range
You can manually set the port of the camera by typing:
```
set tport xxxx
```

# Background information

More information on _how_ our exploit was developed can be found [here](docs/content/index.md).

# Acknowledgments

This exploit was developed by a team of 3 students, namely:
* [Luke Serné](https://github.com/LukeSerne)
* [Leonardo Mathon](https://github.com/leonardomathon)
* [Rick de Jager](https://github.com/rickdejager)

It was developed as a part of the "Offensive Security" course, taught at Eindhoven University of Technology, by [Luca Allodi](https://lallodi.github.io/index.html). We'd like to thank Dr. Allodi and all TA's involved in the course for teaching us about various exploits, attack vectors, and for helping us trouble-shoot issues.

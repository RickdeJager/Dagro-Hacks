# Dagro-Hacks
This repo contains a PoC that can be used to gain a shell on several Dagro IP Cameras.

## TLDR

![Hacking in progress](doc/res/shell_dark.gif)

## Installing

The exploit was developed on linux, and will require some minor changes to work on Windows. Our installation instructions assume you are running a fresh install of Ubuntu 18. 


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
1. `pip install requirements.txt`  

When you want to leave this env, run `deactivate`.  

## Running the script
To run the script, navigate to the `click2pwn` directory, activate the `venv` and run:  
```bash
python main.py [target ip]
```
Typing `help` will show a full list of supported commands. The most interesting one being `shell`, which opens a reverse shell on the target host.


# Acknowledgments

This exploit was developed by a team of 3 students, namely:
* [Luke Serné](https://github.com/LukeSerne)
* [Leonardo Mathon](https://github.com/leonardomathon)
* [Rick de Jager](https://github.com/rickdejager)

It was developed as a part of the "Offensive Security" course, taught at Eindhoven University of Technology, by [Luca Allodi](https://lallodi.github.io/index.html). We'd like to thank Mr. Allodi and all TA's involved in the course for teaching us about various exploits, attack vectors, and for helping us trouble-shoot issues.

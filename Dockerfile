FROM ubuntu:18.04

RUN apt-get update && apt-get -y install binutils-arm-linux-gnueabihf python3 python3-pip nmap

COPY click2pwn /click2pwn

RUN pip3 install -r /click2pwn/requirements.txt

CMD python3 /click2pwn/main.py


#!/bin/sh
sudo apt install python3-pip -y
pip3 install -r /home/ubuntu/newsfeed/requirements.txt
cd /home/ubuntu/newsfeed && echo "Hello world" >> hello.txt
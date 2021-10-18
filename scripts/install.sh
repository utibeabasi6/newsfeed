#!/bin/sh
sudo apt install python3-pip -y
pip3 install -r /home/ubuntu/newsfeed/requirements.txt
echo "Hello world" >> /home/ubuntu/newsfeed
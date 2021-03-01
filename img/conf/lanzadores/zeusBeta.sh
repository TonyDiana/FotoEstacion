#!/bin/sh
cd /home/pi/zeus

bash ./Super_pre.sh
git add .
git commit -m "Ok"
git fetch --all
git reset --hard origin/beta
git pull origin beta
bash ./Super_post.sh


cd ./img/bin
python3 ./zeus.py

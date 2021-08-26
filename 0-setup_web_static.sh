#!/usr/bin/env bash
# sets up web servers for the deployment of web_static

dpkg -s nginx >/dev/null 2>&1

if [ "$?" ]
then
        apt-get -y update
        apt-get install -y nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "testing" > /data/web_static/releases/test/index.html

ln -fs /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data/

server_block="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
file="/etc/nginx/sites-available/default"

sed -i "41a\ $server_block" "$file";
service nginx restart

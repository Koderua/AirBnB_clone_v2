#!/usr/bin/python3
"""fabfile that handles deployment of archive files"""
from fabric.api import *
from os.path import isfile

env.hosts = ['34.138.61.3', '34.75.118.132']
env.user = "ubuntu"


def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if not isfile(archive_path):
        return False
    success = put(archive_path, "/tmp/")
    file_name = archive_path.split("/")[-1]
    file_path = "/data/web_static/releases/{}".format(file_name.split(".")[0])
    success = run("mkdir -p {}".format(file_path))
    success = run("tar -xzf /tmp/{} -C {}".format(file_name, file_path))
    success = run("rm /tmp/{}".format(file_name))
    success = run("mv {}/web_static/* {}/".format(file_path, file_path))
    success = run("rm -rf {}/web_static".format(file_path))
    success = run("rm -rf /data/web_static/current")
    success = run("ln -s {} {}".format(file_path, "/data/web_static/current"))
    return success.succeeded

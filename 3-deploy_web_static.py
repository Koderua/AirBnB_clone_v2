#!/usr/bin/python3
"""creates and distributes an archive to web servers"""
from fabric.api import *
from datetime import datetime
from os.path import abspath, isfile, exists

env.hosts = ['34.138.61.3', '34.75.118.132']
env.user = "ubuntu"


def do_pack():
    """creates a tarfile"""
    local("mkdir -p versions")
    now = datetime.now()
    tar_file = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    success = local("tar -cvzf versions/{} web_static".format(tar_file))
    if not exists("./versions/{}".format(tar_file)):
        return None
    else:
        return abspath("./versions/{}".format(tar_file))


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


def deploy():
    """creates and distributes an archive"""
    packed = do_pack()
    if not packed:
        return False
    deployed = do_deploy(packed)
    return deployed

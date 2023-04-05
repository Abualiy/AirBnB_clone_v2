#!/usr/bin/python3
"""compresing web_static package
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['54.172.132.229', '54.144.223.170']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploying file"""
    try:
        if not (path.exists(archive_path)):
            return False

        # upload
        put(archive_path, '/tmp/')

        # create dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/\
                releases/web_static_{}/'.format(timestamp))

        # uncompress
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
                    .format(timestamp, timestamp))

        # remove the archve
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # moving content in to host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
                    .format(timestamp))

        # delete
        run('sudo rm -rf /data/web_static/current')

        # re-establish
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))

    except:
        return False

    return True

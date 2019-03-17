import errno
import json
import os
import random
import socket

rndName = None
hitCount = 0


def get_hostname():
    return socket.gethostname()


def get_local_address():
    return socket.gethostbyname(socket.gethostname())


def get_worker_instance():
    global rndName
    if not rndName:
        rndName = random.randint(1, 1000)
    return "Worker Instance {}".format(rndName)


def get_target():
    return os.environ.get("TARGET", "undefined")


def get_server_hit_count():
    global hitCount
    hitCount = hitCount + 1
    return hitCount


def read_config(app):
    # noinspection PyBroadException
    try:
        with open('/etc/config/config') as json_file:
            config = json.load(json_file)
            # copy config params into flask's
            for k in config.keys():
                app.config[k] = config[k]
            app.logger.debug("from /etc/config: {}".format(config))
    except (OSError, IOError) as e:  # FileNotFoundError does not exist on Python < 3.3
        # It is no big deal if file is not there.
        if getattr(e, 'errno', 0) != errno.ENOENT:
            app.logger.error("Opening /etc/config failed: {}".format(e))

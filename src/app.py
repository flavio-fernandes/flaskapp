import os
import time

from flask import Flask
from flask import request
from flask import jsonify
import datetime

import utils

BOOM_ABORT = frozenset(["no", "0", "false", "nay", "never", "negative", "difused", "nack"])
MY_RELEASE = os.environ.get('RELEASE', "undefined")

startTime = datetime.datetime.now().replace(microsecond=0)
startTimeStr = startTime.strftime("%Y-%b-%d %H:%M:%S %Z").strip()

app = Flask(__name__)
utils.read_config(app)


@app.route("/")
def show_details():
    _handle_args(request.args)
    uptime = datetime.datetime.now().replace(microsecond=0) - startTime
    return "<html>" + \
           "<head><title>Demo Application</title></head>" + \
           "<body>" + \
           "<table>" + \
           "<tr><td> Release </td> <td>" + MY_RELEASE + "</td> </tr>" + \
           "<tr><td> Start Time </td> <td>" + startTimeStr + "</td> </tr>" + \
           "<tr><td> Up Time </td> <td>" + str(uptime) + "</td> </tr>" + \
           "<tr><td> Hostname </td> <td>" + utils.get_hostname() + "</td> </tr>" + \
           "<tr><td> Local Address </td> <td>" + utils.get_local_address() + "</td> </tr>" + \
           "<tr><td> Remote Address </td> <td>" + request.remote_addr + "</td> </tr>" + \
           "<tr><td> Server Hit </td> <td>" + str(utils.get_server_hit_count()) + "</td> </tr>" + \
           "<tr><td> Worker Instance </td> <td>" + utils.get_worker_instance() + "</td> </tr>" + \
           "<tr><td> Target </td> <td>" + utils.get_target() + "</td> </tr>" + \
           "</table>" + \
           "</body>" + \
           "</html>"


@app.route("/json")
def send_json():
    _handle_args(request.args)
    uptime = datetime.datetime.now().replace(microsecond=0) - startTime
    return jsonify({'Release': MY_RELEASE,
                    'StartTime': startTimeStr,
                    'Uptime': str(uptime),
                    'Hostname': utils.get_hostname(),
                    'LocalAddress': utils.get_local_address(),
                    'RemoteAddress': request.remote_addr,
                    'ServerHit': str(utils.get_server_hit_count()),
                    'WorkerInstance': utils.get_worker_instance(),
                    'Target': utils.get_target(),
                    })


def _handle_args(args):
    arg_delay = args.get("delay")
    if arg_delay:
        try:
            # sleep delay in milliseconds
            time.sleep(int(arg_delay) / 1000.0)
        except ValueError:
            pass
    arg_boom = args.get("boom")
    if arg_boom is not None and arg_boom.lower() not in BOOM_ABORT:
        app.logger.error("bye bye cruel world")
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

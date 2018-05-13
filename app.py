from flask import Flask, render_template, request
from .app_conf import AppConfig, get_all_config_files
from json import dumps
from .conf_util import ConfigUtil
import os 

PID_DIR = "/home/qf/work/flask_app_manager/pid/"


def create_app():

    app = Flask(__name__)


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/configs')
    def get_configs():
        config_names = get_all_config_files()
        apps = []
        for config_name in config_names:
            apps.append({
                'name':config_name,
                'status': get_app_status(config_name)})

        return dumps({'code':0, 'apps':apps})

    @app.route('/config_status', methods=(['POST']))
    def config_status():
        config_name = request.form.get('config_name')
        config_status = request.form.get('config_status')
        if not config_name or not config_status:
            return dumps({'code': -1})

        if config_status == 'stop':
            ret = stop_app(config_name)
        if config_status == 'run':
            ret = run_app(config_name)

        if not ret:
            return dumps({'code': -2})

        return dumps({'code':0})

    return app

def get_app_status(config_name):
    lock_file = PID_DIR + config_name + '.lock'
    pid_file = PID_DIR + config_name + '.pid'

    if os.path.exists(lock_file) and os.path.exists(pid_file):
        return 'stopping'
    if os.path.exists(pid_file):
        return 'running'
    if os.path.exists(lock_file):
        os.remove(lock_file)
    return 'stopped'


def stop_app(config_name):
    pid_file = PID_DIR + config_name + '.pid'
    lock_file = PID_DIR + config_name + '.lock'
    if os.path.exists(lock_file):
        return False

    f = open(lock_file, 'w')
    f.close()

    os.system('/bin/bash scripts/stop_app.sh %s %s %s' % (config_name, pid_file, lock_file))
    return True

def run_app(config_name):
    print('run', config_name)
    config = ConfigUtil(config_name)
    root_dir = config.get('default', 'root_dir')
    if not root_dir:
        return False

    venv_name = config.get('default', 'venv_name', 'venv')
    worker_count = config.get('default', 'worker_count', 4)
    host = config.get('default', 'host', '127.0.0.1')
    port = config.get('default', 'port', '7000')
    wsgi_file = config.get('default', 'wsgi_file', 'app')
    wsgi_obj = config.get('default', 'wsgi_obj', 'app')
    pid_file = PID_DIR + config_name + '.pid'

    os.system('/bin/bash scripts/run_app.sh %s %s %s %s %s %s %s %s %s' % (config_name, root_dir, venv_name, worker_count, host, port, wsgi_file, wsgi_obj, pid_file))
    return True

app = create_app()
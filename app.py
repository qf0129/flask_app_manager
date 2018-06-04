import sys  
if 'python3' not in sys.executable:
    print('please use python3')
    sys.exit(0)

import os 
from json import dumps
from conf_util import ConfigUtil, get_all_configs
from bottle import Bottle, template, request, static_file
from threading import Thread


PID_DIR = os.getcwd() + "/pid/"


def create_app():

    app = Bottle()

    @app.get('/')
    def index():
        return template('tpls/index.html')

    @app.get('/static/<filename>')
    def get_static_file(filename):
        return static_file(filename, 'statics')

    @app.get('/configs')
    def get_configs():
        config_names = get_all_configs()
        apps = []
        for config_name in config_names:
            config = ConfigUtil(config_name)
            err_list = config.check_config()

            apps.append({
                'name': config_name,
                'err_list': err_list,
                'status': get_app_status(config_name)})

        return dumps({'code':0, 'apps':apps})

    @app.post('/config_status')
    def config_status():
        config_name = request.forms.get('config_name')
        config_status = request.forms.get('config_status')
        if not config_name or not config_status:
            return dumps({'code': -1, 'msg': 'params error'})

        if config_status == 'stop':
            t = Thread(target=stop_app,args=(config_name,))
        if config_status == 'run':
            t = Thread(target=run_app,args=(config_name,))
        t.start()

        # if not ret:
        #     return dumps({'code': -2})

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
    port = config.get('default', 'port', '7001')
    wsgi_file = config.get('default', 'wsgi_file', 'app')
    wsgi_obj = config.get('default', 'wsgi_obj', 'app')
    pid_file = PID_DIR + config_name + '.pid'

    config.set(venv_name=venv_name, worker_count=worker_count, host=host, port=port, wsgi_file=wsgi_file, wsgi_obj=wsgi_obj, pid_file=pid_file)

    os.system('/bin/bash scripts/run_app.sh %s %s %s %s %s %s %s %s %s' % (config_name, root_dir, venv_name, worker_count, host, port, wsgi_file, wsgi_obj, pid_file))
    return True

if __name__ == '__main__':

    if 'python3' not in sys.executable:
        print('please use python3')
    else:
        app = create_app()
        app.run(host='0.0.0.0', port=7000, debug=True)
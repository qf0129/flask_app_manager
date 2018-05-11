from flask import Flask, render_template, request
from .app_conf import ConfigParser, get_all_config_files
from json import dumps


def create_app():

    app = Flask(__name__)


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/configs')
    def get_configs():
        configs = get_all_config_files()
        return dumps({'code':0, 'configs':configs})

    @app.route('/start_config', methods=(['POST']))
    def start_config():
        req_json = request.get_json()
        if 'config_name' not in req_json:
            return dumps({'code': -1})
            
        config_name = req_json['config_name']

        # start_from_config(config_name)
        return dumps({'code':0})

    return app

def start_from_config(config_name):
    config = ConfigParser(config_name)
    root_dir = config['default']['root_dir']
    virtualenv_dir = config['default']['virtualenv_dir']
    worker_count = config['default']['worker_count']
    host = config['default']['host']
    port = config['default']['port']
    os.system('/bin/bash other_app.sh %s %s %s %s %s %s ' % (config_name, root_dir, virtualenv_dir, worker_count, host, port))

app = create_app()
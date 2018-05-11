from configparser import ConfigParser
import os


CONFIG_DIR = "conf.d/"


class AppConfig(ConfigParser):
    def __init__(self, filename):
        self.filepath = CONFIG_DIR + filename
        super(AppConfig, self).__init__()
        
        if os.path.exists(self.filepath):
            self.read(self.filepath)
        else:
            self['default'] = {'root_dir': '',
                                'virtualenv_dir': '',
                                'worker_count': 2,
                                'host': '127.0.0.1',
                                'port': '7001'}

    def save(self):
        with open(self.filepath, 'w') as f:
            self.write(f)

def get_all_config_files():
    return os.listdir(CONFIG_DIR)


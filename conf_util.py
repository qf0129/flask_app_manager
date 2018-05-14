from configparser import ConfigParser
import os

CONFIG_DIR = os.getcwd() + "/conf.d/"

class ConfigUtil:
    def __init__(self, config_name):
        self.config_name = config_name
        self.dict = self._get_dict()

    def get(self, section, key, default=None):
        if section in self.dict:
            if key in self.dict[section]:
                return self.dict[section][key]
        return default

    def _get_dict(self):
        ret_dict = {}
        config = ConfigParser()
        config.read(CONFIG_DIR + self.config_name)
        for s in config.sections():
            ret_dict[s] = {}
            for o in config.options(s):
                ret_dict[s][o] = config.get(s, o, fallback='')

        return ret_dict

def get_all_configs():
    return os.listdir(CONFIG_DIR)

def config_is_exist(config_name):
    return os.path.exists(CONFIG_DIR + config_name)
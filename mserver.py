import importlib
import yaml


class Config:
    def __init__(self, path):
        self.config = {}
        self.load(path)

    def load(self, path):
        with open('config.yaml') as file:
            raw = yaml.load(file.read(), Loader=yaml.Loader)

        for module in raw['modules']:
            self.config[module] = {}
            default = raw['modules'][module]
            if default == None:
                default = {}
            for user in raw['users']:
                if module not in raw['users'][user]:
                    continue
                custom = raw['users'][user][module]
                if custom == None:
                    custom = {}
                self.config[module][user] = default | custom


class ModuleHandler:

    def __init__(self, config_path='config.yaml'):
        self.config = Config(config_path)
        self.modules = {}

    def __call__(self, name, *args, **kwargs):
        if name not in self.modules:
            self.load(name)
        return self.modules[name].procces(*args, **kwargs)

    def load(self, name):
        self.modules[name] = importlib.import_module(name)

    def reload(self, name):
        importlib.reload(self.modules[name])

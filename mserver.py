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

    def __getitem__(self, name):
        return self.config[name]



class Module:

    def __init__(self, name, config):
        self.config = config
        self.module = importlib.import_module(name)
        self.instances = {}

    def __getitem__(self, user):
        if user not in self.instances:
            self.instances[user] = self.module.prepare(self.config[user])
        return self.instances[user]

    def reload(self):
        self.instances = {}
        importlib.reload(self.module)



class ServiceHandler:

    def __init__(self, config_path):
        self.config = Config(config_path)
        self.modules = {}

    def __call__(self, name, user):
        if name not in self.modules:
            self.load(name)
        return self.modules[name][user]

    def load(self, name):
        self.modules[name] = Module(name, self.config[name])

    def reload(self, name):
        self.modules[name].reload()

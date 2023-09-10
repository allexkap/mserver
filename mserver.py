import importlib

class ModulesHandler:

    def __init__(self):
        self.modules = {}

    def __call__(self, name, *args, **kwargs):
        if name not in self.modules:
            self.load(name)
        return self.modules[name].procces(*args, **kwargs)

    def load(self, name):
        self.modules[name] = importlib.import_module(name)

    def reload(self, name):
        importlib.reload(self.modules[name])

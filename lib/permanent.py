import json

"""
Pattern for permanent objects
This object is given three things
f: a function to serialize its structure
rf: a function to deserialize its structure
k: the name of a file to save data in (in the data folder)
"""
class PermanentContext(object):
    def __init__(self, f, rf, k):
        self.key = k if k.startswith("data/") else "data/{}".format(k)
        self.f = f
        try:
            with open(self.key, "r", encoding="utf-8") as f:
                self.structure = rf(f.read())
        except:
            self.structure = {}
        self.is_open = True

    def __setattr__(self, name, value): 
        if name == "key" or name == "is_open" or name == "structure" or name == "f":
            super().__setattr__(name, value)
        else:
            if self.is_open == True:
                self.structure[name] = value
                self.update()

    def __getattr__(self, name):
        return self.structure[name]
    
    def __setitem__(self, name, value):
        self.__setattr__(name, value)

    def __getitem__(self, name):
        self.__getattr__(name)
    
    def __contains__(self, other):
        return other in self.structure.keys()

    def update(self):
        with open(self.key, "w", encoding="utf-8") as f:
            f.write(self.f(self.structure))

"""
Implementation of the PermanentContext class for json.
"""
class PermanentJsonContext(PermanentContext): 
    def __init__(self, key):
        super().__init__(json.dumps, json.loads, "{}.json".format(key))
    
    

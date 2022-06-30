import json
from re import A

from sympy import true
"""
Pattern for permanent objects
"""
class PermanentObject(object):
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
                with open(self.key, "w", encoding="utf-8") as f:
                    f.write(self.f(self.structure))

    def __getattr__(self, name):
        return self.structure[name]

class PermanentJsonContext(PermanentObject): 
    def __init__(self, key):
        super().__init__(json.dumps, json.loads, "{}.json".format(key))
    
    

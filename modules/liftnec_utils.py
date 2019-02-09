import os


def remove_none_key(data):
    new_data = {}
    for key in data.keys():
        if data[key]:
            new_data[key] = data[key]
    return new_data


class SequentialCode:
    def __init__(self):
        self.seq = 0

    def next(self, last=None):
        if last:
            self.seq = int(last)
        else:
            self.seq += 1
        return '%5d' % self.seq


class module_counter:
    def listModules(self):
        modules = []
        for module in os.listdir(os.path.dirname(__file__)):
            modules.insert(module)

        return modules

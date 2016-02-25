class SBDict(dict):
    def __init__(self):
        super(dict, self).__init__()

    def add(self, x):
        self.update(x)

    def remove(self, x):
        del self[x]

    def getKeys(self):
        return self.keys()

    def getValues(self):
        return self.values()

    def writeSbPairs(self, sbOut):
        import json
        with open('C:/Users/nschiff2/Documents/MWRDGC_WSRR/Optimatics/optimizer-hecras-integration/src' + sbOut, 'wb') as dumpFile:
            json.dump(self, dumpFile)

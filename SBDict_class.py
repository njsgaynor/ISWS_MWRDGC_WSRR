class SBDict(dict):
    def __init__(self):
        super(dict, self).__init__()

    def add(self, s, rlsrate):
        s.rlsrate = rlsrate
        self.update({s.getIdentifier(): s})

    def remove(self, x):
        del self[x]

    def getKeys(self):
        self.keys()

    def getArea(self, x):
        return self[x].area

    def getReleaseRate(self, x):
        return self[x].rlsrate

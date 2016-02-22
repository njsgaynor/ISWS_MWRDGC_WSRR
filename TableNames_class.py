class TableNames(list):
    def __init__(self):
        super(TableNames, self).__init__()

    def append(self, x):
        super(TableNames, self).append(x)

    def remove(self, x):
        super(TableNames, self).remove(x)

    def writeTableFile(self, tableOut):
        import pickle
        pickle.dump(self, tableOut)

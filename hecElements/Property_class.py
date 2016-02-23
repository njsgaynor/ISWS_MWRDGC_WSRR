class Property:
    def __init__(self, name):
        self.name = name
        self.value = None

    @classmethod
    def newProperty(cls, name, value):
        p = Property(name)
        p.setValue(value)
        return p

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getAsFloat(self):
        try:
            return float(self.value)
        except ValueError:
            print("Cannot convert to float.")

    def getAsString(self):
        try:
            return str(self.value)
        except ValueError:
            print("Cannot convert to string.")

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

import Element_class as Element
import Property_class as Property

class Diversion(Element):
    def __init__(self):
        super(Diversion, self).__init__('Diversion', None)
        self.downstream = Property(None)
        self.divertto = Property(None)
        self.staticProperties = [self.downstream.name, self.divertto.name]

    @classmethod
    def readDiversion(cls, currentLine, basinsrc, basinsink):
        d = Diversion()
        super(Diversion, d).deserialize(currentLine, basinsrc)
        d.serialize(basinsink)
        return d

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Diversion, self).add(self.downstream)
            elif a.getName() == self.divertto.getName():
                self.divertto.setValue(a.getValue())
                super(Diversion, self).add(self.divertto)
            else:
                super(Diversion, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            elif a.getName() == self.divertto.getName():
                self.divertto.setValue(None)
            else:
                try:
                    super(Diversion, self).remove(a)
                except LookupError:
                    print("Property not found.")

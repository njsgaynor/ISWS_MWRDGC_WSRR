import Element_class as Element
import Property_class as Property
import Pdata_class as Pdata
import TableNames_class as TableNames

class Reservoir(Element):
    def __init__(self):
        super(Reservoir, self).__init__('Reservoir', None)
        self.downstream = Property(None)
        self.storageoutflow = Property(None)
        self.staticProperties = [self.downstream.name, self.storageoutflow.name]

    @classmethod
    def readReservoir(cls, currentLine, basinsrc, basinsink):
        r = Reservoir()
        super(Reservoir, r).deserialize(currentLine, basinsrc)
        r.serialize(basinsink)
        return r

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Reservoir, self).add(self.downstream)
            elif a.getName() == self.storageoutflow.getName():
                self.storageoutflow.setValue(a.getValue())
                super(Reservoir, self).add(self.storageoutflow)
            else:
                super(Reservoir, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            elif a.getName() == self.storageoutflow.getName():
                self.storageoutflow.setValue(None)
            else:
                try:
                    super(Reservoir, self).remove(a)
                except LookupError:
                    print("Property not found.")

    @classmethod
    def newReservoir(cls, s, basinsink, pdatasink, dssfile, redevel, rlsrate):
        r = Reservoir()
        r.setIdentifier('Reservoir ' + s.getIdentifier())
        r.downstream = Property.newProperty('Downstream', 'J ' + s.getIdentifier())
        r.storageoutflow = Property.newProperty('Storage-Outflow Table', s.getIdentifier() + 'MWRD_' + str(redevel) +
                                                '_' + str(rlsrate))
        super(Reservoir, r).add(Property.newProperty('Canvas X', s.canvasx.getValue()))
        super(Reservoir, r).add(Property.newProperty('Canvas Y', s.canvasy.getValue()))
        super(Reservoir, r).add(r.downstream)
        super(Reservoir, r).add(Property.newProperty('Route', 'Modified Puls'))
        super(Reservoir, r).add(Property.newProperty('Routing Curve', 'Storage-Outflow'))
        super(Reservoir, r).add(Property.newProperty('Initial Outflow Equals Inflow', 'Yes'))
        super(Reservoir, r).add(r.storageoutflow)
        r.serialize(basinsink)
        Pdata.newPdata(r, pdatasink, dssfile)
        TableNames.append(r.storageoutflow.getAsString())
        return r

import Element_class as Element
import Property_class as Property
import Junction_class as Junction
import Reservoir_class as Reservoir
import copy

class Subbasin(Element):
    def __init__(self):
        super(Subbasin, self).__init__('Subbasin', None)
        self.area = Property('Area')
        self.downstream = Property('Downstream')
        self.curvenum = Property('Curve Number')
        self.impervious = Property('Percent Impervious Area')
        self.canvasx = Property('Canvas X')
        self.canvasy = Property('Canvas Y')
        self.canopy = Property('Canopy')
        self.staticProperties = [self.area.name, self.downstream.name, self.curvenum.name, self.impervious.name,
                                 self.canvasx.name, self.canvasy.name, self.canopy.name]

    @classmethod
    def readSubbasin(cls, currentLine, basinsrc, basinsink, pdatasink, dssfile, redevel, curvenum, rlsrate):
        s = Subbasin()
        super(Subbasin, s).deserialize(currentLine, basinsrc)
        s.divideSubbasin(basinsink, pdatasink, dssfile, redevel, curvenum, rlsrate)
        s.serialize(basinsink)
        return s

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.area.getName():
                self.area.setValue(a.getAsFloat())
                super(Subbasin, self).add(self.area)
            elif a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Subbasin, self).add(self.downstream)
            elif a.getName() == self.curvenum.getName():
                self.curvenum.setValue(a.getAsFloat())
                super(Subbasin, self).add(self.curvenum)
            elif a.getName() == self.impervious.getName():
                self.impervious.setValue(a.getAsFloat())
                super(Subbasin, self).add(self.impervious)
            elif a.getName() == self.canvasx.getName():
                self.canvasx.setValue(a.getValue())
                super(Subbasin, self).add(self.canvasx)
            elif a.getName() == self.canvasy.getName():
                self.canvasy.setValue(a.getValue())
                super(Subbasin, self).add(self.canvasy)
            elif a.getName() == self.canopy.getName():
                self.canopy.setValue(a.getValue())
                super(Subbasin, self).add(self.canopy)
            else:
                super(Subbasin, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.area.getName():
                self.area.setValue(None)
            elif a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            elif a.getName() == self.curvenum.getName():
                self.curvenum.setValue(None)
            elif a.getName() == self.impervious.getName():
                self.impervious.setValue(None)
            elif a.getName() == self.canvasx.getName():
                self.canvasx.setValue(None)
            elif a.getName() == self.canvasy.getName():
                self.canvasy.setValue(None)
            elif a.getName() == self.canopy.getName():
                self.canopy.setValue(None)
            else:
                try:
                    super(Subbasin, self).remove(a)
                except LookupError:
                    print("Property not found.")

    def divideSubbasin(self, basinsink, pdatasink, dssfile, redevel, curvenum, rlsrate):
        #may need to be modified once I figure out exactly how this will be used
        j = Junction.newJunction(self, basinsink)
        r = Reservoir.newReservoir(self, basinsink, pdatasink, dssfile, redevel, rlsrate)
        sNew = Subbasin.newSubbasin(self, basinsink, redevel, curvenum)
        self.area.setValue(self.area.getAsFloat() - sNew.area.getAsFloat())
        self.downstream.setValue('J ' + self.getIdentifier())

    @classmethod
    def newSubbasin(cls, s, basinsink, redevel, curvenum):
        sNew = copy.deepcopy(s)
        sNew.setIdentifier(s.getIdentifier() + 'MWRD')
        sNew.area.setValue((redevel / 100.) * s.area.getAsFloat())
        sNew.downstream.setValue('Reservoir ' + s.getIdentifier())
        sNew.canopy.setValue('SMA')
        # Define new canopy properties
        initCanopy = Property.newProperty('Initial Canopy Storage Percent', 0)
        maxCanopy = Property.newProperty('Canopy Maximum Storage', 0.52)
        endCanopy = Property.newProperty('End Canopy', '')
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, endCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, maxCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, initCanopy)
        sNew.curvenum.setValue(curvenum)
        sNew.serialize(basinsink)
        return sNew
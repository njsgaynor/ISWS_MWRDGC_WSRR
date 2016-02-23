import Element_class as Element
import Property_class as Property
import datetime
import calendar

class Pdata(Element):
    def __init__(self):
        super(Pdata, self).__init__('Table', None)
        self.dssfile = Property(None)
        self.pathname = Property(None)
        self.staticProperties = [self.dssfile.name, self.pathname.name]

    def newPdata(self, soname, pdatasink, dssfile):
        self.__init__()
        # Add a new storage-outflow table to pdata
        nowDT = datetime.today()
        nowDate = str(nowDT.day) + ' ' + calendar.month_name[nowDT.month] + ' ' + str(nowDT.year)
        nowTime = nowDT.hour + ':' + nowDT.minute + ':' + nowDT.second
        self.setIdentifier(soname)
        super(Pdata, self).add(Property.newProperty('Table Type', 'Storage-Outflow'))
        super(Pdata, self).add(Property.newProperty('Last Modified Date', str(nowDate)))
        super(Pdata, self).add(Property.newProperty('Last Modified Time', str(nowTime)))
        super(Pdata, self).add(Property.newProperty('X-Units', 'ACRE-FT'))
        super(Pdata, self).add(Property.newProperty('Y-Units', 'CFS'))
        super(Pdata, self).add(Property.newProperty('User External DSS File', 'NO'))
        super(Pdata, self).add(Property.newProperty('DSS File', dssfile))
        super(Pdata, self).add(Property.newProperty('Pathname', '//' + self.getIdentifier() + '/STORAGE-FLOW///TABLE/'))
        self.serialize(pdatasink)

# Jython 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date: February 2016

import sys
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/bin/java.exe")
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/src/java")
sys.path.append("C:/Program Files/Java/javahelp-2.0.05.jar")

import java.lang
import javax.help
import javax.swing as swing
import java.awt as awt
import datetime
import calendar
import copy
from operator import itemgetter

class Subwatershed(dict):

    # List of required keys for Subwatershed dict item
    # 'elements' is a list of type Element with one item for each element of Subwatershed
    _keys = ['watershed', 'subwatershed', 'basinin', 'basinout', 'pdatafile', 'dssfile', 'redevelopment', 'curvenumber',
             'releaserate', 'elements', 'pdata']

    @classmethod
    def getKeys(cls):
        return cls._keys

    def __init__(self):
        # Initialize this instance to None, then get properties from user
        for key in self._keys:
            self[key] = None
        self.chooseWatershed()
        self.getFilenames()
        self.getParams()
        self.initElements()

    def chooseWatershed(self):
        # GUI to choose the watershed and subwatershed
        self['watershed'] = None
        self['subwatershed'] = None

    def getFilenames(self):
        # GUI to get filename of *.basin file for reading - this is from the source version
        basinchoice = swing.JFileChooser()  #FileFilter="basin"
        #        filter = swing.JFileChooser.FileNameExtensionFilter("*.basin files",["basin"])
        #        basinin.addChoosableFileFilter(filter)
        #        basinin.SetFileFilter(FileNameExtensionFilter("basin"))
        basinfile = basinchoice.showOpenDialog(None)
        self['basinin'] = basinchoice.selectedFile

        # GUI to get filename of *.basin file for writing - this is for the new version
        basinchoice = swing.JFileChooser()
        basinfile = basinchoice.showOpenDialog(None)
        self['basinout'] = basinchoice.selectedFile

        # GUI to get filename of the *.pdata file - this is for the new version
        pdatachoice = swing.JFileChooser()
        pdatafile = pdatachoice.showOpenDialog(None)
        self['pdatafile'] = pdatachoice.selectedFile

        # GUI to get filename of the *.dss file - this is for the new version
        dsschoice = swing.JFileChooser()
        dssfile = dsschoice.showOpenDialog(None)
        self['dssfile'] = dsschoice.selectedFile

    def setParams(self, rd, cn, rr):
        # Save the future conditions parameters to the current instance of Subwatershed
        self['redevelopment'] = float(rd.getText())
        self['curvenumber'] = float(cn.getText())
        self['releaserate'] = float(rr.getText())

    def getParams(self):
        # GUI to get future % of subbasin redeveloped, curve number, and release rate
        # Initialize window for UI
        frame = swing.JFrame("Set conditions of redeveloped portion of subbasin", layout=awt.BorderLayout())
        frame.setDefaultCloseOperation(swing.JFrame.EXIT_ON_CLOSE)

        # Create panel that includes three text entry fields for % redeveloped, curve number, and release rate
        futureparams = swing.JPanel(layout=awt.GridLayout(3,2))
        inbutton = swing.JPanel()
        futureparams.add(swing.JLabel('Percent Redevelopment '))
        tf1 = futureparams.add(swing.JTextField())
        futureparams.add(swing.JLabel('Future Curve Number '))
        tf2 = futureparams.add(swing.JTextField())
        futureparams.add(swing.JLabel('Release Rate '))
        tf3 = futureparams.add(swing.JTextField())

        # Create panel for button that stores the values entered
        setButton = swing.JButton('Set parameters', actionPerformed=self.setParams(tf1, tf2, tf3))

        # Add panels to the window and make the window visible
        frame.add(futureparams, awt.BorderLayout.NORTH)
        inbutton.add(setButton)
        frame.add(inbutton, awt.BorderLayout.SOUTH)
        frame.pack()
        frame.setVisible(True)

    def initElements(self):
        self['elements'] = []


class Element(List):
    def __init__(self, category, identifier):
        # Initialize a generic Element with a category/name and an identifier/ID
        self.setCategory(category)
        self.setIdentifier(identifier)

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def getCategory(self):
        return self.category

    def setCategory(self, category):
        self.category = category

    def deserialize(self, currentLine, infile):
        lineList = currentLine.split(': ').strip()
        self.setIdentifier(lineList[1])
        # Read a single line and add the info to a new Property of an Element child class as long it is not an 'End:'
        # line. This is intended to be used only in the child classes in super() or overridden in the child class.
        currentLine = infile.readline(self)
        while not currentLine == 'End:':
            p = Property(None)
            lineList = currentLine.split(': ').strip()
            p.setName(lineList[0])
            p.setValue(lineList[1])
            self.add(p)

    def serialize(self, outfile):
        # Print Element object to file and then print 'End:'
        outfile.write('\n')
        for p in self:
            outfile.write(p[0],': ',p[1],'\n')
        outfile.write('End:\n')
        pass

    def add(self, a):
        # Adds a Property object to current instance of Element
        super(Element, self).append(a)

    def remove(self, a):
        # Removes a Property object from current instance of Element
        try:
            super(Element, self).remove(a)
        except LookupError:
            print("Property not found.")


class Basin(Element):
    def __init__(self, currentLine, basinsrc):
        super(Basin, self).__init__('Basin',None)
        super(Basin, self).deserialize(currentLine, basinsrc)


class Subbasin(Element):
    def __init__(self, currentLine, basinsrc, ws):
        super(Subbasin, self).__init__('Subbasin', None)
        self.area = Property('Area')
        self.downstream = Property('Downstream')
        self.curvenum = Property('Curve Number')
        self.impervious = Property('Percent Impervious Area')
        self.canvasx = Property('Canvas X')
        self.canvasy = Property('Canvas Y')
        self.canopy = Property('Canopy')
        self.staticProperties = [area.name, downstream.name, curvenum.name, impervious.name, canvasx.name, canvasy.name,
                                 canopy.name]
        super(Subbasin, self).deserialize(currentLine, basinsrc)
        self.divideSubbasin(ws)

    def add(self, a):
        if isinstance(a,Property):
            if a.getName == self.area.name:
                self.area.setValue(a.getValue())
                super(Subbasin, self).add(area)
            elif a.getName == self.downstream.name:
                self.downstream.setValue(a.getValue())
                super(Subbasin, self).add(downstream)
            elif a.getName == self.curvenum.name:
                self.curvenum.setValue(a.getValue())
                super(Subbasin, self).add(curvenum)
            elif a.getName == self.impervious.name:
                self.impervious.setValue(a.getValue())
                super(Subbasin, self).add(impervious)
            elif a.getName == self.canvasx.name:
                self.canvasx.setValue(a.getValue())
                super(Subbasin, self).add(canvasx)
            elif a.getName == self.canvasy.name:
                self.canvasy.setValue(a.getValue())
                super(Subbasin, self).add(canvasy)
            elif a.getName == self.canopy.name:
                self.canopy.setValue(a.getValue())
                super(Subbasin, self).add(canopy)
            else:
                super(Subbasin, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == self.area.name:
                self.area.setValue(None)
            elif a.getName == self.downstream.name:
                self.downstream.setValue(None)
            elif a.getName == self.curvenum.name:
                self.curvenum.setValue(None)
            elif a.getName == self.impervious.name:
                self.impervious.setValue(None)
            elif a.getName == self.canvasx.name:
                self.canvasx.setValue(None)
            elif a.getName == self.canvasy.name:
                self.canvasy.setValue(None)
            elif a.getName == self.canopy.name:
                self.canopy.setValue(None)
            else:
                try:
                    super(Subbasin, self).remove(a)
                except LookupError:
                    print("Property not found.")

    def divideSubbasin(self, ws):
        #may need to be modified once I figure out exactly how this will be used
        j = Junction.newJunction(self)
        r = Reservoir.newReservoir(self, ws)
        s = Subbasin.newSubbasin(self, ws)
        self.area.setValue(self.area.getAsFloat() - s.area.getAsFloat())
        self.downstream.setValue('J ' + self.downstream.getName())

    @classmethod
    def newSubbasin(cls, s, ws):
        sNew = copy.deepcopy(s)
        sNew.setIdentifier(s.getIdentifier + 'MWRD')
        sNew.area.setValue(ws['redevelopment'] * s.area)
        sNew.downstream.setValue('Reservoir ' + s.downstream)
        sNew.canopy.setValue('SMA')
        # Define new canopy properties
        initCanopy = Property.newProperty('Initial Canopy Storage Percent', 0)
        maxCanopy = Property.newProperty('Canopy Maximum Storage', 0.52)
        endCanopy = Property.newProperty('End Canopy', '')
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, endCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, maxCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, initCanopy)
        sNew.curvenum.setValue(ws['curvenumber'])


class Junction(Element):
    def __init__(self, currentLine, basinsrc):
        super(Junction, self).__init__('Junction', None)
        self.downstream = Property(None)
        self.staticProperties = [downstream.name]
        super(Junction, self).deserialize(currentLine, basinsrc)

    def add(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(a.getValue())
                super(Junction, self).add(self.downstream)
            else:
                super(Junction, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(None)
            else:
                try:
                    super(Junction, self).remove(a)
                except LookupError:
                    print("Property not found.")

    @classmethod
    def newJunction(cls, s):
        super(Junction, self).__init__('Junction', 'J ' + s.getIdentifier)
        downstream = Property(s.downstream)
        super(Junction, self).add(Property.newProperty('Canvas X', s.canvasx))
        super(Junction, self).add(Property.newProperty('Canvas Y', s.canvasy))
        super(Junction, self).add(downstream)


class Reservoir(Element):
    def __init__(self, currentLine, basinsrc):
        super(Reservoir, self).__init__('Reservoir', None)
        self.downstream = Property(None)
        self.storageoutflow = Property(None)
        self.staticProperties = [downstream.name, storageoutflow.name]
        super(Reservoir, self).deserialize(currentLine, basinsrc)

    def add(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(a.getValue())
                super(Reservoir, self).add(self.downstream)
            elif a.getName == storageoutflow.name:
                self.storageoutflow.setValue(a.getValue())
                super(Reservoir, self).add(self.storageoutflow)
            else:
                super(Reservoir, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(None)
            elif a.getName == storageoutflow.name:
                self.storageoutflow.setValue(None)
            else:
                try:
                    super(Reservoir, self).remove(a)
                except LookupError:
                    print("Property not found.")

    @classmethod
    def newReservoir(cls, s, ws):
        super(Reservoir, self).__init__('Reservoir', 'Reservoir ' + s.getIdentifier)
        downstream = Property('J ' + s.downstream)
        storageoutflow = Property('Storage-Outflow Table')
        storageoutflow.setValue(s.getIdentifier + 'MWRD_15_0l.15')
        super(Reservoir, self).add(Property.newProperty('Canvas X', s.canvasx))
        super(Reservoir, self).add(Property.newProperty('Canvas Y', s.canvasy))
        super(Reservoir, self).add(downstream)
        super(Reservoir, self).add(Property.newProperty('Route', 'Modified Puls'))
        super(Reservoir, self).add(Property.newProperty('Routing Curve', 'Storage-Outflow'))
        super(Reservoir, self).add(Property.newProperty('Initial Outflow Equals Inflow', 'Yes'))
        super(Reservoir, self).add(storageoutflow)
        newPdata(self, ws)


class Reach(Element):
    def __init__(self, currentLine, basinsrc):
        super(Reach, self).__init__('Reach', None)
        self.downstream = Property(None)
        self.staticProperties = [self.downstream.name]
        super(Reach, self).deserialize(currentLine, basinsrc)

    def add(self, a):
        if isinstance(a,Property):
            if a.getName == self.downstream.name:
                self.downstream.setValue(a.getValue())
                super(Reach, self).add(self.downstream)
            else:
                super(Reach, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(None)
            else:
                try:
                    super(Reach, self).remove(a)
                except LookupError:
                    print("Property not found.")


class Diversion(Element):
    def __init__(self, currentLine, basinsrc):
        super(Diversion, self).__init__('Diversion', None)
        self.downstream = Property(None)
        self.divertto = Property(None)
        self.staticProperties = [downstream.name, divertto.name]
        super(Diversion, self).deserialize(currentLine, basinsrc)

    def add(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(a.getValue())
                super(Diversion, self).add(self.downstream)
            elif a.getName == divertto.name:
                self.divertto.setValue(a.getValue())
                super(Diversion, self).add(self.divertto)
            else:
                super(Diversion, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(None)
            elif a.getName == divertto.name:
                self.divertto.setValue(None)
            else:
                try:
                    super(Diversion, self).remove(a)
                except LookupError:
                    print("Property not found.")


class Sink(Element):
    def __init__(self, currentLine, basinsrc):
        super(Sink, self).__init__('Sink', None)
        super(Sink, self).deserialize(currentLine, basinsrc)


class BasinSchema(Element):
    def __init__(self, currentLine, basinsrc):
        super(BasinSchema, self).__init__('Basin Schematic Properties', None)
        super(BasinSchema, self).deserialize(currentLine, basinsrc)


class Pdata(Element):
    def __init__(self):
        super(Pdata, self).__init__('Table', None)
        self.dssfile = Property(None)
        self.pathname = Property(None)
        self.staticProperties = [dssfile.name, pathname.name]

    def newPdata(self, r, ws):
        self.__init__()
        # Add a new storage-outflow table to pdata
        nowDT = datetime.today()
        nowDate = str(nowDT.day) + ' ' + calendar.month_name[nowDT.month] + ' ' + str(nowDT.year)
        nowTime = nowDT.hour + ':' + nowDT.minute + ':' + nowDT.second
        self.setIdentifier(r.storageoutflow.getAsString())
        Property.newProperty('Table Type', 'Storage-Outflow')
        Property.newProperty('Last Modified Date', str(nowDate))
        Property.newProperty('Last Modified Time', str(nowTime))
        Property.newProperty('X-Units', 'ACRE-FT')
        Property.newProperty('Y-Units', 'CFS')
        Property.newProperty('User External DSS File', 'NO')
        Property.newProperty('DSS File', ws['dssfile'])
        Property.newProperty('Pathname', '//' + self.getIdentifier() + '/STORAGE-FLOW///TABLE/')


class Property:
    def __init__(self, name):
        setName(name)
        setValue(None)

    @classmethod
    def newProperty(self, name, value):
        setName(name)
        setValue(value)

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


class UpdateSubwatershed(self, basinin):    #Driver class
    def __init__(self):
        ws = Subwatershed()
        readBasinFile(ws)
        writeBasinFile(ws)
        updatePdataFile(ws['pdata'])

    # Open *.basin source file and read it line by line. Store each basin element (i.e. Junction, Reservoir,
    # Subbasin, etc.) separately as an object of the corresponding type.
    def readBasinFile(self, ws):
        with open(ws['basinin'], 'r') as basinsrc:
            recordnum = 0
            currentLine = ' '
            while not currentLine == '':
                try:
                    currentLine = basinsrc.readline()
                    if(currentLine == "End:"):
                        recordnum += 1
                    elif currentLine == '\n':
                        pass
                    elif currentLine.startswith('Basin:'):
                        b = Basin(currentLine, basinsrc)
                    elif currentLine.startswith('Subbasin:'):
                        b = Subbasin(currentLine, basinsrc, ws)
                    elif currentLine.startswith('Junction:'):
                        b = Junction(currentLine, basinsrc)
                    elif currentLine.startswith('Reservoir:'):
                        b = Reservoir(currentLine, basinsrc)
                    elif currentLine.startswith('Reach:'):
                        b = Reach(currentLine, basinsrc)
                    elif currentLine.startswith('Diversion:'):
                        b = Diversion(currentLine, basinsrc)
                    elif currentLine.startswith('Sink:'):
                        b = Sink(currentLine, basinsrc)
                    elif currentLine.startswith('Basin Schematic Properties:'):
                        b = BasinSchema(currentLine, basinsrc)
                    elif currentLine == '':
                        print("End of file " + ws['basinin'] + ".")
                        return
                    else:
                        print(currentLine)
                        raise RuntimeError("Invalid subwatershed element. Check input *.basin file.")
                except IOError:
                    print("Cannot read file " + ws['basinin'] + ".")
                    return
                ws['elements'].append(b)

    # Write info to *.basin sink file and *.pdata
    def writeBasinFile(self, ws):
        with open(ws['basinout'],'w') as basinsink:
            ws['elements'].serialize(basinsink)

    # Add Storage-Outflow entry for new subbasin to *.pdata file
    def updatePdataFile(self, pdata):
        with open(pdata, 'w') as pdatasink:
            ws['pdatafile'].serialize(pdatasink)


if __name__=="__main__":
    UpdateSubwatershed()

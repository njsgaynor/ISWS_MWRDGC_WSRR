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
from operator import itemgetter

class Subwatershed(dict):

    # List of required keys for Subwatershed dict item
    _keys = ['watershed', 'subwatershed', 'basinin', 'basinout', 'pdata', 'redevelopment', 'curvenumber', 'releaserate',
             'elements']    # 'elements' is a list of type Element with one item for each element of Subwatershed

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
#        self.modBasin()
#        self.modPdata()

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
        pdatafile = pdata.showOpenDialog(None)
        self['pdata'] = pdatachoice.selectedFile

    def setParams(self, rd, cn, rr):
        # Save the future conditions parameters to the current instance of Subwatershed
        self['redevelopment'] = float(rd.getText())
        self['curvenumber'] = float(cn.getText())
        self['releaserate'] = float(rr.getText())
        print(self['releaserate'])

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
        setCategory(category)
        setIdentifier(identifier)

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
            super(Element, List).append(p)

    def serialize(self, outfile):
        # Print Element object to file and then print 'End:'
        outfile.write('\n')
        for p in Subwatershed['elements']:
            outfile.write(p[0],': ',p[1],'\n')
        outfile.write('End:\n')
        pass

    def add(self, a):
        list.append(a)

    def remove(self, a):
        try:
            list.remove(a)
        except LookupError:
            print("Property not found.")

    def copy(self, a):
        # Copy properties to a new instance of Element
        Subwatershed['elements'].list.append(a)


class Basin(Element):
    def __init__(self, currentLine, basinsrc):
        super(Basin, Element).__init__('Basin',None)
        super(Basin, Element).deserialize(currentLine, basinsrc)


class Subbasin(Element):
    def __init__(self, currentLine, basinsrc):
        super(Subbasin, Element).__init__('Subbasin',None)
        self.area = Property('Area')
        self.downstream = Property('Downstream')
        self.curvenum = Property('Curve Number')
        self.impervious = Property('Percent Impervious Area')
        self.canvasx = Property('Canvas X')
        self.canvasy = Property('Canvas Y')
        self.canopy = Property('Canopy')
        self.staticProperties = [area.name, downstream.name, curvenum.name, impervious.name, canvasx.name, canvasy.name,
                                 canopy.name]
        self.deserialize(currentLine, basinsrc)

    def deserialize(self, currentLine, infile):
        lineList = currentLine.split(': ').strip()
        self.setIdentifier(lineList[1])
        # Read a single line and add the info to a new Property of Subbasin as long it is not an 'End:' line
        currentLine = infile.readline(self)
        while not currentLine == 'End:':
            p = Property(None)
            lineList = currentLine.split(': ').strip()
            p.setName(lineList[0])
            p.setValue(lineList[1])
            self.add(p)

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

    def divideSubbasin(self, areaval, dsval, cnval, impval):
        #may need to be modified once I figure out exactly how this will be used
        s = Subbasin.newSubbasin(self)
        j = Junction.newJunction(self)
        r = Reservoir.newReservoir(self)
        self.area.setValue(self.area.getAsFloat() - s.area.getAsFloat())
        self.downstream.setValue('J ' + self.downstream.getName())

    @classmethod
    def newSubbasin(cls, s):
        super(Subbasin, self).copy(s)
        self.setIdentifier(s.getIdentifier + 'MWRD')
        self.area.setValue(Subwatershed['redevelopment'] * s.area)
        self.downstream.setValue('Reservoir ' + s.downstream)
        self.canopy.setValue('SMA')
        #need to add insert() to Element
        self.list.insert(self.list.index(self.canopy) + 1, [['Initial Canopy Storage Percent', 0],['Canopy Maximum Storage',
                                                                                               0.52],['End Canopy','']])
        self.curvenum.setValue(Subwatershed['curvenumber'])


class Junction(Element):
    def __init__(self, currentLine, basinsrc):
        super(Junction, self).__init__('Junction', None)
        downstream = Property(None)
        self.staticProperties = [downstream.name]
        self.deserialize(currentLine, basinsrc)

    def deserialize(self, currentLine, infile):
        lineList = currentLine.split(': ').strip()
        self.setIdentifier(lineList[1])
        # Read a single line and add the info to a new Property of Subbasin as long it is not an 'End:' line
        currentLine = infile.readline(self)
        while not currentLine == 'End:':
            p = Property(None)
            lineList = currentLine.split(': ').strip()
            p.setName(lineList[0])
            p.setValue(lineList[1])
            self.add(p)

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
        downstream = Property(None)
        storageoutflow = Property(None)
        self.staticProperties = [downstream.name, storageoutflow.name]
        self.deserialize(currentLine, basinsrc)

    def deserialize(self, currentLine, infile):
        lineList = currentLine.split(': ').strip()
        self.setIdentifier(lineList[1])
        # Read a single line and add the info to a new Property of Subbasin as long it is not an 'End:' line
        currentLine = infile.readline(self)
        while not currentLine == 'End:':
            p = Property(None)
            lineList = currentLine.split(': ').strip()
            p.setName(lineList[0])
            p.setValue(lineList[1])
            self.add(p)

    def add(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(a.getValue())
                super(Reservoir, self).append(self.downstream)
            elif a.getName == storageoutflow.name:
                self.storageoutflow.setValue(a.getValue())
                super(Reservoir, self).add(self.storageoutflow)
            else:
                super(Reservoir, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
                self.downstream.setValue(None)
                super(Element, self).add(self.downstream)
            elif a.getName == storageoutflow.name:
                self.storageoutflow.setValue(None)
            else:
                try:
                    super(Reservoir, self).remove(a)
                except LookupError:
                    print("Property not found.")

    @classmethod
    def newReservoir(cls, s):
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

class Reach(Element):
    def __init__(self, currentLine, basinsrc):
        super(Reach, self).__init__('Reach', None)
        downstream = Property(None)
        self.staticProperties = [downstream.name]
        self.deserialize(currentLine, basinsrc)

    def deserialize(self, currentLine, infile):
        lineList = currentLine.split(': ').strip()
        self.setIdentifier(lineList[1])
        # Read a single line and add the info to a new Property of Subbasin as long it is not an 'End:' line
        currentLine = infile.readline(self)
        while not currentLine == 'End:':
            p = Property(None)
            lineList = currentLine.split(': ').strip()
            p.setName(lineList[0])
            p.setValue(lineList[1])
            self.add(p)

    def add(self, a):
        if isinstance(a,Property):
            if a.getName == downstream.name:
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
                    super(Reach,self).remove(a)
                except LookupError:
                    print("Property not found.")

class Diversion(Element):
    def __init__(self, currentLine, basinsrc):
        super(Diversion, self).__init__('Diversion', None)
        downstream = Property(None)
        divertto = Property(None)
        self.staticProperties = [downstream.name, divertto.name]
        self.deserialize(currentLine, basinsrc)

    def deserialize(self, currentLine, infile):
        lineList = currentLine.split(': ').strip()
        self.setIdentifier(lineList[1])
        # Read a single line and add the info to a new Property of Subbasin as long it is not an 'End:' line
        currentLine = infile.readline(self)
        while not currentLine == 'End:':
            p = Property(None)
            lineList = currentLine.split(': ').strip()
            p.setName(lineList[0])
            p.setValue(lineList[1])
            self.add(p)

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
        super(Sink, Element).deserialize(currentLine, basinsrc)

class BasinSchema(Element):
    def __init__(self, currentLine, basinsrc):
        super(BasinSchema, self).__init__('Basin Schematic Properties', None)
        super(BasinSchema, Element).deserialize(currentLine, basinsrc)

class Property:
    def __init__(self, name):
        setName(name)
        setValue(None)

    @classmethod
    def newProperty(self, name, value):
        setName(name)
        setValue(value)

    def getValue(self):
        return value

    def setValue(self, value):
        self.value = value

    def getAsFloat(self):
        try:
            return float(value)
        except ValueError:
            print("Cannot convert to float.")

    def getAsString(self):
        try:
            return str(value)
        except ValueError:
            print("Cannot convert to string.")

    def getName(self):
        return name

    def setName(self, name):
        self.name = name


class UpdateSubwatershed(self, basinin):    #Driver class
    def __init__(self):
        ws = Subwatershed()
        readBasinFile(ws['basinin'])
        updateBasinFile(ws['basinout'])
        updatePdataFile(ws['pdata'])

    # Open *.basin source file and read it line by line. Store each basin element (i.e. Junction, Reservoir,
    # Subbasin, etc.) separately as an object of the corresponding type.
    def readBasinFile(self, basinin):
        with open(basinin.selectedFile, 'r') as basinsrc:
            recordnum = 0
            try:
                currentLine = basinsrc.readline()
                if(currentLine == "End:"):
                    recordnum += 1
                elif currentLine.startswith('Basin:'):
                    b = Basin(currentLine, basinsrc)
                elif currentLine.startswith('Subbasin:'):
                    s = Subbasin(currentLine, basinsrc)
                elif currentLine.startswith('Junction:'):
                    j = Junction(currentLine, basinsrc)
                elif currentLine.startswith('Reservoir:'):
                    r = Reservoir(currentLine, basinsrc)
                elif currentLine.startswith('Reach:'):
                    r = Reach(currentLine, basinsrc)
                elif currentLine.startswith('Diversion:'):
                    d = Diversion(currentLine, basinsrc)
                elif currentLine.startswith('Sink:'):
                    s = Sink(currentLine, basinsrc)
                elif currentLine.startswith('Basin Schematic Properties:'):
                    b = BasinSchema(currentLine, basinsrc)
            except RuntimeError:
                print("Invalid subwatershed element. Check input *.basin file.")
                pass

    # Write info to *.basin sink file and *.pdata
    def updateBasinFile(self, basinout):
        with open(basinout,'w') as basinsink:
            pass

    # Add Storage-Outflow entry for new subbasin to *.pdata file
    def updatePdataFile(self, pdata):
        with open(pdata, 'w') as pdatasink:
            pass


if __name__=="__main__":
    UpdateSubwatershed()

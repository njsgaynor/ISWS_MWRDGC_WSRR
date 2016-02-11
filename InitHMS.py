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

    def deserialize(self, infile):
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

    def copy(self, category):
        # Copy properties to a new instance of Element
        Subwatershed['elements'].list.append(Subwatershed['elements'])


class Basin(Element):
    def __init__(self):
        super(Basin, Element).__init__('Basin',None)

    def add(self):
        pass

    def remove(self):
        pass


class Subbasin(Element):
    def __init__(self, basinsrc):
        super(Subbasin, Element).__init__('Subbasin',None)
        self.area = Property('Area')
        self.downstream = Property('Downstream')
        self.curvenum = Property('Curve Number')
        self.impervious = Property('Percent Impervious Area')
        self.staticProperties = [area.name, downstream.name, curvenum.name, impervious.name]
        self.deserialize(basinsrc)

    def deserialize(self, infile):
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
            if a.getName == area.name:
                self.area.setValue(a.getValue())
                super(Subbasin, List).append(self.area)
            elif a.getName == downstream.name:
                self.downstream.setValue(a.getValue())
                super(Subbasin, List).append(self.downstream)
            elif a.getName == curvenum.name:
                self.curvenum.setValue(a.getValue())
                super(Subbasin, List).append(self.curvenum)
            elif a.getName == impervious.name:
                self.impervious.setValue(a.getValue())
                super(Subbasin, List).append(self.impervious)
            else:
                super(Subbasin,List).append(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == 'area':
                self.area = None

    def updateSubbasin(self, areaval, dsval, cnval, impval):
        #may need to be modified once I figure out exactly how this will be used
        self.area.setValue(areaval)
        self.downstream.setValue(dsval)
        self.curvenum.setValue(cnval)
        self.impervious.setValue(impval)


class Junction(Element):
    def __init__(self):
        super(Junction, self).__init__('Junction', None)
        downstream = Property(None)

class Reservoir(Element):
    def __init__(self):
        super(Reservoir, self).__init__('Reservoir', None)
        downstream = Property(None)
        storageoutflow = Property(None)

class Reach(Element):
    def __init__(self):
        super(Reach, self).__init__('Reach', None)
        downstream = Property(None)

class Diversion(Element):
    def __init__(self):
        super(Diversion, self).__init__('Diversion', None)
        downstream = Property(None)
        divertto = Property(None)

class Sink(Element):
    def __init__(self):
        super(Sink, self).__init__('Sink', None)

class BasinSchema(Element):
    def __init__(self):
        super(BasinSchema, self).__init__('Basin Schematic Properties', None)

class Property:
    def __init__(self, name):
        setName(name)
        setValue(None)

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


class UpdateSubwatershed(self, basinin):
    # Open *.basin source file and read it line by line. Store each basin element (i.e. Junction, Reservoir,
    # Subbasin, etc.) separately as an object of the corresponding type.
    def startRead(self):
        with open(basinin.selectedFile, 'r') as basinsrc:
            recordnum = 0
            try:
                x = basinsrc.readline()
                if(x == "End:"):
                    recordnum += 1
                elif x.startswith('Basin:'):
                    b = Basin()
                    b.deserialize(basinsrc)
                elif x.startswith('Subbasin:'):
                    s = Subbasin(basinsrc)
                elif x.startswith('Junction:'):
                    j = Junction()
                    j.deserialize(basinsrc)
                elif x.startswith('Reservoir:'):
                    r = Reservoir()
                    r.deserialize(basinsrc)
                elif x.startswith('Reach:'):
                    r = Reach()
                    r.deserialize(basinsrc)
                elif x.startswith('Diversion:'):
                    d = Diversion()
                    d.deserialize(basinsrc)
                elif x.startswith('Sink:'):
                    s = Sink()
                    s.deserialize(basinsrc)
                elif x.startswith('Basin Schematic Properties:'):
                    b = BasinSchema()
                    b.deserialize(basinsrc)
            except RuntimeError:
                print("Invalid subwatershed element. Check input *.basin file.")
                pass

    # Add junction to each subbasin in *.basin sink file - this will be the downstream element for both portions of the
    # subbasin. Use the current downstream element for the junction.
    def addJunction(self, x):
        y = x.split(': ').strip()
        pass

    # Add a reservoir to each subbasin in *.basin sink file
    def addReservoir(self, x):
        pass

    # Update portion of each subbasin corresponding to % of redevelopment, using future CN and RR, in *.basin sink file
    def addPostdevSubbasin(self, x):
        pass

    # Add the portion of the subbasin that has not been redeveloped
    def addPredevSubbasin(self, x):
        pass

    # Add Storage-Outflow entry for new subbasin to *.pdata file
    def updatePdata(self, pdata):
        with open(pdata.selectedFile, 'w') as pdatasink:
            pass

    # Write info to *.basin sink file and *.pdata
    def updateBasin(self, basinin):
        with open(basinout.selectedFile,'w') as basinsink:
            pass



if __name__=="__main__":
    getFuture()
    pullBasinElements()

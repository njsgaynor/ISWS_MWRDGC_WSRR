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
        default_path = 'C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek/Stony_V1.0/HydrologicModels/ExistingConditions/LucasDitch/LUDT_DesignRuns'
        # GUI to get filename of *.basin file for reading - this is from the source version
        basinchoice = swing.JFileChooser(default_path)  #FileFilter="basin"
        #        filter = swing.JFileChooser.FileNameExtensionFilter("*.basin files",["basin"])
        #        basinin.addChoosableFileFilter(filter)
        basinchoice.setDialogTitle('Choose the source *.basin file (old version)')
#        basinchoice.SetFileFilter(FileNameExtensionFilter('*.basin files', 'basin'))
        basinfile = basinchoice.showOpenDialog(None)
        self['basinin'] = str(basinchoice.selectedFile)

        # GUI to get filename of *.basin file for writing - this is for the new version
        basinchoice = swing.JFileChooser(default_path)
        basinchoice.setDialogTitle('Choose the sink *.basin file (new version)')
        basinfile = basinchoice.showOpenDialog(None)
        self['basinout'] = str(basinchoice.selectedFile)

        # GUI to get filename of the *.pdata file - this is for the new version
        pdatachoice = swing.JFileChooser(default_path)
        basinchoice.setDialogTitle('Choose the *.pdata file (new version)')
        pdatafile = pdatachoice.showOpenDialog(None)
        self['pdatafile'] = str(pdatachoice.selectedFile)

        # GUI to get filename of the *.dss file - this is for the new version
        dsschoice = swing.JFileChooser(default_path)
        basinchoice.setDialogTitle('Choose the *.dss file (new version)')
        dssfile = dsschoice.showOpenDialog(None)
        self['dssfile'] = str(dsschoice.selectedFile)

    def setParams(self, rd, cn, rr, frame):
        # Save the future conditions parameters to the current instance of Subwatershed
        self['redevelopment'] = float(15) #rd.text #float(rd.text)
        self['curvenumber'] = float(88) #cn.text #float(cn.text)
        self['releaserate'] = float(0.15) #rr.text #float(rr.text)
        print('setParams')
        frame.dispose()
#        self.initElements()
#        readBasinFile(self['basinin'], self['basinout'])

    def getParams(self):
        # GUI to get future % of subbasin redeveloped, curve number, and release rate
        # Initialize window for UI
        frame = swing.JFrame("Set conditions of redeveloped portion of subbasin", layout=awt.BorderLayout())
        frame.setDefaultCloseOperation(swing.JFrame.EXIT_ON_CLOSE)

        # Create panel that includes three text entry fields for % redeveloped, curve number, and release rate
        futureparams = swing.JPanel(layout=awt.GridLayout(3,2))
        inbutton = swing.JPanel()
        futureparams.add(swing.JLabel('Percent Redevelopment '))
        rd = swing.JTextField('', 5)
        futureparams.add(rd)
        futureparams.add(swing.JLabel('Future Curve Number '))
        cn = swing.JTextField('', 5)
        futureparams.add(cn)
        futureparams.add(swing.JLabel('Release Rate '))
        rr = swing.JTextField('', 5)
        futureparams.add(rr)

        # Create panel for button that stores the values entered
        setButton = swing.JButton('Set parameters', actionPerformed=(lambda x: self.setParams(rd, cn, rr, frame)))

        # Add panels to the window and make the window visible
        frame.add(futureparams, awt.BorderLayout.NORTH)
        inbutton.add(setButton)
        frame.add(inbutton, awt.BorderLayout.SOUTH)
#        setButton.addMouseListener(awt.event.MouseListener.mouseClicked(self, self.setParams(rd, cn, rr, frame)))
        frame.pack()
        frame.setVisible(True)

    def initElements(self):
        self['elements'] = []
        print('init elements')


class Element(list):
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
        lineList = currentLine.strip('\n').strip().split(': ')
        try:
            self.setIdentifier(lineList[1])
        except IndexError:
            print(lineList)
            self.setIdentifier('')
        # Read a single line and add the info to a new Property of an Element child class as long it is not an 'End:'
        # line. This is intended to be used only in the child classes in super() or overridden in the child class.
        currentLine = infile.readline()
        while not currentLine == 'End:\n':
            if not currentLine == '\n':
                p = Property(None)
                lineList = currentLine.strip('\n').strip().split(': ')
                p.setName(lineList[0])
                try:
                    p.setValue(lineList[1])
                except IndexError:
                    print(lineList)
                    p.setValue('')
                self.__class__.add(self, p)
                currentLine = infile.readline()
            else:
                currentLine = infile.readline()

    def serialize(self, outfile):
        # Print Element object to file and then print 'End:'
        outfile.write(self.getCategory() + ': ' + self.getIdentifier() + '\n')
        for line in self:
            outfile.write('    ' + line.getName() + ': ' + line.getAsString() + '\n')
        outfile.write('End:\n')
        outfile.write('\n')
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
    def __init__(self):
        super(Basin, self).__init__('Basin', None)

    @classmethod
    def readBasin(cls, currentLine, basinsrc):
        b = Basin()
        super(Basin, b).deserialize(currentLine, basinsrc)
        return b


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
    def readSubbasin(cls, currentLine, basinsrc, redevel, curvenum, rlsrate):
        s = Subbasin()
        super(Subbasin, s).deserialize(currentLine, basinsrc)
        s.divideSubbasin(redevel, curvenum, rlsrate)
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

    def divideSubbasin(self, redevel, curvenum, rlsrate):
        #may need to be modified once I figure out exactly how this will be used
        j = Junction.newJunction(self)
        r = Reservoir.newReservoir(self)
        sNew = Subbasin.newSubbasin(self, redevel, curvenum)
        self.area.setValue(self.area.getAsFloat() - sNew.area.getAsFloat())
        self.downstream.setValue('J ' + self.downstream.getName())

    @classmethod
    def newSubbasin(cls, s, redevel, curvenum):
        sNew = copy.deepcopy(s)
        sNew.setIdentifier(s.getIdentifier() + 'MWRD')
        sNew.area.setValue(redevel * s.area.getAsFloat())
        sNew.downstream.setValue('Reservoir ' + s.downstream.getAsString())
        sNew.canopy.setValue('SMA')
        # Define new canopy properties
        initCanopy = Property.newProperty('Initial Canopy Storage Percent', 0)
        maxCanopy = Property.newProperty('Canopy Maximum Storage', 0.52)
        endCanopy = Property.newProperty('End Canopy', '')
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, endCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, maxCanopy)
        super(Subbasin, sNew).insert(super(Subbasin, sNew).index(sNew.canopy) + 1, initCanopy)
        sNew.curvenum.setValue(curvenum)
        return sNew


class Junction(Element):
    def __init__(self):
        super(Junction, self).__init__('Junction', None)
        self.downstream = Property(None)
        self.staticProperties = [self.downstream.name]

    @classmethod
    def readJunction(cls, currentLine, basinsrc):
        j = Junction()
        super(Junction, j).deserialize(currentLine, basinsrc)
        return j

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Junction, self).add(self.downstream)
            else:
                super(Junction, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == downstream.getName():
                self.downstream.setValue(None)
            else:
                try:
                    super(Junction, self).remove(a)
                except LookupError:
                    print("Property not found.")

    @classmethod
    def newJunction(cls, s):
        j = Junction()
        j.setIdentifier('J ' + str(s.getIdentifier()))
        j.downstream = s.downstream
        p = Property.newProperty('Canvas X', s.canvasx.getValue())
        super(Junction, j).add(Property.newProperty('Canvas X', s.canvasx.getValue()))
        super(Junction, j).add(Property.newProperty('Canvas Y', s.canvasy.getValue()))
        super(Junction, j).add(j.downstream)
        return j


class Reservoir(Element):
    def __init__(self):
        super(Reservoir, self).__init__('Reservoir', None)
        self.downstream = Property(None)
        self.storageoutflow = Property(None)
        self.staticProperties = [self.downstream.name, self.storageoutflow.name]

    @classmethod
    def readReservoir(cls, currentLine, basinsrc):
        r = Reservoir()
        super(Reservoir, j).deserialize(currentLine, basinsrc)
        return r

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Reservoir, self).add(self.downstream)
            elif a.getName() == storageoutflow.getName():
                self.storageoutflow.setValue(a.getValue())
                super(Reservoir, self).add(self.storageoutflow)
            else:
                super(Reservoir, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == downstream.getName():
                self.downstream.setValue(None)
            elif a.getName() == storageoutflow.getName():
                self.storageoutflow.setValue(None)
            else:
                try:
                    super(Reservoir, self).remove(a)
                except LookupError:
                    print("Property not found.")

    @classmethod
    def newReservoir(cls, s):
        r = Reservoir()
        r.setIdentifier('Reservoir ' + s.getIdentifier())
        r.downstream = Property.newProperty('Downstream', 'J ' + s.downstream.getAsString())
        storageoutflow = Property.newProperty('Storage-Outflow Table', s.getIdentifier() + 'MWRD_15_0l.15')
        super(Reservoir, r).add(Property.newProperty('Canvas X', s.canvasx.getValue()))
        super(Reservoir, r).add(Property.newProperty('Canvas Y', s.canvasy.getValue()))
        super(Reservoir, r).add(r.downstream)
        super(Reservoir, r).add(Property.newProperty('Route', 'Modified Puls'))
        super(Reservoir, r).add(Property.newProperty('Routing Curve', 'Storage-Outflow'))
        super(Reservoir, r).add(Property.newProperty('Initial Outflow Equals Inflow', 'Yes'))
        super(Reservoir, r).add(r.storageoutflow)
#        newPdata(self, ws)
        return r


class Reach(Element):
    def __init__(self):
        super(Reach, self).__init__('Reach', None)
        self.downstream = Property(None)
        self.staticProperties = [self.downstream.name]

    @classmethod
    def readReach(cls, currentLine, basinsrc):
        r = Reach()
        super(Reach, r).deserialize(currentLine, basinsrc)
        return r

    def add(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(a.getValue())
                super(Reach, self).add(self.downstream)
            else:
                super(Reach, self).add(a)

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName() == self.downstream.getName():
                self.downstream.setValue(None)
            else:
                try:
                    super(Reach, self).remove(a)
                except LookupError:
                    print("Property not found.")


class Diversion(Element):
    def __init__(self):
        super(Diversion, self).__init__('Diversion', None)
        self.downstream = Property(None)
        self.divertto = Property(None)
        self.staticProperties = [self.downstream.name, self.divertto.name]

    @classmethod
    def readDiversion(cls, currentLine, basinsrc):
        d = Diversion()
        super(Diversion, d).deserialize(currentLine, basinsrc)
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


class Sink(Element):
    def __init__(self):
        super(Sink, self).__init__('Sink', None)

    @classmethod
    def readSink(cls, currentLine, basinsrc):
        s = Sink()
        super(Sink, s).deserialize(currentLine, basinsrc)
        return s


class BasinSchema(Element):
    def __init__(self):
        super(BasinSchema, self).__init__('Basin Schematic Properties', None)

    @classmethod
    def readBasinSchema(cls, currentLine, basinsrc):
        b = BasinSchema()
        super(BasinSchema, b).deserialize(currentLine, basinsrc)
        return b


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


class UpdateSubwatershed():    #Driver class

    # Open *.basin source file and read it line by line. Store each basin element (i.e. Junction, Reservoir,
    # Subbasin, etc.) separately as an object of the corresponding type.
    # Write info to *.basin sink file and *.pdata
    # Add Storage-Outflow entry for new subbasin to *.pdata file
    pass


def updatePdataFile(ws):
    with open(pdata, 'w') as pdatasink:
        ws['pdatafile'].serialize(pdatasink)


def readBasinFile(basinin, basinout, redevel, curvenum, rlsrate):
    with open(basinin, 'r') as basinsrc, open(basinout, 'wb') as basinsink:
        recordnum = 0
        currentLine = ' '
        while not currentLine == '':
            try:
                currentLine = basinsrc.readline()
                if(currentLine == "End:"):
                    b.serialize(basinsink)
                    recordnum += 1
                elif currentLine == '\n':
                    pass
                elif currentLine.startswith('Basin:'):
                    b = Basin.readBasin(currentLine, basinsrc)
                elif currentLine.startswith('Subbasin:'):
                    b = Subbasin.readSubbasin(currentLine, basinsrc, redevel, curvenum, rlsrate)
                elif currentLine.startswith('Junction:'):
                    b = Junction.readJunction(currentLine, basinsrc)
                elif currentLine.startswith('Reservoir:'):
                    b = Reservoir.readReservoir(currentLine, basinsrc)
                elif currentLine.startswith('Reach:'):
                    b = Reach.readReach(currentLine, basinsrc)
                elif currentLine.startswith('Diversion:'):
                    b = Diversion.readDiversion(currentLine, basinsrc)
                elif currentLine.startswith('Sink:'):
                    b = Sink.readSink(currentLine, basinsrc)
                elif currentLine.startswith('Basin Schematic Properties:'):
                    b = BasinSchema.readBasinSchema(currentLine, basinsrc)
                elif currentLine == '':
                    print("End of file " + basinin + ".")
                    return
                else:
                    print(currentLine)
                    raise RuntimeError("Invalid subwatershed element. Check input *.basin file.")
            except IOError:
                print("Cannot read file " + basinin + " or " + basinout + ".")
                return
#            elements.append(b)


def writeBasinFile(**ws):
    print(ws['basinout'])
    with open(ws['basinout'],'w') as basinsink:
        ws['elements'].serialize(basinsink)


if __name__=="__main__":
    ws = Subwatershed()
    readBasinFile(ws['basinin'], ws['basinout'], ws['redevelopment'], ws['curvenumber'], ws['releaserate'])
    print('Program finished successfully.')
#    writeBasinFile(ws)
#    updatePdataFile(ws['pdata'])

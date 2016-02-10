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

    _keys = ['watershed', 'subwatershed', 'basinin', 'basinout', 'pdata', 'redevelopment', 'curvenumber', 'releaserate']

    def __init__(self):
        for key in self._keys:
            self[key] = None
        self.chooseWatershed()
        self.getFilenames()
        self.getParams()
#        self.modBasin()
#        self.modPdata()

    def chooseWatershed(self):
        # GUI to choose the watershed and subwatershed
        self['watershed'] = None
        self['subwatershed'] = None

    def getFilenames(self):
        # Get filename of *.basin file for reading - this is from the source version
        basinchoice = swing.JFileChooser()  #FileFilter="basin"
        #        filter = swing.JFileChooser.FileNameExtensionFilter("*.basin files",["basin"])
        #        basinin.addChoosableFileFilter(filter)
        #        basinin.SetFileFilter(FileNameExtensionFilter("basin"))
        basinfile = basinchoice.showOpenDialog(None)
        self['basinin'] = basinchoice.selectedFile

        # Get filename of *.basin file for writing - this is for the new version
        basinchoice = swing.JFileChooser()
        basinfile = basinchoice.showOpenDialog(None)
        self['basinout'] = basinchoice.selectedFile

        # Get filename of the *.pdata file - this is for the new version
        pdatachoice = swing.JFileChooser()
        pdatafile = pdata.showOpenDialog(None)
        self['pdata'] = pdatachoice.selectedFile

    def setParams(self, rd, cn, rr):
        # Save the future conditions parameters
        self['redevelopment'] = float(rd.getText())
        self['curvenumber'] = float(cn.getText())
        self['releaserate'] = float(rr.getText())
        print(self['releaserate'])

    def getParams(self):
        # Get future % of subbasin redeveloped, curve number, and release rate
        # First set up window for UI
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


class Element(List):
    def __init__(self):
        setName(name)
        setIdentifier(identifier)

    def getIdentifier(self):
        return identifier

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def getName(self):
        return name

    def setName(self, name):
        self.name = name

    def deserialize(self):  #add arg for input file
        currentLine = file.readline(self)
        while not currentLine == 'End:':
            p = Property(None)
            currentLine = currentLine.strip()
            lineList = currentLine.split(': ')
            p.setName(lineList[0])
            p.setValue(lineList[1])
            #add p to the Element object

    def serialize(self):    #add arg for output file
        #add code to print Element object to file and then print 'End:'
        pass

    def copy(self):
        #copy something... don't understand this yet
        pass


class Basin(Element):
    def __init__(self):
        super(Basin, self).__init__()

    def add(self):
        pass

    def remove(self):
        pass


class Subbasin(Element):
    def __init__(self):
        super(Subbasin, self).__init__()
        self.area = Property('Area')
        self.downstream = Property('Downstream')
        self.curvenum = Property('Curve Number')
        self.impervious = Property('Percent Impervious Area')
        self.staticProperties = [area.name, downstream.name, curvenum.name, impervious.name]

    def add(self, a):
        if isinstance(a,Property):
            if a.getName in staticProperties:
                self.area = a

    def remove(self, a):
        if isinstance(a,Property):
            if a.getName == 'area':
                self.area = None

    def updateSubbasin(self, areaval, dsval, cnval, impval):
        self.area.setValue(areaval)
        self.downstream.setValue(dsval)
        self.curvenum.setValue(cnval)
        self.impervious.setValue(impval)


class Junction(Element):
    def __init__(self):
        super(Junction, self).__init__()
        downstream = Property(None)

class Reservoir(Element):
    def __init__(self):
        super(Reservoir, self).__init__()
        downstream = Property(None)
        storageoutflow = Property(None)

class Reach(Element):
    def __init__(self):
        super(Reach, self).__init__()
        downstream = Property(None)

class Diversion(Element):
    def __init__(self):
        super(Diversion, self).__init__()
        downstream = Property(None)
        divertto = Property(None)

class Sink(Element):
    pass

class BasinSchema(Element):
    pass

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


    # Pull subbasin data from *.basin source file and store for processing
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
                else:
                    y = x.split(': ').strip()
                    if(y=="Subbasin"):
                        pass
            except None:
                pass

    # Add junction to each subbasin in *.basin sink file - this will be the downstream element for both portions of the
    # subbasin. Use the current downstream element for the junction.
    def addJunction(self):
        pass

    # Add a reservoir to each subbasin in *.basin sink file
    def addReservoir(self):
        pass

    # Update portion of each subbasin corresponding to % of redevelopment, using future CN and RR, in *.basin sink file
    def addPostdevSubbasin(self):
        pass

    # Add the portion of the subbasin that has not been redeveloped
    def addPredevSubbasin(self):
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

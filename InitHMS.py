# Jython 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date: February 2016

import sys
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/bin/java.exe")
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/src/java")
sys.path.append("C:/Program Files/Java/javahelp-2.0.05.jar")

#import java.lang
#import javax.help
import shutil

import Subwatershed_class as Subwatershed
import Basin_class as Basin
import Subbasin_class as Subbasin
import Junction_class as Junction
import Reservoir_class as Reservoir
import Reach_class as Reach
import Diversion_class as Diversion
import Sink_class as Sink
import BasinSchema_class as BasinSchema


def updatePdataFile(pd, pdatasink):
    pd.serialize(pdatasink)


def readBasinFile(basinin, basinout, pdatafile, dssfile, redevel, curvenum, rlsrate):
    pdatabackup = pdatafile + ".back"
    with open(basinin, 'rb') as basinsrc, open(basinout, 'wb') as basinsink, open(pdatafile, 'ab') as pdatasink, \
            open(pdatabackup, 'wb') as pdatacopy:
        shutil.copyfileobj(pdatasink, pdatabackup)
        recordnum = 0
        currentLine = ' '
        while not currentLine == '':
            try:
                currentLine = basinsrc.readline()
                if(currentLine.startswith('End:')):
                    b.serialize(basinsink)
                    recordnum += 1
                elif currentLine.startswith('Basin:'):
                    b = Basin.readBasin(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Subbasin:'):
                    b = Subbasin.readSubbasin(currentLine, basinsrc, basinsink, pdatasink, dssfile, dssfile, redevel,
                                              curvenum, rlsrate)
                elif currentLine.startswith('Junction:'):
                    b = Junction.readJunction(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Reservoir:'):
                    b = Reservoir.readReservoir(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Reach:'):
                    b = Reach.readReach(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Diversion:'):
                    b = Diversion.readDiversion(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Sink:'):
                    b = Sink.readSink(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Basin Schematic Properties:'):
                    b = BasinSchema.readBasinSchema(currentLine, basinsrc, basinsink)
                elif currentLine.endswith('\n'):
                    pass
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
    readBasinFile(ws['basinin'], ws['basinout'], ws['pdatafile'], ws['dssfile'], ws['redevelopment'], ws['curvenumber'],
                  ws['releaserate'])
    print('Program finished successfully.')
#    writeBasinFile(ws)
#    updatePdataFile(ws['pdata'])

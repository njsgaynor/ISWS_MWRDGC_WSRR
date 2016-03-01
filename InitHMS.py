#!/usr/bin/python

# Jython 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date: February 2016

# add Java directories to system path
import sys
import os
from subprocess import call
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/bin/java.exe")
sys.path.append("C:/Program Files/Java/jdk1.8.0_72/src/java")
sys.path.append("C:/Program Files/Java/javahelp-2.0.05.jar")

from Subwatershed_class import Subwatershed


def updatePdataFile(pd, pdatasink):
    pd.serialize(pdatasink)


def readBasinFile(ws):
    print('readBasinFile')
    # import Python modules
    import shutil

    from hecElements.Basin_class import Basin
    from hecElements.Subbasin_class import Subbasin
    from hecElements.Junction_class import Junction
    from hecElements.Reservoir_class import Reservoir
    from hecElements.Reach_class import Reach
    from hecElements.Diversion_class import Diversion
    from hecElements.Sink_class import Sink
    from hecElements.BasinSchema_class import BasinSchema
    from TableNames_class import TableNames
    from hecElements.Pdata_class import Pdata
    from SBDict_class import SBDict

    pdatabackup = ws['pdatafile'] + ".back"
    tableFile = "table_names.json"
    subbasinFile = "subbasin_records.json"
    # Make backup of *.pdata file
#    with open(ws['pdatafile'], 'ab') as pdatasink, open(pdatabackup, 'wb') as pdatacopy:
#        shutil.copyfileobj(pdatasink, pdatacopy)
    shutil.copyfile(ws['pdatafile'], pdatabackup)
    # Read elements from *.basin file and split the subbasins; write to new *.basin file
    # Also create list of table names (txt) and and subbasins/release rates (JSON) and write to files for later use
    with open(ws['basinin'], 'rb') as basinsrc, open(ws['basinout'], 'wb') as basinsink, open(ws['pdatafile'], 'ab') \
            as pdatasink:
        tableList = TableNames()
        sbAll = SBDict()
        recordnum = 0
        currentLine = ' '
        while not currentLine == '':
            try:
                currentLine = basinsrc.readline()
                if(currentLine.startswith('End:')):
                    try:
                        b.serialize(basinsink)
                        recordnum += 1
                    except:
                        print("Unexpected 'End:' statement in " + ws['basinin'] + ". Exiting.")
                        return
                elif currentLine.startswith('Basin:'):
                    b = Basin.readBasin(currentLine, basinsrc, basinsink)
                elif currentLine.startswith('Subbasin:'):
                    b, b2, soname = Subbasin.readSubbasin(currentLine, basinsrc, basinsink, ws['redevelopment'],
                                                      ws['curvenumber'], ws['releaserate'])
                    tableList.append([b2.getIdentifier(), soname, b2.area.getAsFloat(), ws['releaserate']])
                    Pdata.newPdata(soname, pdatasink, ws['dssfile'])
                    sbAll.add({b.getIdentifier(): b.rlsrate.getAsFloat(), b2.getIdentifier(): b2.rlsrate.getAsFloat()})
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
                    print("End of file " + ws['basinin'] + ".")
                    tableList.writeTableFile(tableFile)
                    sbAll.writeSbPairs(subbasinFile)
                    return tableList
                else:
                    print(currentLine)
                    raise RuntimeError("Invalid subwatershed element. Check input *.basin file.")
            except IOError:
                print("Cannot read file " + ws['basinin'] + " or " + ws['basinout'] + ".")
                return


def modMetFile(metFile, metData, hmsPath, sbList):
    import json
    metFileName = hmsPath + "/" + metFile
#    tableFileName = scriptPath + "/" + "table_names.json"
    with open(metFileName, 'ab') as metFileObj:#, open(tableFileName, 'rb') as subbasins:
#        sbList = json.load(subbasins)
#        print(subbasins)
        metFileObj.write('\n\n')
        for subbasin in sbList:
            lines = ['Subbasin: ', subbasin[0], '\n    Gage: ', metData, '\n\n    Begin Snow: None\nEnd:\n\n']
            metFileObj.writelines(lines)


def main(config):
    metFile = config.hmsMetFile + ".met"
    ws = Subwatershed(config)
    tableList = readBasinFile(ws)
    modMetFile(metFile, config.hmsGageName, config.getHmsProjectPath(), tableList)


if __name__=="__main__":
    main()

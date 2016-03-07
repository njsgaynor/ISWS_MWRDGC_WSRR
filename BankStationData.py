### These methods are intended to be used within other programs. As such, the file storage may not be robust across
### different versions of Jython.

#dssFilePath=config.getHmsProjectPath() + "/" + config.hmsProjectName + ".dss"
#dss = HecDss.open(dssFilePath)

# examples of accessing and using flow data from DSS file
#subbasinName="W28530"
#subbasinDataPath="//" + subbasinName + "/FLOW-UNIT GRAPH/TS-PATTERN/5MIN/RUN:" + config.hmsRunName + "/"
#inflowHydrograph = dss.get(subbasinDataPath.upper())

from hec.heclib.dss import HecDss
import pickle

def serialize(dataFromFile, sinkFile):
    # Writes data to a pickle file for use in subsequent script.
    pickle.dump(dataFromFile, sinkFile)
    pass

def getTimestageData(sourceFile):
    # Read in hourly (or other periodic) STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
    # Example of data paths:
    # /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/
    # /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01JAN2007/1HOUR/HUFFQII_100YR12H/
    dssFile = HecDss.open(sourceFile)
    dataPath = "/E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/"
    dataFromFile = dssFile.get(dataPath.upper())


    pass

def getBankData(sourceFile):
    ### Not sure if this can be automated. Would only need to do it once for each watershed.
    # Read in hourly (or other periodic) XXX data from HEC-RAS DSS file. Store data in a pickle file for further use.
    # Example of data paths:
    #
    pass

def getMaxstageData(sourceFile):
    # Read in hourly (or other periodic) LOCATION-ELEVATION//MAX STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
    # Example of data paths:
    # /E STONY CR DITCH E STONY CR DITCH//LOCATION-ELEV//MAX STAGE/HUFFQII_100YR12H/
    pass

def getPeakTimeData(sourceFile):
    # Read in hourly (or other periodic) LOCATION-TIME//MAX STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
    # Example of data paths:
    # /E STONY CR DITCH E STONY CR DITCH//LOCATION-ELEV//MAX STAGE/HUFFQII_100YR12H/
    pass
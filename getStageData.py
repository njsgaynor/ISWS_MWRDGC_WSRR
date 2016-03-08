

from hec.heclib.dss import HecDss
import pickle
from BankStationConfig import BankStation_config
from DSSDataDict_class import DSSDataDict

# Read in hourly (or other periodic) STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
# Example of data paths:
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01JAN2007/1HOUR/HUFFQII_100YR12H/
# .get([file path], True) returns data from all dates

filePath = "C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek/Stony_V3.0/"
dssFileName = filePath + "HydraulicModel/ExistingConditions/STCR/STCR_DesignRuns/STCR_Design2.dss"
dataPath = "C:/Users/nschiff2/ISWS_MWRDGC_WSRR/"

dataToGet = [["STAGE/01DEC2006/1HOUR", "timestage"], ["LOCATION-ELEV//MAX STAGE", "maxstage"],
             ["LOCATION-TIME//MAX STAGE", "peaktime"]]
config = BankStation_config()
dssFile = HecDss.open(config.dssFileName, True)
for i in range(len(dataToGet)):
    print("----------------------------------")
    pathNames = dssFile.getCatalogedPathnames("/*/*/" + dataToGet[i][0] + "/HUFFQII_100YR12H/")
    dataDict = getDSSData(pathNames, dssFile)
    print(dataPath + dataToGet[i][1] + ".txt")
    pickle.dump(dataDict, dataPath + dataToGet[i][1] + ".txt")

def getDSSData(pathNames, dssFile):
    dataDict = {}
    for item in range(len(pathNames)):
        dataFromFile = dssFile.get(pathNames[item], True)
        dataDict.update({pathNames[item]: dataFromFile.values})
    return dataDict
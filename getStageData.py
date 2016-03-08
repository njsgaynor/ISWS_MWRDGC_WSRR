from hec.heclib.dss import HecDss
from getDSSData import getDSSData
import pickle
from BankStationConfig import BankStation_config

# Read in hourly (or other periodic) STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
# Example of data paths:
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01JAN2007/1HOUR/HUFFQII_100YR12H/
# .get([file path], True) returns data from all dates
dataToGet = [["STAGE/01DEC2006/1HOUR", "timestage"], ["LOCATION-ELEV//MAX STAGE", "maxstage"],
             ["LOCATION-TIME//MAX STAGE", "peaktime"]]
config = BankStation_config()
dssFile = HecDss.open(config.dssFileName, True)
for i in range(len(dataToGet)):
    pathNames = dssFile.getCatalogedPathnames("/*/*/" + dataToGet[i][0] + "/HUFFQII_100YR12H/")
    dataDict = getDSSData(pathNames, dssFile)
    pickle.dump(dataDict, dataToGet[i][1] + ".txt")

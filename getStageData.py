

from hec.heclib.dss import HecDss
import pickle
#from BankStationConfig import BankStation_config
#from DSSDataDict_class import DSSDataDict

# Read in hourly (or other periodic) STAGE data from HEC-RAS DSS file. Store data in a pickle file for further use.
# Example of data paths:
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01DEC2006/1HOUR/HUFFQII_100YR12H/
# /E STONY CR DITCH E STONY CR DITCH/3.614/STAGE/01JAN2007/1HOUR/HUFFQII_100YR12H/
# .get([file path], True) returns data from all dates

filePath = "C:/Users/Nicki/IdeaProjects/"
dssFileName = filePath + "optimizer-hecras-integration/src/HEC-RASModels/STCR/STCR_DesignRuns/" \
                                   "STCR_Design2.dss"
#filePath = "C:/Users/nschiff2/Documents/MWRDGC_WSRR/Watershed_progs/StonyCreek/Stony_V3.0/"
#dssFileName = filePath + "HydraulicModel/ExistingConditions/STCR/STCR_DesignRuns/STCR_Design2.dss"
dataPath = filePath + "ISWS_MWRDGC_WSRR/"

dataToGet = [["STAGE/01DEC2006/1HOUR", "timestage"], ["LOCATION-ELEV//MAX STAGE", "maxstage"],
             ["LOCATION-TIME//MAX STAGE", "peaktime"]]
#config = BankStation_config()
#dssFile = HecDss.open(config.dssFileName, True)
dssFile = HecDss.open("C:/Users/Nicki/IdeaProjects/optimizer-hecras-integration/src/HEC-RASModels/STCR/"
                      "STCR_DesignRuns/STCR_Design2.dss", True)
for i in range(len(dataToGet)):
    pathNames = dssFile.getCatalogedPathnames("/*/*/" + dataToGet[i][0] + "/HUFFQII_100YR12H/");
    #dataDict = getDSSData(pathNames, dssFile)
    dataDict = {}
    for item in range(len(pathNames)):
        dataFromFile = dssFile.get(pathNames[item], True)
        try:
            dataList = list(dataFromFile.values)
            dataDict.update({pathNames[item]: dataList})
        except:
            #locationList = list(dataFromFile.xOrdinates)
            #dataList = list(dataFromFile.yOrdinates)
            #print(dataList)
            dataLocation = round(dataFromFile.xOrdinates[0], 6)
            dataValue = round(dataFromFile.yOrdinates[0][0], 6)
            splitPath = pathNames[item].split('/')
            splitPath[2] = str(dataLocation)
            pathNames[item] = "/".join(splitPath)
            dataDict.update({pathNames[item]: dataValue})
    print("-----------------------------------")
    print(dataPath + dataToGet[i][1] + ".txt")
    outFile = open(dataPath + dataToGet[i][1] + ".txt", 'wb')
    pickle.dump(dataDict, outFile)
    outFile.close()
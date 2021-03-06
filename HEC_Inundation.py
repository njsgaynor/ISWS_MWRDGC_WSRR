# Python 2.7
# Original author: Nicole JS Gaynor (nschiff2 [at] illinois [dot] edu)
# Created for: Illinois State Water Survey
# Date: February 2016

# This program takes data from the HEC-RAS model and compares the max stage and hourly stage to the bank station
# elevations to determine how far out of banks the water rises and how many hours the water is out of banks. This is
# recorded for each out-of-banks event in the simulation. Output is to a CSV file with columns RiverReach, StationID,
# and OOB_Depth#, and OOB_Time# for each OOB event (numbered #).

import csv
from operator import itemgetter
from BankStationConfig import BankStation_config
from subprocess import call
import pickle
import os

def getData():
    print("-----------------getData------------------")
    popd=os.getcwd()
    dssvuePath = "C:/Program Files (x86)/HEC/HEC-DSSVue/"
    os.chdir(dssvuePath)
    #scriptPath = "C:/Users/Nicki/IdeaProjects/ISWS_MWRDGC_WSRR/"
    scriptPath = "C:/Users/nschiff2/ISWS_MWRDGC_WSRR/"
    call(["HEC-DSSVue.cmd", "-s", scriptPath + "getStageData.py"], shell=True)
    os.chdir(popd)
    print("---------------getData end----------------")

def getTimeStage():
    print("getTimeStage")
    timestage = pickle.load(open("timestage.txt", 'rb'))
    #print(timestage)
    #print(len(timestage))
    # For every item in timestage (each station in Stony Creek), keep the data only if it is not an interpolated
    # station. The station ID is the second item in the data address.
    keyList = timestage.keys()
    for key in keyList:
        # Extract station ID from data address in DSS file
        u = key.split('/')
        try:
            v = float(u[2])  # see if station ID includes a *
            u[2] = str(round(float(u[2]), 2))
            newKey = " ".join(u[1:3])  # river/reach
            timestage[newKey] = timestage.pop(key)
        except ValueError:  # if station ID includes a * (is interpolated)
            timestage.pop(key)
    return timestage

def getBankElevations(bankFile):
    print("getBankElevations")
    # Open CSV file that contains the bank station elevations for each station in the Stony Creek watershed and read whole
    # file into a list.
    #   The CSV was copy-pasted from HEC-RAS (Profile output table) to Excel (data and headers) and saved as a CSV file.
    #   Interpolated cross sections must be included or only four decimal places of the station ID will show. This data is
    #   not available in HEC-DSSVue.
    with open(bankFile, 'rb') as csvfile:
        bank = list(csv.reader(csvfile, delimiter=','))
        print('bank ',len(bank))   #used for debugging
        # For every column in bank (each station in Stony Creek), keep the data only if it is not an interpolated station.
        #   The first three elements are river, reach, and station ID. Station ID needs to be converted to a float.
        #   Then concatenate river and reach into a single, uppercase element and assign to element 1.
        #   Store river/reach, station ID, left bank, and right bank for each station in bank_ID.
        bankDict = {}
        count = 0
        for t in bank:
            t[1] = " ".join(bank[count][0:2])
            t[1] = t[1].upper()
            try:
                r = float(t[2])
                if r > 0:
                    location = " ".join(t[1:3])
                    bankDict.update({location: list(t[-2:-1])})
            except ValueError:

                pass
            count += 1
        return bankDict

def getMaxStage(timestage):
    print("getMaxStage")
    maxstage = pickle.load(open("maxstage.txt", 'rb'))
    # For every item in maxstage (each station in Stony Creek), keep the data only if it is not an interpolated
    # station. The station ID is the second item in the data address. Timestage is used as the reference standard
    # for which stations to keep.
    print(maxstage)
    print(type(maxstage))
    print(len(maxstage))
    keyList = maxstage.keys()
    print(timestage.keys())
    print(maxstage.keys())
    for key in keyList:
        # Extract station ID from data address in DSS file
        u = key.split('/')
        u[2] = str(round(float(u[2]), 2))
        newKey = " ".join(u[1:3])  # river/reach
        if timestage.has_key(newKey):  # if station ID is not interpolated
            maxstage[newKey] = maxstage.pop(key)
        else:  # if station ID is interpolated
            maxstage.pop(key)
            print("Pop maxstage:", newKey)
    return maxstage

def checkInputs(bank, timestage, maxstage):
    print("checkInputs")
    # Debug which stations don't match between maxstage, bank, and timestage
    for y in maxstage:
        #assert bank.has_key(y)
        #assert timestage.has_key(y)
        pass
    # Used to check that each data set has the same number of stations (debugging)
    print('maxstage ',len(maxstage))
    print('timestage ',len(timestage))
    print('bank ',len(bank))

def match_stations(config):
    print("match_stations")
    timestage = getTimeStage()
    bank = getBankElevations(config.bankFileName)
    maxstage = getMaxStage(timestage)
    #checkInputs(bank, timestage, maxstage)
    #return (bank, timestage, maxstage)
    return maxstage, timestage, bank

def getStationID(item):
    print("getStationID")
    temp = item.split(' ')
    print(temp)
    return temp[0:(len(temp)-2)], temp[len(temp)-1]

def OOB_DepthTime(bank, timestage, maxstage):
    print("OOB_DepthTime")
    # By this point maxstage_ID, timestage_ID, and bank_ID should contain all the same stations.
    # River/reach/ID will be checked each time to make sure this is the case. Then calculate how far the max stage
    # exceeds the lower bank station and for how many hours the stage/water surface elevation exceeds the lower bank
    # station.
    overflow = [['River_Reach', 'Station_ID', 'OOB_Depth1', 'OOB_Time1']]
    count = 0
    # For each station
    for item in bank:
        riverReach, stationID = getStationID(item)
        overflow.append([riverReach, stationID])
        overflow[count+1].extend([-1, 0])
        # Calculate the lower bank station, the max stage OOB, and initialize the first OOB event
        lowbank = float(min(bank[item]))
        try:
            OOB_depth = round(float(maxstage[item])-lowbank, 4)
            if (not OOB_depth < 0):
                overflow[item+1][2] = OOB_depth
            else:
                overflow[item+1][2] = -1
            OOB_event = 1
            # For each time
            for stage in range(len(timestage[item])):
                if float(timestage[item][stage]) > lowbank:
                    try:
                        # Count the number of output times when river is out of banks
                        overflow[item+1][OOB_event+2] += 1
                    except IndexError:
                        # If OOB_event just started, add it to the list for current station
                        overflow[item+1].extend([1])
                        # Add column header if it doesn't exist yet
                        try:
                            overflow[0][OOB_event+2]
                        except IndexError:
                            overflow[0].extend(['OOB_Time'+str(OOB_event)])
                elif (float(timestage[item][stage]) < lowbank) and (overflow[item+1][-1] > 0):
                    # If within banks after >=1 OOB event, increment event counter
                    try:
                        overflow[item+1][OOB_event+2]
                        OOB_event += 1
                    except IndexError:
                        pass
            count = count + 1
        except KeyError:
            print("Key Error in maxstage: ", item)
    return overflow

def writeOOB_DepthTime(outFile, overflow):
    print("writeOOB_DepthTime")
    # Write overflow to a CSV file for further analysis or viewing in Excel
    with open(outFile, 'wb') as output:
        writer = csv.writer(output)
        writer.writerows(overflow)

# Used to look at state of variables for debugging
print('done')

def main():
    getData()
    config = BankStation_config()
    maxstage, timestage, bank = match_stations(config)
    #(bank, timestage, maxstage) = match_stations(config)
    overflow = OOB_DepthTime(bank, timestage, maxstage)
    writeOOB_DepthTime(config.outFileName, overflow)
    #print(maxstage.keys())
    print(len(maxstage))
    print(len(timestage))
    print(len(bank))

if __name__ == '__main__':
    main()

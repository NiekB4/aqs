# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 18:32:24 2018

@author: Niek
"""

import readSensorsCsv
import readLuchtmeetnet
import readWeerlive
import csv
from datetime import datetime, date, time, timedelta

# Call functions from the readSensorsCsv module:
dataSensorsCSV = readSensorsCsv.sensorsCSVtoMain()
dataSensorsCSVPleinweg = dataSensorsCSV[0]
dataSensorsCSVZwartewaalstraat = dataSensorsCSV[1]

# Call functions from the readLuchtmeetnet module:
dataLuchtmeetnet = readLuchtmeetnet.LuchtmeetnetDBtoMain()
dataLuchtmeetnetDBPleinweg = dataLuchtmeetnet[0]
dataLuchtmeetnetDBZwartewaalstraat = dataLuchtmeetnet[1]

# Call functions from the readWeerlive module:
dataWeerlive = readWeerlive.weerliveDBtoMain()

datasetCSV = dataSensorsCSVPleinweg
datasetDB = dataLuchtmeetnetDBPleinweg

   
def combine(datasetCSV, datasetDB, street):
    if street == "Zwartewaalstraat":
        filename = 'data/dataZwartewaalstraat.csv'
    elif street == "Pleinweg":
        filename = 'data/dataPleinweg.csv'
    c = 0
    with open(filename, 'w') as f:
        f.write("recordID;sensorID;aq1_1s;aq1_2s;aq1_10s;aq2_1s;aq2_2s;aq2_10s;temp1;temp2;hum1;hum2;lum;timestSensor;LMrecordID;LMstreet;LMno;LMno2;LMpm2;LMpm10;LMfn;LMtimestNodeRED;LMtimest;wlRecordID;WLcity;WLtemp;WLhum;WLwinddir;WLwindspeed;WLairpr;WLtimest\n")
        for i in range(0, len(datasetCSV[0])):
            # Set the different times used for the time matching. 
            timestCSV = datasetCSV[13][i]
            #timestCSV_min3 = timestCSV + timedelta(hours=-3) # Used for matching with LUCHTMEETNET.
            timestCSV_min2 = timestCSV + timedelta(hours=-2) # Used for matching with WEERLIVE.
            try:
                for j in range(0, len(datasetDB[0])):
                    stDB = datasetDB[8][j-1]
                    etDB = datasetDB[8][j]
                    if stDB < timestCSV_min2 < etDB:
                        f.write(str(datasetCSV[0][i]) + ";" + str(datasetCSV[1][i]) + ";" + str(datasetCSV[2][i]) + ";" + str(datasetCSV[3][i]) + ";" + str(datasetCSV[4][i]) + ";" + str(datasetCSV[5][i]) + ";" + str(datasetCSV[6][i]) + ";" + str(datasetCSV[7][i]) + ";" + str(datasetCSV[8][i]) + ";" + str(datasetCSV[9][i]) + ";" + str(datasetCSV[10][i]) + ";" + str(datasetCSV[11][i]) + ";" + str(datasetCSV[12][i]) + ";" + str(datasetCSV[13][i]) + ";" + str(datasetDB[0][j]) + ";" + str(datasetDB[1][j]) + ";" + str(datasetDB[2][j]) + ";" + str(datasetDB[3][j]) + ";" + str(datasetDB[4][j]) + ";" + str(datasetDB[5][j]) + ";" + str(datasetDB[6][j]) + ";" + str(datasetDB[7][j]) + ";" + str(datasetDB[8][j]) + ";")
                for k in range(0, len(dataWeerlive[0])):
                    stDBwl = dataWeerlive[7][k-1]
                    #stDBwl_PLUS_2 = dataWeerlive[7][k-1] + timedelta(hours=2)
                    etDBwl = dataWeerlive[7][k]
                    #etDBwl_PLUS_2 = dataWeerlive[7][k] + timedelta(hours=2)
                    if stDBwl < timestCSV_min2 < etDBwl:
                    #if stDBwl_PLUS_2 < timestCSV < etDBwl_PLUS_2:
                        f.write(str(dataWeerlive[0][k]) + ";" + str(dataWeerlive[1][k]) + ";" + str(dataWeerlive[2][k]) + ";" + str(dataWeerlive[3][k]) + ";" + str(dataWeerlive[4][k]) + ";" + str(dataWeerlive[5][k]) + ";" + str(dataWeerlive[6][k]) + ";" + str(dataWeerlive[7][k]) + ";" + "\n")
                        #f.write(str(dataWeerlive[0][k]) + ";" + str(dataWeerlive[1][k]) + ";" + str(dataWeerlive[2][k]) + ";" + str(dataWeerlive[3][k]) + ";" + str(dataWeerlive[4][k]) + ";" + str(dataWeerlive[5][k]) + ";" + str(dataWeerlive[6][k]) + ";" + str(etDBwl_PLUS_2) + ";" + "\n")
                #if c == 500:
                #    break
                #else:
                #    c += 1
            except IndexError:
                pass
    f.close()

def createNewCSV(datasetCSV, datasetDB, street):
    if street == "Zwartewaalstraat":
        combine(dataSensorsCSVZwartewaalstraat, dataLuchtmeetnetDBZwartewaalstraat, "Zwartewaalstraat")
        print("New CSV file created for {}!".format(street))
    elif street == "Pleinweg":
        combine(dataSensorsCSVPleinweg, dataLuchtmeetnetDBPleinweg, "Pleinweg")
        print("New CSV file created for {}!".format(street))

for i in range(0, 1):
    createNewCSV(dataSensorsCSVPleinweg, dataLuchtmeetnetDBPleinweg, "Pleinweg")
    createNewCSV(dataSensorsCSVZwartewaalstraat, dataLuchtmeetnetDBZwartewaalstraat, "Zwartewaalstraat")    
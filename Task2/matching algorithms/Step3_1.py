import pandas as pd
import re
import numpy as np

allAddress = pd.read_csv("ReducedAddress2_6_13.csv",
                         dtype={'EVENT_ID' : 'str',
                                'START_DATE' : 'str',
                                'END_DATE' : 'str',
                                'STREET1' : 'str',
                                'STREET2' : 'str',
                                'CITY' : 'str',
                                'STATE' : 'str',
                                'POSTAL_CODE' : 'str',
                                'P_STREET_NUM' : 'str',
                                'P_STREET_PRE' : 'str',
                                'P_STREET' : 'str',
                                'P_STREET_SUF' : 'str',
                                'P_STREET_APT' : 'str',
                                })

allAddress = allAddress.drop('Unnamed: 0', axis=1)
o = open("ReducedAddress3_6_13.csv", "w")

cols = allAddress.columns
for item in cols:
    if item != cols[0]:
        o.write(','+item)
    else:
        o.write(item)
o.write('\n')


s1 = allAddress.shape[0]
s2 = 0
s3 = 0
for index, row in allAddress.iterrows():
    s2 = s2 + 1
    if str(row['P_STREET_NUM']).isnumeric() == True:
        if str(row['P_STREET']) not in ['None','Unknown','Homeless','',' ','nan','NA']:
            h = re.sub('[^0-9]','',str(row['POSTAL_CODE']))
            if h not in [' ','']:
                s3 = s3 + 1
                o.write(str(row['EVENT_ID'])+','+str(row['DEDUP_KEY'])+','+str(row['START_DATE'])+','+str(row['END_DATE'])+','+str(row['STREET1'])+','+
                    str(row['STREET2'])+','+str(row['CITY'])+','+str(row['STATE'])+','+h+','+str(row['P_STREET_NUM'])+','+str(row['P_STREET_PRE'])+','+
                    str(row['P_STREET'])+','+str(row['P_STREET_SUF'])+','+str(row['P_STREET_APT'])+'\n')
    percent = ((s2/s1)*100)
    print("Percent Done: %2.4f   IN: %d   OUT: %d" % (percent,s2,s3), end='\r')
o.close()

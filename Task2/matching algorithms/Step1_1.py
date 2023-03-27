import pandas as pd
from address import AddressParser, Address
import numpy as np
import re

allAddress = pd.read_csv("K:/iTranslators/UTHealth Projects Jacky/Fujimoto/COVID-19 Contact Tracing/data/Patient Address History/PatientAddressHistory from202003to202112 PrimaryAddressOnly NoPendingDedup - v20220613.csv",
                         dtype={'EVENT_ID' : 'str',
                                'DEDUP_KEY' : 'str',
                                'START_DATE' : 'str',
                                'END_DATE' : 'str',
                                'STREET1' : 'str',
                                'STREET2' : 'str',
                                'CITY' : 'str',
                                'STATE' : 'str',
                                'POSTAL_CODE' : 'str'},
                         encoding='cp1252')
o = open("ReducedAddress1_6_13.csv", "w")
o.write("EVENT_ID,DEDUP_KEY,START_DATE,END_DATE,STREET1,STREET2,CITY,STATE,POSTAL_CODE,P_STREET_NUM,P_STREET_PRE,P_STREET,P_STREET_SUF,P_STREET_APT\n")

s1 = allAddress.shape[0]
s2 = 0
s3 = 0
ap = AddressParser()
for row in allAddress.itertuples(index=False):
    s2 = s2 + 1
    if str(row.STREET1) not in ['',' ','nan','NA']  and str(row.POSTAL_CODE) not in ['',' ','nan','NA']:
        s3 = s3 + 1
        h1 = re.sub('[^A-Za-z0-9]+',' ',str(row.STREET1))
        h2 = re.sub('[^A-Za-z0-9]+',' ',str(row.STREET2))
        if h2 == 'nan':
            h2 = ' '
        h4 = re.sub('[^A-Za-z0-9]+',' ',str(row.STATE))
        h5 = re.sub('[^A-Za-z0-9]+',' ',str(row.POSTAL_CODE))
        h6 = re.sub('[^A-Za-z0-9]+',' ',str(row.CITY))
        streetIN = h1 + ', ' + h2 + ', ' + h4 + ', ' + h5
        streetOUT = ap.parse_address(streetIN)
        apt = str(streetOUT.apartment)
        apt = apt.replace('Apt','').replace('APT','').replace('apt','').replace('Unit','').replace('unit','')
        if apt in ['',' ']:
            apt = 'None'
        o.write(str(row.EVENT_ID)+','+str(row.DEDUP_KEY)+','+str(row.START_DATE)+','+str(row.END_DATE)+','+h1+','+
                h2+','+h6+','+h4+','+h5+','+str(streetOUT.house_number)+','+str(streetOUT.street_prefix)+','+
                str(streetOUT.street)+','+str(streetOUT.street_suffix)+','+apt+'\n')
    percent = ((s2/s1)*100)
    print("Percent Done:  %2.4f  IN: %d    OUT: %d" % (percent,s2,s3), end='\r')
o.close()

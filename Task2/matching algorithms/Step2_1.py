import pandas as pd
import numpy as np

def merge_dates(grp):
    temp = pd.DataFrame(columns=['EVENT_ID','DEDUP_KEY','START_DATE','END_DATE','STREET1','STREET2','CITY',
                                      'STATE','POSTAL_CODE','P_STREET_NUM',
                                      'P_STREET_PRE','P_STREET','P_STREET_SUF','P_STREET_APT'])
    list_temp = [temp]
    dedupKey = grp.groupby(grp.DEDUP_KEY)
    listOfDedupKey = grp['DEDUP_KEY'].unique()
    for key in listOfDedupKey:
        df1 = dedupKey.get_group(key)
        df2 = dedupKey.get_group(key)
        df2['P_STREET_APT'] = df2['P_STREET_APT'].replace('None','z')
        df2 = df2.sort_values(by=['P_STREET_APT'])
        dt_groups = (df1['START_DATE'] != df1['END_DATE'].shift()).cumsum()
        collapsedDates = df1.groupby(dt_groups).agg({'EVENT_ID':'first','DEDUP_KEY':'first','START_DATE':'first','END_DATE':'last',})
        temp1 = pd.DataFrame({'EVENT_ID' : [collapsedDates.iloc[0][0]],
                'DEDUP_KEY' : [collapsedDates.iloc[0][1]],
                'START_DATE' : [collapsedDates.iloc[0][2]],
                'END_DATE' : [collapsedDates.iloc[0][3]],
                'STREET1': [df2.iloc[0][4]],
                'STREET2' : [df2.iloc[0][5]],
                'CITY' : [df2.iloc[0][6]],
                'STATE' : [df2.iloc[0][7]],
                'POSTAL_CODE' : [df2.iloc[0][8]],
                'P_STREET_NUM' : [df2.iloc[0][9]],
                'P_STREET_PRE' : [df2.iloc[0][10]],
                'P_STREET' : [df2.iloc[0][11]],
                'P_STREET_SUF' : [df2.iloc[0][12]],
                'P_STREET_APT' : [df2.iloc[0][13]]})
        list_temp.append(temp1)
    sendIT = pd.concat(list_temp)
    return sendIT
        
pd.options.mode.chained_assignment = None
address = pd.read_csv("ReducedAddress1_6_13.csv",
                         dtype={'EVENT_ID' : 'str',
                                'DEDUP_KEY' : 'str',
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
                                'P_STREET_APT' : 'str'},
                         encoding='cp1252', on_bad_lines='warn')
s1 = address.shape[0]
s2 = 0
s3 = 0
listOfPercent = [10,20,30,40,50,60,70,80,90,100]
c = 0
address['START_DATE'] = np.where((address.START_DATE == "1900-01-01"), "1990-01-01", address.START_DATE)
address['END_DATE'] = np.where((address.END_DATE == "2030-01-01"), "2025-01-01", address.END_DATE)
address['START_DATE'] = pd.to_datetime(address['START_DATE'])
address['END_DATE'] = pd.to_datetime(address['END_DATE'])
eventIDs = address.groupby(address.EVENT_ID)
listOfEventIDs = address['EVENT_ID'].unique()

new_addresses = pd.DataFrame(columns=['EVENT_ID','DEDUP_KEY','START_DATE','END_DATE','STREET1','STREET2','CITY',
                                      'STATE','POSTAL_CODE','P_STREET_NUM',
                                      'P_STREET_PRE','P_STREET','P_STREET_SUF','P_STREET_APT'])
list_new_addresses = [new_addresses]

for ident in listOfEventIDs:
    new_array = eventIDs.get_group(ident)
    s2 = new_array.shape[0] + s2
    percent = ((s2/s1)*100)
    new_address = merge_dates(new_array)
    s3 = s3 + new_address.shape[0]
    new_address = new_address.reset_index()
    list_new_addresses.append(new_address)
    if percent > listOfPercent[c]:
        c = c + 1
        new_address = pd.concat(list_new_addresses)
        list_new_addresses = [new_address]
    print("Percent Done: %2.4f   IN: %d   OUT: %d" % (percent,s2,s3), end='\r')

new_addresses = pd.concat(list_new_addresses)
new_addresses = new_addresses.drop('index',axis=1)
new_addresses['P_STREET_APT'] = new_addresses['P_STREET_APT'].replace('z','None')
new_addresses.to_csv("ReducedAddress2_6_13.csv", sep=',',encoding='utf-8')


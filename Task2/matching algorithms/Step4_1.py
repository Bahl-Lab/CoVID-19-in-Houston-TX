import pandas as pd
import numpy as np

#define function that recieves a dataframe and appends the filtered dataframe to a list
def filterAddress(data):
    #create new column containing continuious address data
    data['STREET_ALL'] = data[['P_STREET_NUM','P_STREET','P_STREET_APT']].apply(lambda row: "_".join(row.values.astype(str)),axis=1)
    #index dataframe by the newly create column and remove records where the 'STREET_ALL' value appears more than 19 times
    data=data.groupby('STREET_ALL').filter(lambda x : len(x) <16)
    #remove the newly created column from filtered dataframe
    del data['STREET_ALL']
    #add filtered dataframe to list to be concat to main dataframe later
    list_allData.append(data)

pd.options.mode.chained_assignment = None
f = pd.read_csv("ReducedAddress3_6_13.csv",
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
                                'P_STREET_APT' : 'str'})
fs = f.groupby(f.POSTAL_CODE)
listOfZip = f['POSTAL_CODE'].unique()
count = 1
inNum = 0
outNum = 0
allData = pd.DataFrame(columns=['EVENT_ID',
                                'START_DATE',
                                'END_DATE',
                                'STREET1',
                                'STREET2',
                                'CITY',
                                'STATE',
                                'POSTAL_CODE',
                                'P_STREET_NUM',
                                'P_STREET_PRE',
                                'P_STREET',
                                'P_STREET_SUF',
                                'P_STREET_APT'])
list_allData = [allData]

for zipCode in listOfZip:
    new_array = fs.get_group(zipCode)
    size = new_array.shape
    if size[0] > 5000:
        cnt = 1
        street_nums = new_array.groupby(new_array.P_STREET_NUM)
        listOfNum = new_array['P_STREET_NUM'].unique()
        for num in listOfNum:
            new_array2 = street_nums.get_group(num)
            filterAddress(new_array2)
            per = (cnt/len(listOfNum))*100
            percent = (count/len(listOfZip))*100
            print("IN: %d   OUT: %d   Percent Done: %2.4f   SubProcess: %2.4f    " % (inNum,outNum,percent,per) ,end='\r',flush=True)
            cnt +=1
    else:
       filterAddress(new_array)
    if count < 150:
        allData = pd.concat(list_allData)
        list_allData = [allData]
    else:
        if count % 100 == 0:
            allData = pd.concat(list_allData)
            list_allData = [allData]
    size2 = allData.shape
    outNum = size2[0]
    inNum = inNum + size[0]
    percent = (count/len(listOfZip))*100
    print("IN: %d   OUT: %d   Percent Done: %2.4f" % (inNum,outNum,percent) ,end='\r',flush=True)
    count +=1
print("IN: %d   OUT: %d   Percent Done: %2.4f" % (inNum,outNum,percent) ,end='\r',flush=True)    
allData.to_csv("ReducedAddress4_6_13.csv",sep=',',encoding='utf-8')

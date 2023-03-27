import pandas as pd
import recordlinkage
import numpy as np
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Bring in dataset of reduced addresses, use dtype to prevent multi-type input errors
address = pd.read_csv("ReducedAddress4_6_13.csv",
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
address = address.replace(np.nan,' ')
address = address.replace('nan',' ')
#Create counter to track number of zip code groups which have been processed
count = 1
#Create counter to track number of records processed
inNum = 0
#Create counter to track the number of matches found
outNum = 0
#create counter to track the number of times matches output to csv file (outputs ~every 500,000 matches)
po = 0
#create counter to track number of matches outputed to csv file
hold = 0
#Create empty dataframe to concat to dataframes of matches
matchesAllInfo = pd.DataFrame(columns=['EVENT_ID_x',
                                       'START_DATE_x',
                                       'END_DATE_x',
                                       'STREET1_x',
                                       'STREET2_x',
                                       'CITY_x',
                                       'STATE_x',
                                       'POSTAL_CODE_x',
                                       'P_STREET_NUM_x',
                                       'P_STREET_PRE_x',
                                       'P_STREET_x',
                                       'P_STREET_SUF_x',
                                       'P_STREET_APT_x',
                                       'Unnamed: 0.1_y',
                                       'EVENT_ID_y',
                                       'START_DATE_y',
                                       'END_DATE_y',
                                       'STREET1_y',
                                       'STREET2_y',
                                       'CITY_y',
                                       'STATE_y',
                                       'POSTAL_CODE_y',
                                       'P_STREET_NUM_y',
                                       'P_STREET_PRE_y',
                                       'P_STREET_y',
                                       'P_STREET_SUF_y',
                                       'P_STREET_APT_y'])
list_matchesAllInfo = [matchesAllInfo]
#index address dataset by zip code
addresses = address.groupby(address.POSTAL_CODE)
#create a list containing all zip code values in address dataset
listOfZip = address['POSTAL_CODE'].unique()
#iterate through list of zip codes to access the index values in address dataset
for zipCode in listOfZip:
    #create new dataframe holding only records containing specified zip
    new_array = addresses.get_group(zipCode)
    #store the size information of the new dataframe
    size = new_array.shape
    #create counter to track the number of street_num groups which have been processed
    cnt1 = 0
    #index zip code dataset by street_num
    street_nums = new_array.groupby(new_array.P_STREET_NUM)
    #create a list containing all street_num values in zip code dataset
    listOfNum = new_array['P_STREET_NUM'].unique()
    #iterate through list of street_num to access the index values in zip code dataset
    for num in listOfNum:
        #create new dataframe holding only records of specified street_num
        new_array2 = street_nums.get_group(num)
        #increament counter for zip code processing
        cnt1 +=1
        #create counter to track the number of street2 groups which have been processed
        cnt2 = 1
        #index street_num dataset by street2
        apt_nums = new_array2.groupby(new_array2.P_STREET_APT)
        #create list containing all street2 values in street_num dataset
        listOfApt = new_array2['P_STREET_APT'].unique()
        #iterate through list of street2 to access the index values in street_num dataset
        for apts in listOfApt:
            matchesPart = pd.DataFrame(columns=['EVENT_ID_x',
                                                'START_DATE_x',
                                                'END_DATE_x',
                                                'STREET1_x',
                                                'STREET2_x',
                                                'CITY_x',
                                                'STATE_x',
                                                'POSTAL_CODE_x',
                                                'P_STREET_NUM_x',
                                                'P_STREET_PRE_x',
                                                'P_STREET_x',
                                                'P_STREET_SUF_x',
                                                'P_STREET_APT_x',
                                                'Unnamed: 0.1_y',
                                                'EVENT_ID_y',
                                                'START_DATE_y',
                                                'END_DATE_y',
                                                'STREET1_y',
                                                'STREET2_y',
                                                'CITY_y',
                                                'STATE_y',
                                                'POSTAL_CODE_y',
                                                'P_STREET_NUM_y',
                                                'P_STREET_PRE_y',
                                                'P_STREET_y',
                                                'P_STREET_SUF_y',
                                                'P_STREET_APT_y'])
            matchesPartList = [matchesPart]
            #create new dataframe holding only records of specified street2
            new_array3 = apt_nums.get_group(apts)
            #initialize an instance of recordlinkage index 
            indexer = recordlinkage.Index()
            #specify the type of index
            indexer.full()
            #interate through the smaller subsets of the larger subset
            for dfB_subset in np.split(new_array3,np.arange(10,len(new_array3),10)):
                #create an index of possible matches between the street2 dataset and itself
                candidates = indexer.index(new_array3,dfB_subset)
                #initialize an instance of recordlinkage compare
                comp = recordlinkage.Compare(n_jobs=-1)
                #add compare condition, fuzzy matching with .9 threshold using levenshtein's algo
                comp.string('P_STREET','P_STREET', method='levenshtein', threshold=0.75)
                #add compare condition, event_ids must not match
                comp.exact('EVENT_ID','EVENT_ID', agree_value=0,disagree_value=1)
                #add compare condition, must match
                comp.exact('P_STREET_NUM','P_STREET_NUM')
                #add compare condition, must match
                comp.exact('P_STREET_APT','P_STREET_APT')
                #add compare condition, must match
                comp.exact('POSTAL_CODE','POSTAL_CODE')
                #run the recordlinkage compute method to find possible matches
                matches = comp.compute(candidates, new_array3, new_array3)
                #filter results to only retain those matches that meet every condition
                matches = matches[matches.sum(axis=1)>4].reset_index()
                #merge the indexes of the matches to the matches source data
                matches = pd.merge(matches,new_array3, left_on='level_1',right_index=True)
                #merge the indexes of the matches to the matches source data
                matches = matches.merge(new_array3, left_on = 'level_0', right_index=True)
                #remove columns that are no longer needed
                matches = matches.drop(columns=['level_0','level_1',0,1,2,3,4])
                #append dataframe of matches to list in order to concat to main matches dataset later
                matchesPartList.append(matches)
            #bring all the matches found into one dataset
            matchesHold = pd.concat(matchesPartList)
            #build mask (condition) to filter dataset, to test if dates are overlapping
            mask = (((matchesHold['START_DATE_x'] > matchesHold['START_DATE_y']) & (matchesHold['START_DATE_x'] < matchesHold['END_DATE_y'])) | ((matchesHold['END_DATE_x'] > matchesHold['START_DATE_y']) & (matchesHold['END_DATE_x'] < matchesHold['END_DATE_y'])) | ((matchesHold['END_DATE_x'] == matchesHold['END_DATE_y']) & (matchesHold['START_DATE_x'] == matchesHold['START_DATE_y'])))
            #run filtering using mask built in previous step
            matchesHold = matchesHold.loc[mask]
            #build another mask to order event_ids in order to remove duplicate matches
            mask  = matchesHold['EVENT_ID_x'] < matchesHold['EVENT_ID_y']
            #create new column with the higher valued event_id
            matchesHold['first'] = matchesHold['EVENT_ID_x'].where(mask, matchesHold['EVENT_ID_y'])
            #create new column with the lower valued event_id
            matchesHold['second'] = matchesHold['EVENT_ID_y'].where(mask, matchesHold['EVENT_ID_x'])
            #remove the duplicate matches using the columns 'first' and'second'
            matchesHold = matchesHold.drop_duplicates(subset=['first','second'], keep='last')
            #drop columns that are no longer useful
            matchesHold = matchesHold.drop(columns=['first', 'second'])
            #add dataset to list to be brought together later
            list_matchesAllInfo.append(matchesHold)
            #calculate percent of street2 processed
            per2 = (cnt2/len(listOfApt))*100
            #calculate percent of street_num processed
            per = (cnt1/len(listOfNum))*100
            #calculate percent of zip codes processed
            percent = (count/len(listOfZip))*100
            #print updated data on processing
            print("IN: %d   OUT: %d    Percent Done: %2.4f     SubProcess: %2.4f   SubSubProcess: %2.4f" % (inNum,outNum,percent,per,per2),end="\r", flush=True)
            #increment counter for number of street2 groups processed
            cnt2 +=1
    if count < 100:
        #concat main matches dataset with all dataframes saved to list of matchesAllInfo
        matchesAllInfo = pd.concat(list_matchesAllInfo)
        #reset list of matchesAllInfo to contain only the main matches dataset
        list_matchesAllInfo = [matchesAllInfo]
    else:
        if count % 10 == 0:
            #concat main matches dataset with all dataframes saved to list of matchesAllInfo
            matchesAllInfo = pd.concat(list_matchesAllInfo)
            #reset list of matchesAllInfo to contain only the main matches dataset
            list_matchesAllInfo = [matchesAllInfo]
    #store the size information of matches found 
    size2 = matchesAllInfo.shape
    #store the number matches found
    outNum = hold + size2[0]
    if size2[0] > 500000:
        hold = hold + size2[0]
        po +=1
        h = "Matches" + str(po) + "_6_13.csv"
        matchesAllInfo.to_csv(h,sep=',',encoding='utf-8')
        matchesAllInfo = pd.DataFrame(columns=['EVENT_ID_x',
                                               'START_DATE_x',
                                               'END_DATE_x',
                                               'STREET1_x',
                                               'STREET2_x',
                                               'CITY_x',
                                               'STATE_x',
                                               'POSTAL_CODE_x',
                                               'P_STREET_NUM_x',
                                               'P_STREET_PRE_x',
                                               'P_STREET_x',
                                               'P_STREET_SUF_x',
                                               'P_STREET_APT_x',
                                               'EVENT_ID_y',
                                               'START_DATE_y',
                                               'END_DATE_y',
                                               'STREET1_y',
                                               'STREET2_y',
                                               'CITY_y',
                                               'STATE_y',
                                               'POSTAL_CODE_y',
                                               'P_STREET_NUM_y',
                                               'P_STREET_PRE_y',
                                               'P_STREET_y',
                                               'P_STREET_SUF_y',
                                               'P_STREET_APT_y'])
    list_matchesAllInfo = [matchesAllInfo]
    #increment the number of records processed
    inNum = inNum + size[0]
    #increment counter tracking number of zip codes processed
    count += 1
print("IN: %d   OUT: %d    Percent Done: %2.4f     SubProcess: %2.4f   SubSubProcess: %2.4f" % (inNum,outNum,percent,per,per2),end="\r", flush=True)
po+=1
h = "Matches" + str(po) + "_6_13.csv"
matchesAllInfo.to_csv(h,sep=',',encoding='utf-8')

Jacky Kuo, Ryan Lewis
03/01/2023


### to do
  - add fake data to show data structure


###### !! ~  The following notes were extracted from Ryan's folder and were originally written by him  ~ !! ######



==================================================================
====== /// /// /// NOTES BY RYAN /// /// /// =====================
==================================================================
COVID-19 Address Matching 1-11-22
Version 4

Initial:Total = 7,849,621 (3,312,427 EVENT_ID)

Step 1 (Clean/Standardize):
	Remove ['',' ','nan','NA'] from ['STREET1'] & ['POSTAL_CODE']
	Total = 7,465,624 (3,110,707 EVENT_ID)
	
	['STREET1'] + ['STREET2'] + ['STATE'] + ['POSTAL_CODE'] = ['P_STREET_NUM'],['P_STREET_PRE'],['P_STREET'],['P_STREET_SUF'],['P_STREET_APT']
	Location def = ['POSTAL_CODE'],['P_STREET_NUM'],['P_STREET'],['P_STREET_APT']
	Locations = 2,087,014

Step 2 (Reduction):
	['EVENT_ID'],['DEDUP_KEY'] == ['EVENT_ID'],['DEDUP_KEY'] (take record that contains a number in the ['P_STREET_APT'] column, else take earliest time)
	Total = 3,510,334 (3,110,707 EVENT_ID)
	Locations = 1,905,560

Step 3 (Clean):
	Remove ['None','Unknown','Homeless',' ','','nan','NA'] from ['P_STREET']
	Remove all ['P_STREET_NUM'] that are non-numeric values 
	Cut all non-numeric characters from ['POSTAL_CODE'], then Remove [' ',''] from ['POSTAL_CODE']
	Total = 3,380,375 (3,016,449 EVENT_ID)
	Locations = 1,850,266

Step 4 (Filter):
	Locations with frequency > 15 Removed
	Total = 3,015,523 (2,724,484 EVENT_ID)
	Locations = 1,843,456

Step 5 (Matching):
	Total Matches = 2,022,329 (1,148,390 EVENT_ID)
	Unique Matches = 1,983,189
	Locations = 417,979

	After filtering Locations with frequency > 45
	Total Matches = 1,668,404 (1,100,497 EVENT_ID)
	Unique Matches = 1,640,205
	Locations = 414,093 (2.66 Indivduals/Locations)





==========================================================================
====== /// /// /// SUMMARY FOR CDC (also by Ryan) /// /// /// ============
==========================================================================
  * After data cleaning/standardization 1,850,266 locations were identified

  * 6,810 locations with > 15 records associated with it
     - Within the 6,810 locations there are 364,852 records and 291,965 individuals
         ~ Of the 291,965 individuals, 102,230 individuals are associated with another location or 35.01%

  * Of the 6,810 locations, 193 have > 200 records associated with it
     - Within the 193 locations there are 99,691 records
        ~ Of the 99,691 records:
	  19.65%  are  healthcare facilities 				(green)
	  14.26%  are  assisted living centers 				(red)
	  13.72%  are  detention centers 				(blue)
	  10.78%  are  commercial/offices 				(pink)
	  3.22%   are  government facilities 				(orange)
	  2.80%   are  charities/homeless facilities			(olive)
	  2.70%   are  education centers		 		(purple)
	  32.87%  are  Apartments with no apartment# or Unknown Origin

  * 1,843,456 locations with < 15 records associated with it
     - Of the 1,843,456 locations, 417,979 locations have multiple individuals or 22.67%
        ~ Within the 417,979 locations there is an average of 2.74 individuals per location




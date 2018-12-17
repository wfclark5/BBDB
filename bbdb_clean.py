import pandas

bbdb = pandas.read_csv("bbdb_raw.csv")



##These first few lines will get rid of all data that has bot been completed. This typically happens when someone opens a survey but doesn't do anything else 


notcompletedfilter = bbdb[(bbdb['consent_timestamp'] != "[not completed]") & (bbdb['firstname'].notna())]



##Use the cleaned data to begin to check for duplicates merge the first name and last names together 

notcompletedfilter["fnlmerge"] = notcompletedfilter['firstname'].str.lower().replace("", "") + notcompletedfilter['lastname'].str.lower().replace("", "")

duplicates = notcompletedfilter

duplicates["is_duplicated"] = notcompletedfilter.duplicated(['fnlmerge'], keep = False)


###these commented out lines of code will create your duplicate file 


# duplicates = duplicates[(duplicates["is_duplicated"] == True)]
# duplicates.to_csv("bbdb_duplicates.csv")
# duplicates = notcompletedfilter[(notcompletedfilter['duplicate'] == 1)]


###this is the file that we will want to join back the cleaned duplicate data and the ace participant data

clean_non_duplicated = duplicates[(duplicates["is_duplicated"] == False)]

print(clean_non_duplicated)

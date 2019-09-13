import os.path
import os
import urllib
from requests import post
import sys
import pandas
import json
import numpy as np
from collections import Counter
import re
import time
from datetime import datetime
from pathlib import Path
p = Path(__file__).parents[1]
api_keys = pandas.read_csv(str(p) + r"\api_keys.csv")
api_p1 = api_keys["API Key"][0]
api_p2 = api_keys["API Key"][1]
api_p3 = api_keys["API Key"][2]
api_arc = api_keys["API Key"][3]
api_ready = api_keys["API Key"][4]
api_mchat = api_keys["API Key"][5]
api_enrollment = api_keys["API Key"][6]
api_bbdb = api_keys["API Key"][7]

today = str(datetime.today().strftime('%Y-%m-%d' +'_' +'%H%M'))

print("The task has succesfully started")

print(str(datetime.today()))

path = os.path.dirname(os.path.realpath(__file__))


def getData(data):
    r = post("https://redcap.duke.edu/redcap/api/", data)
    r.content
    d = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request("https://redcap.duke.edu/redcap/api/", d)
    response = urllib.request.urlopen(req)
    file = response.read()
    result = json.loads(file)
    df = pandas.DataFrame.from_records(result)
    return df


#This data extract is for pulling out all of the MCHAT scores from within the P1 database

data = {
    'token': 'str(api_bbdb)',
    'content': 'report',
    'format': 'json',
    'report_id': '18651',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'json'
}

bbdb = getData(data)

##These first few lines will get rid of all data that has bot been completed. This typically happens when someone opens a survey but doesn't do anything else

# notcompletedfilter = bbdb[(bbdb['firstname'].notna())]

notcompletedfilter = bbdb

##Use the cleaned data to begin to check for duplicates merge the first name and last names together

notcompletedfilter["fnlmerge"] = notcompletedfilter['firstname'].str.lower().replace("", "") + notcompletedfilter['lastname'].str.lower().replace("", "") + notcompletedfilter['dob'].str.lower()

duplicates = notcompletedfilter

duplicates["is_duplicated"] = notcompletedfilter.duplicated(['fnlmerge'], keep = False)

final_df = duplicates[duplicates["is_duplicated"] == False]

final_df.to_csv(path + r"\registry_participants.csv", index=False)

duplicated = duplicates[duplicates["is_duplicated"] == True]

duplicated.to_csv(path + r"\duplicate_potential.csv", index=False)

print("Successfully Completed")
time.sleep(30)



###these commented out lines of code will create your duplicate file


# duplicates = duplicates[(duplicates["is_duplicated"] == True)]
# duplicates.to_csv("bbdb_duplicates.csv")
# duplicates = notcompletedfilter[(notcompletedfilter['duplicate'] == 1)]


###this is the file that we will want to join back the cleaned duplicate data and the ace participant data

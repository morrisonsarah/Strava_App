#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Script to get Strava activities and save to .json file in current working directory
Requires access token generated from strava.com user account, saved in file access_token
Written for Python 2.7.x
'''

# Imports
import sys
import requests
import json
import os

## Authentication
#TODO: add COMMENTS to file (ignore '#')??
cwd = os.getcwd()
access_token = open(cwd + "/" + 'access_token').read().strip()

## Get Athlete Data
print "Getting Athlete Data"
url = 'https://www.strava.com/api/v3/athlete/activities'
header = {'Authorization': 'Bearer ' + access_token}
params = {'per_page': '200','page':'1'}

# Get first page of data, exit if HTML Request fails
try:
    data = requests.get(url, headers=header, params=params)
    data.raise_for_status()
except requests.exceptions.HTTPError as err:
    print err
    sys.exit(1)

# Convert to JSON (N.B. this is a LIST), exit if conversion fails
try:
    athlete_data = data.json()
except ValueError as err:
    print err
    sys.exit(1)

# Count number of entries
data_page_length = len(athlete_data)

# Set initial page to 1
page = 1

# TODO: Complexity is O(n^2)
while data_page_length > 0:
    # increment page
    page += 1
    params['page'] = str(page)
    #print params

    # get page
    data = requests.get(url, headers=header, params=params)

    # convert data class to data_page dict
    data_next_page = data.json()

    # count data_page_length
    data_page_length = len(data_next_page)

    # append to athelete_data
    # TODO: Complexity is O(n^2)
    athlete_data += data_next_page[:]

print "Strava Activities Collected: ", len(athlete_data)

# Write data_page to file
filename = "athlete_data.json"
json.dump(athlete_data,open(filename,'w'))
print "Saved to file:", cwd + "/" + filename,

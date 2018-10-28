# -*- coding: utf-8 -*-
"""
Phanalytix Show Tracker

Joseph May 
josephmay95@hotmail.com
919-600-4688
"""
import requests
import logging
import sys

from logging import debug, info
import json

'''
Identify Hard-Coded values up front, with a dictionary of names for referencing
'''
params = {
    #Save the base URL for the Phish.in API 
    'phishin_url': 'http://phish.in/api/v1',
    #Save the base URL for the Phish.Net API
    'phishnet_url': 'https://api.phish.net/v3/',
    #the Phish.net API key for application "jmay1995" is: E972636BCF5D4EF75256 
    'phishnet_key': 'E972636BCF5D4EF75256',
    #the Phish.net Public key for application "jmay1995" is: 4A474082F30E6491601A
    'phishnet_public': '4A474082F30E6491601A'
    }   
shows_attended = ['2014-07-25', '2015-08-14', '2015-08-15', '2015-08-16',
                  '2016-06-24', '2016-06-25', '2016-06-26', '2016-08-26',
                  '2016-08-28', '2016-10-21', '2016-10-22', '2017-08-01',
                  '2017-08-02', '2017-08-04', '2017-08-05', '2017-08-06',
                  '2017-12-28', '2017-12-29', '2017-12-30', '2017-12-31',
                  '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-07',
                  '2018-08-08', '2018-08-10', '2018-08-11', '2018-08-12']

def get_years(url):
    url_years = (url + '/years')
    response = requests.get(url_years).json()
    data = response['data']
    return data

def get_shows_from_years(url, years):
    shows = []
    for year in years:
        url_year = (url + '/years/' + year)
        response = requests.get(url_year).json()
        data = response['data']
        for show in data:
            date = show['date']
            shows.append(date)
    return shows

def get_setlists_from_shows(url, key, shows):
    setlists = []
    url_base = (url+ 'setlists/get?apikey=' + key)
    for show in shows:
        url_setlist = (url_base + '&showdate=' + show)
        response = requests.get(url_setlist).json()
        data = response['response']['data']
        
        #Clean data for calls that return nothing
        if data != []:
            setlists.append(data[0])
    return setlists

if __name__ == '__main__':
    #Set up logging environment
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s %(module)-8s %(funcName)-12s %(message)s', datefmt='%H:%M:%S')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    #Get a list of every year that Phish played shows in
    years = get_years(params['phishin_url'])
    #Get a list of every show that phish has played
    shows = get_shows_from_years(params['phishin_url'], years)
    #Get the setlist data for every show listed
    setlists = get_setlists_from_shows(params['phishnet_url'], params['phishnet_key'], shows)

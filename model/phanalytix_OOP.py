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
from collections import OrderedDict

#Define utility functions for serializing object states
def listify(list_of_obj):
    return [o.todict() for o in list_of_obj]
def dictify(dict_of_obj):
    return {k: v.todict() for k, v in dict_of_obj.items()}

class Phanalytix():
    '''Overall shell set up for model run'''
    def __init__(self, name, params, shows_attended, years=[], dates = []):
        self.name = name
        self.params = params  
        self.shows_attended = shows_attended

        if (years == []) and (dates == []):
            info('A - Model fed with no input years or dates')
            self.years = self.get_years()
            self.dates = self.get_dates_from_years()
        elif years == []:
            #This allows the user to input a list of dates and only query those dates
            info('B - Model fed with no input years, and dates: {}'.format(dates))
            self.years = list(set([k[:4] for k in dates]))
            self.dates = dates
        elif dates == []:
            #This allows the user to input a list of years and only query those years
            info('C - Model fed with no input dates, and years: {}'.format(years))
            self.years = years
            self.dates = self.get_dates_from_years()
        else:
            #This allows the user to input a list of years and dates and combine the two
            info('D - Model fed with input years: {} and input dates: {}'.format(years, dates))
            self.years = years
            self.dates = self.get_dates_from_years()
            self.dates.extend(dates)
        
        self.shows = self.get_showdata_from_dates()
        
    @classmethod
    def load_model(cls, name, params, shows_attended, years=[], dates=[]):
        phanalytix = Phanalytix(name, params, shows_attended, years, dates)
        return phanalytix
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        st = "Model({}, Years{}, Shows{})".format(self.name, self.years, self.shows)
        return st
    
    def todict(self):
        '''
        Output a Dict representation of the model
        '''
        model = OrderedDict(
                years=listify(self.years),
                shows=listify(self.shows))
        return model

    def get_years(self):
        '''
        Get a list of every year that Phish has played shows in from Phish.in
        '''
        url_years = (self.params['phishin_url'] + '/years')
        response = requests.get(url_years).json()
        data = response['data']
        return data
    
    def get_dates_from_years(self):
        '''
        Get a list of every show played in the years passed through
        '''
        dates = []
        for year in self.years:
            url_year = (self.params['phishin_url'] + '/years/' + year)
            response = requests.get(url_year).json()
            data = response['data']
            for show in data:
                date = show['date']
                dates.append(date)
        return dates

    def get_showdata_from_dates(self):
        shows = OrderedDict()
        url_base = (self.params['phishnet_url'] + 'setlists/get?apikey=' + self.params['phishnet_key'])
        for date in self.dates:
            url_setlist = (url_base + '&showdate=' + date)
            response = requests.get(url_setlist).json()
            data = response['response']['data']
            if data != []:
                data = data[0]
                show = Shows.create_shows(data, self)
                shows[date] = show
        return shows

class Shows():
    def __init__(self, model, name, showid, short_date, artist, venueid, venue, 
                 location, setlist, notes, rating):
    
        self.model = model
        self.name = name
        self.showid = showid
        self.short_date = short_date
        self.artist = artist
        self.venueid = venueid
        self.venue = venue
        self.location = location 
        self.setlist = setlist
        self.notes = notes
        self.rating = rating
        
        
    @classmethod
    def create_shows(cls, show_dict, model = None):
        name = show_dict['showdate']
        showid = show_dict['showid']
        short_date = show_dict['short_date']
        artist = show_dict['artist']
        venueid = show_dict['venueid']
        venue = show_dict['venue']
        location = show_dict['location']
        setlist = show_dict['setlistdata']
        notes = show_dict['setlistnotes']
        rating = show_dict['rating']
    
        show = Shows(model, name, showid, short_date, artist, venueid, venue,
                     location, setlist, notes, rating)
        return show
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        st = ("Show({}, showid{}, short_date{}, artist{}, venueid{}, venue{},"
                "location{}, setlist{}, notes{}, rating{})").format(self.name, 
                        self.showid, self.short_date, self.artist, self.venueid,
                        self.venue, self.location, self.setlist, self.notes, self.rating)
        return st
    
    def to_dict(self):
        show = OrderedDict()
        return show

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
    
    params = {#Save the base URL for the Phish.in API 
            'phishin_url': 'http://phish.in/api/v1',
            #Save the base URL for the Phish.Net API
            'phishnet_url': 'https://api.phish.net/v3/',
            #the Phish.net API key
            'phishnet_key': 'E972636BCF5D4EF75256',
            #the Phish.net Public key
            'phishnet_public': '4A474082F30E6491601A',
            'subset': 30}   
        
    shows_attended = ['2014-07-25', '2015-08-14', '2015-08-15', '2015-08-16',
                   '2016-06-24', '2016-06-25', '2016-06-26', '2016-08-26',
                   '2016-08-28', '2016-10-21', '2016-10-22', '2017-08-01',
                   '2017-08-02', '2017-08-04', '2017-08-05', '2017-08-06',
                   '2017-12-28', '2017-12-29', '2017-12-30', '2017-12-31',
                   '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-07',
                   '2018-08-08', '2018-08-10', '2018-08-11', '2018-08-12',
                   '2018-10-16', '2018-10-17', '2018-10-19', '2018-10-20',
                   '2018-10-21', '2018-10-26', '2018-10-27']
    
#    model = Phanalytix.load_model('Phanalytix', params, shows_attended, years=['2018'])
    model = Phanalytix.load_model('Phanalytix', params, shows_attended)
    
    years = model.years
    dates = model.dates
    print(type(model.shows))
    shows = model.shows
    print('\n\n', dir(model))
    
    

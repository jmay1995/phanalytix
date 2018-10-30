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

from program.params import PHISHIN_URL, PHISHNET_URL, PHISHNET_KEY, PHISHNET_PUBLIC, DATES_ATTENDED

#Define utility functions for serializing object states
def listify(list_of_obj):
    return [o.todict() for o in list_of_obj]
def dictify(dict_of_obj):
    return {k: v.todict() for k, v in dict_of_obj.items()}

class Phanalytix():
    '''Overall shell set up for model run'''
    def __init__(self, name, shows_attended, years=[], dates = []):
        self.name = name
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

        info('List of Dates and Years processed')
        
        self.shows = self.get_showdata_from_dates()
        
    @classmethod
    def load_model(cls, name, shows_attended, years=[], dates=[]):
        info('Loading model')
        phanalytix = Phanalytix(name, shows_attended, years, dates)
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
        url_years = (PHISHIN_URL + '/years')
        response = requests.get(url_years).json()
        data = response['data']
        info('Sucessfully retrieved list of years Phish has played shows in')
        return data
    
    def get_dates_from_years(self):
        '''
        Get a list of every show played in the years passed through
        '''
        dates = []
        for year in self.years:
            url_year = (PHISHIN_URL + '/years/' + year)
            response = requests.get(url_year).json()
            data = response['data']
            show_count = 0
            for show in data:
                date = show['date']
                dates.append(date)
                show_count +=1
            info('Identified {} dates with concerts played in {}'.format(show_count, year))
        return dates

    def get_showdata_from_dates(self):
        '''
        Create a Show object based on the Phish.net data for a certain date
        '''
        shows = OrderedDict()
        url_base = (PHISHNET_URL + 'setlists/get?apikey=' + PHISHNET_KEY)
        for date in self.dates:
            url_setlist = (url_base + '&showdate=' + date)
            response = requests.get(url_setlist).json()
            data = response['response']['data']
            if data != []:
                data = data[0]
                #Create an instance of the Shows class for the date
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
        info('Show data processed for date {}'.format(name))
        
        
    @classmethod
    def create_shows(cls, show_dict, model = None):
        name = show_dict['showdate']
        showid = show_dict['showid']
        short_date = show_dict['short_date']
        # long_date = show_dict['long_date']
        # relative_date = show_dict['relative_date']
        # url = show_dict['url']
        # gapchart = show_dict['gapchart']
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

    
    

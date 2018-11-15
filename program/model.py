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
import string

from logging import debug, info
from collections import OrderedDict

from program.params import PHISHIN_URL, PHISHNET_URL, PHISHNET_KEY, PHISHNET_PUBLIC, DATES_ATTENDED
from program.utils import Setlist_HTMLParser, ArtistVenue_HTMLParser

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
            self.years = list(set([k[:4] for k in dates.split(' ')]))
            self.dates = dates.split(' ')
        elif dates == []:
            #This allows the user to input a list of years and only query those years
            info('C - Model fed with no input dates, and years: {}'.format(years))
            self.years = years.split(' ')
            self.dates = self.get_dates_from_years()
        else:
            #This allows the user to input a list of years and dates and combine the two
            info('D - Model fed with input years: {} and input dates: {}'.format(years, dates))
            self.years = years.split(' ')
            self.dates = self.get_dates_from_years()
            self.dates.extend(dates.split(' '))

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
                 location, city, state, country, setlist, notes, rating):
    
        self.model = model
        self.name = name
        self.showid = showid
        self.short_date = short_date
        self.artist = artist
        self.venueid = venueid
        self.venue = venue
        self.location = location
        self.city = city
        self.state = state
        self.country = country 
        self.setlist = setlist
        self.notes = notes
        self.rating = rating

        self.songs = self.get_song_data_from_setlist()

        info('Show data processed for date {} \n'.format(name))
 
        
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

        #Parse items still in HTML format into processed text
        parser = ArtistVenue_HTMLParser()
        parser.feed(artist)
        artist = parser.item
        
        parser.feed(venue)
        venue = parser.item

        #Break up Location into items for City, State, and Country
        location_list = location.split(', ')
        location_list = [c for c in location_list if c != '']
        (city, state, country) = location_list

    
        #Create an object of the Shows class to pass back into a list of shows
        show = Shows(model, name, showid, short_date, artist, venueid, venue,
                     location, city, state, country, setlist, notes, rating)
        return show
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        st = ("Show({}, showid{}, short_date{}, artist{}, venueid{}, venue{}, "
                "location{}, city{}, state{}, country{}. setlist{}, notes{}, "
                "rating{})").format(self.name, self.showid, self.short_date, 
                self.artist, self.venueid, self.venue, self.location, 
                self.city, self.state, self.country, self.setlist, 
                self.notes, self.rating)
        return st
    
    def to_dict(self):
        show = OrderedDict()
        return show

    def get_song_data_from_setlist(self):
        '''
        When we pull setlist data from the API it comes in HTML format.
        This method parses that data into a processable format, splitting
        the long string of HTML into song names and performance details
        '''
        #Initialize a blank dict of song objects which we will populate
        songs = OrderedDict()

        #Parse the HTML data into a list of strings
        parser = Setlist_HTMLParser()
        parser.setlist = []
        parser.feed(self.setlist)
        setlist = parser.setlist.copy()

        set_ids = ['Set 1', 'Set 2', 'Set 3', 'Encore', 'Encore 2']

        #remove blanks from the list
        try:
            setlist.remove('\n')
        except: pass

        #Iterate through the list and load song datq
        for i, val in enumerate(setlist):
            #Strip  value to exclude white space
            val = val.strip()
            
            #Identify The set which the songs were played in
            if val in set_ids:
                set_name = val
            else:
                #Do not count notes as songs in the setlist
                if '[' not in val:
                    if val not in string.punctuation and val != '->':
                        name = val
                        notes = None

                        #If we are indexing first or last song of a show avoid error and list transition.
                        if (i-1) < 0:
                            transition_before = ':'
                        else:
                            transition_before = setlist[(i-1)]
                        if (i+1) > (len(setlist)-1):
                            transition_after = ':'
                        else:
                            transition_after = setlist[(i+1)]
                            
                        #Ensure that we do not reference the name of the set as a transition
                        if transition_after in set_ids:
                            transition_after = ':'

                        #Do not count song notes as transition data
                        if '[' in transition_after:
                            notes = transition_after

                            if (i+2) > (len(setlist)-1):
                                transition_after = ':'
                            else:
                                transition_after = setlist[(i+2)]


                            ###################################################
                            ## Look forward through the rest of the list and match the notes together
                            note_idx = (i+2)
                            multiple_tags = False
                            # Identify the location of the footnote data
                            for x in range(len(setlist)-note_idx):
                                #Start your loop after the tag
                                x += note_idx
                                
                                # Pair the footnote tag with its data, but ensure its not an identical tag
                                if (setlist[x][:3]) == notes:
                                   
                                   #Do not assign other tags as the notes
                                    if len(setlist[x]) <= 3:
                                        multiple_tags = True
                                    else:
                                        notes = setlist[x]

                                        #Do not delete the data if there are other tags that need it
                                        if multiple_tags == False:   
                                            del setlist[x]
                                            break



                        #Create an instance of the Song class for this show
                        song = Songs.create_song(name, transition_before, transition_after, set_name, notes, self)
                        songs[name] = song
        return songs

class Songs():
    def __init__(self, show, name, transition_before, transition_after, set_name, notes):
        self.show = show
        self.name = name
        self.transition_before = transition_before
        self.transition_after = transition_after
        self.set_name = set_name
        self.notes = notes

        self.length = 0
        self.gap = 0
        self.rotation = 0 #system
        self.artist = 'Phish' #system
        self.debut = None #system

        info('Processed song {}, {}'.format(self.show, self.name))

    @classmethod
    def create_song(cls, name, transition_before, transition_after, set_name, notes, show = None):
        '''
        Create an object of the song class and return it into the dictonary of
        songs stored in the show class
        '''
        song = Songs(show, name, transition_before, transition_after, set_name, notes)
        return song

    def __str__(self):
        return self.name
    
    def __repr__(self):
        st = ("Show({}, Name{}, transition_before{}, transition_after{}, "
            "set{}, notes{}, length{}, gap{}, rotation{}, artist{}, "
            "debut{}").format(self.show, self.name, self.transition_before, 
            self.transition_after, self.set, self.notes, self.length, self.gap,
            self.rotation, self.artist, self.debut)
        return st
    
    def todict(self):
        '''
        Output a Dict representation of the model
        '''
        return

    
    
#scrape data as tracks from http://phish.net/song
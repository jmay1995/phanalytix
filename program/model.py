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

import numpy as np

from logging import debug, info, warning
from collections import OrderedDict
from bs4 import BeautifulSoup

from program.utils import (Setlist_HTMLParser, ArtistVenue_HTMLParser,
                            SystemSong_HTMLParser, TeaseChart_HTMLParser)
from program.params import (PHISHIN_URL,
                            PHISHNET_URL,
                            PHISHNET_KEY,
                            DATES_ATTENDED,
                            ORIGINAL_ARTIST_URL,
                            ORIGINAL_ARTIST_CLASS,
                            ORIGINAL_ARTIST_PHISH,
                            DATES_TO_EXCLUDE,
                            TEASE_CHART_URL,
                            TEASE_CHART_CLASS,
                            TEASE_CHART_STOPWORDS,
                            SONGNAME_ALIASES)

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
        
        #Exclude dates from radio/TV specials with non processable songs
        self.dates = [c for c in self.dates if c not in DATES_TO_EXCLUDE]
        info('List of Dates and Years processed')

        self.systemsongs = SystemSongs.create_system_songs()
        info('Non-performance-specific song details read in')

        self.tease_list = self.get_tease_data()
        info('Tease data read in')

        self.shows = self.get_showdata_from_dates()
        info('Show data processed')

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

    def get_tease_data(self):
        '''
        Scrape phish.net tease chart data and compile it into a dictionary
        We will use this data when generating song objects
        '''
        #Read in HTML code from Phish.Net tease chart
        html_string = requests.get(TEASE_CHART_URL).text
        #Process HTML into a parseable format
        soup = BeautifulSoup(html_string, 'lxml')
        #Save only the text from the table we need
        my_table = soup.find('table',{'class': TEASE_CHART_CLASS})

        #Create an object that will store parsed HTML tags
        parser = TeaseChart_HTMLParser()
        parser.original_artist = []
        #Load HTML into parser that will load the empty list we just initialized
        parser.feed(str(my_table))
        #Name the list made from the processed HTML data
        tease_list = parser.original_artist

        #Loop Through the list, delete the linebreaks, and flag the start of each song
        i = 0
        while i < len(tease_list):
            if tease_list[i] == "\n":
                if tease_list[i-1][:5] in TEASE_CHART_STOPWORDS:
                    #If the value is a linebreak ahead of a year, it is a new song
                    tease_list[i] = '_____'
                    i += 1
                else:
                    #If it is a linebreak on its own, then delete it- it's just noise
                    del tease_list[i]
            else: i += 1
        #Delete the last item from the list, it's an underscore and causes index errors later
        del tease_list[-1]

        #Loop through the cleaned list and load all tease data into a dictionary
        processed_teases = []
        for i, val in enumerate(tease_list):
            if val == '_____':
                #When we hit a new tease, load the title and artist of the tease
                tease = tease_list[i+1]
                artist = tease_list[i+2]
                
                #Look foward and loop through all the listings of times that song was teased
                idx = i + 4
                condition = True
                while condition and idx < len(tease_list):
                    if tease_list[idx] != '_____':
                        #Log tease performances into  until you hit a new tease
                        date = tease_list[idx][:10]
                        song = tease_list[idx][11:]
                        info('Processing Tease: {} by {} during {} {}'
                            .format(tease, artist, date, song))

                        #Add performance details into list as tuple
                        tease_tuple = (date, song, tease, artist)
                        processed_teases.append(tease_tuple)
                        idx += 1
                    else:
                        #Once you hit the new song stop, end the subloop
                        condition = False

        return processed_teases

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

        #get the subset of the modelwide teasedict that applies to this date
        self.tease_list = [c[1:4] for c in self.model.tease_list if c[0]==self.name]

        self.song_details = self.get_performance_details()

        self.songs = self.get_song_data_from_setlist()

        info('Show data processed for date {} \n'.format(name))
        
        #Check for places where Phish.Net did not merge with Phish.In data
        if len(self.tease_list) > 0:
            warning('Teases remaining that could not be paired to a song: {}'
                .format(self.tease_list))
        if len(self.song_details) > 0:
            warning('Song details remining that could not be paired to a song: {}'
                .format(self.song_details))

        #delete the info that we only needed for loading individual songs
        del self.setlist
        del self.tease_list
        del self.song_details
 
        
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

        if len(location_list) == 2:
            (city, country) = location_list
            state = country
        else:
            (city, state, country) = location_list

    
        #Create an object of the Shows class to pass back into a list of shows
        show = Shows(model, name, showid, short_date, artist, venueid, venue,
                     location, city, state, country, setlist, notes, rating)
        return show
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        st = ("Show({}, showid{}, short_date{}, artist{}, venueid{}, venue{}, "
                "location{}, city{}, state{}, country{}, notes{}, "
                "rating{}, songs{})").format(self.name, self.showid, self.short_date, 
                self.artist, self.venueid, self.venue, self.location, 
                self.city, self.state, self.country, 
                self.notes, self.rating, self.songs)
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

        set_ids = ['Set 1', 'Set 2', 'Set 3', 'Set 4', 'Set 5', 'Encore', 'Encore 2']

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
                        if (transition_after in set_ids):
                            transition_after = ':'

                        #Do not count song notes as transition data
                        if '[' in transition_after:
                            notes = transition_after

                            if (i+2) > (len(setlist)-1):
                                transition_after = ':'
                            else:
                                transition_after = setlist[(i+2)]
                                
                                #Once we have assigned a foward index, verify 
                                #again that it is not notes from the end of show
                                if ('[' in transition_after or transition_after in set_ids):
                                    transition_after = ':'



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
                                        notes = setlist[x][4:]

                                        #Do not delete the data if there are other tags that need it
                                        if multiple_tags == False:   
                                            del setlist[x]
                                            break

                        #Create an instance of the Song class for this show
                        song = Songs.create_song(name, transition_before, transition_after, set_name, notes, self)
                        songs[name] = song
        return songs

    def get_performance_details(self):
        #Get the API URL for this specific show
        url_show = (PHISHIN_URL + '/shows/' + self.name)
        #Parse API data as JSON format
        response = requests.get(url_show).json()
        data = response['data']

        #Create an empty list that we will load with each of the songs
        song_details = []
        #Loop through all the show data and create an tuple for each song played
        for track in data['tracks']:
            name = track['title']
            duration = track['duration']
            tags = track['tags']
            #Combine the user submitted like count for the song and show into a composite number
            likes = track['likes_count'] + data['likes_count']
            #Load all the details into a tuple, and compile each tuple into a list
            track_tuple = (name, duration, tags, likes)
            song_details.append(track_tuple)

        return song_details

class Songs():
    def __init__(self, show, name, transition_before, transition_after, set_name, notes):
        self.show = show
        self.name = name
        self.transition_before = transition_before
        self.transition_after = transition_after
        self.set_name = set_name
        self.notes = notes

        #Associate each song to a system song to get non-performance specific details
        self.systemsong = self.associate_systemsong()
        
        #Associated teases played with each performance of a song
        self.teases = self.associate_teases()

        self.duration, self.tags, self.likes = self.associate_song_details()

        info('Processed song {}, {}'.format(self.show, self.name))
        # debug('SystemSong: {},{}'.format(self.systemsong.name, self.systemsong.artist))

    @classmethod
    def create_song(cls, name, transition_before, transition_after, set_name, notes, show = None):
        '''
        Create an object of the song class and return it into the dictonary of
        songs stored in the show class
        '''
        song = Songs(show, name, transition_before, transition_after, set_name, notes)
        return song

    def associate_systemsong(self):
        '''
        Looks through the list of systemsongs and associates a system song
        object with this song performance to get non-performance specific
        details such as: original artist, debut, times played, etc.
        '''
        #Get a list of system songs which share the same title or alias
        systemsongs = [c for c in self.show.model.systemsongs 
                        if (self.name==c.name) or (self.name==c.aliases)]
        
        if len(systemsongs) == 0:
            #If there is no system song, then look to match without descriptors
            temp_name = self.name.replace(" Reprise", "")
            temp_name = temp_name.replace(" Jam", "")
            systemsongs = [c for c in self.show.model.systemsongs 
                             if (temp_name==c.name) or (temp_name==c.aliases)]

        if len(systemsongs) == 0:
            #Send error if still no System Song aligns with the song performed
            systemsong = None
            warning('No SystemSong associated with Song performed ({})'.
                format(self.name))
        else:
            #Assign the first SystemSong in the list to the song performed
            systemsong = systemsongs[0]
            
            if len(systemsongs) > 1:
                #FIXME: This is a very hard coded exception, find workaround
                if self.name == "Let's Go":
                    if self.show.name[:4] != '1991':
                        systemsong = systemsongs[1]
                else:
                    #Throw a warning is multiple SystemSongs align with the song
                    warning('Multiple SystemSongs ({}) associated with Song performed ({})'
                        .format(systemsongs, self.name))

        return systemsong

    def associate_teases(self):
        '''
        Looks in the list of teases performed at that show and pairs them with
        the song that they were played during
        '''
        # Initialize an empty list that we will add too
        teases = []
        #Loop through list of teases performed at that show and add to object
        i = 0
        while i < len(self.show.tease_list):
            val = self.show.tease_list[i]
            if (val[0] == self.name) or (val[0] in self.systemsong.aliases):
                #Pair if the song name or song alias aligns then add it to the list
                teases.append('{} by {}'.format(val[1], val[2]))
                #Remove the action from the show tease list so we can track
                #If any teases are leftover and didnt line up
                del self.show.tease_list[i]
            else:
                #If a tease didnt happen during this song then keep iterating
                i += 1

        return teases

    def associate_song_details(self):
        #Create default values to return if we do not find a match
        duration = np.nan
        tags = []
        likes = np.nan

        #Establish our loop indeces and conditions
        i = 0
        condition = True
        #Loop through list of tuples to find the song we align with
        while i < len(self.show.song_details) and condition:
            if (self.name == self.show.song_details[i][0]) or\
                (self.show.song_details[i][0] in self.systemsong.aliases):
                #Pair the details with the song if they share a name or alias

                #Extract values from the Tuple to be returned to the object
                duration = self.show.song_details[i][1]
                tags = self.show.song_details[i][2]
                likes = self.show.song_details[i][3]
                #Once we have assigned song details, delete it from the list
                # This is a safeguard for when they play a song twice in a show
                del self.show.song_details[i]
                #Stop the loop so we dont hit another match and overwrite
                condition = False
            else: 
                #Iterate through the list until we find a match
                i += 1
        return duration, tags, likes

    def __str__(self):
        return self.name
    
    def __repr__(self):
        st = ("Song({}, Name{}, transition_before{}, transition_after{}, "
            "set_name{}, notes{}, systemsong{}, teases{}, duration{}, tags{}, "
            "likes{}").format(
            self.show, self.name,self.transition_before, self.transition_after, 
            self.set_name, self.notes, self.systemsong, self.teases,
            self.duration, self.tags, self.likes)
        return st
    
    def todict(self):
        '''
        Output a Dict representation of the model
        '''
        return

class SystemSongs():
    def __init__(self, name, artist, times, debut, last, current_gap, aliases):
        self.name = name
        self.artist = artist
        self.times = times
        self.debut = debut
        self.last = last
        self.current_gap = current_gap
        self.aliases = aliases

        self.cover = 0
        if self.artist not in ORIGINAL_ARTIST_PHISH:
            self.cover = 1

        self.shows_since_debut = None
        self.rotation = None
        
        # debug('SystemSong: {}, {}, {}, {}, {}, {}'.format(
            # self.name, self.artist, self.times, self.debut, self.last, self.current_gap))

        info('Processed SystemSong: {}'.format(self.name))
        if self.aliases != []:
            info('\tSystemSong has aliases: {}'.format(self.aliases))

    @classmethod
    def create_system_songs(self):
        '''
        Scrape Phish.net song history to get data on non-performance-specific
        song details such as original artist, times played, rotation, debut. etc.
        '''
        #Read in HTML code from Phish.Net Songs page
        html_string = requests.get(ORIGINAL_ARTIST_URL).text
        #Process HTML into a parseable format
        soup = BeautifulSoup(html_string, 'lxml')
        #Save only the text from the table we need
        song_table = soup.find('table',{'class':ORIGINAL_ARTIST_CLASS})

        #Create an object that will store parsed HTML tags
        parser = SystemSong_HTMLParser()
        parser.system_song = []
        #Load HTML code into parser that will load the empty list we just created
        parser.feed(str(song_table))

        #Loop through list of system song data and create dict of Aliases ahead of time
        alias_dict = {}
        i = 6
        while i < len(parser.system_song):
            if 'Alias of' in parser.system_song[(i+2)]:
                #If the listing are for a song name alias, record and delete
                alias_dict[parser.system_song[(i+3)]] = parser.system_song[i]
                del parser.system_song[(i+3)]
                del parser.system_song[(i+2)]
                del parser.system_song[(i+1)]
                del parser.system_song[i]
            elif 'Found in Discography' in parser.system_song[(i+2)]:
                #If the song has never been performed, we dont want to list it
                del parser.system_song[(i+2)]
                del parser.system_song[(i+1)]
                del parser.system_song[i]
            elif 'Found in Discography' in parser.system_song[(i+1)]:
                #If the song has never been performed, we dont want to list it
                del parser.system_song[(i+1)]
                del parser.system_song[i]
            else:
                i += 6

        #Loop through list of system song data and load it into an list of objects
        systemsong_list = []
        i = 6   
        while i < len(parser.system_song):
            name = parser.system_song[i]
            artist = parser.system_song[(i+1)]
            times = parser.system_song[(i+2)]
            debut = parser.system_song[(i+3)]
            last = parser.system_song[(i+4)]
            current_gap = parser.system_song[(i+5)]

            #Get all the manually imputed alias, and contribute to it
            aliases = [c for c in SONGNAME_ALIASES.keys()
                        if SONGNAME_ALIASES[c] == name]
            for k, v in alias_dict.items():
                if k == name:
                    aliases.append(v)

            #Create a SystemSong object and add it to the list to return
            systemsong = SystemSongs(name, artist, times, debut, last, current_gap, aliases)
            systemsong_list.append(systemsong)

            i += 6
        return systemsong_list
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        st = ("SystemSong(name{}, artist{}, times{}, debut{}, last{}, current_gap{}, "
            "aliases{}, cover{}, shows_since_debut{}, rotation{})").format(self.name,
            self.artist, self.times, self.debut, self.last, self.current_gap,
            self.aliases, self.cover, self.shows_since_debut, self.rotation)
        return st
    
    def todict(self):
        '''
        Output a Dict representation of the model
        '''
        return

class PerformanceStatisticsProcessor():
    '''
    Class is feed the full loaded phanalytix model with all scraped data and
    iterates through every performance to process statistics such as song gap
    for each performance, cumulative times playes, and song rotation.
    '''
    def __init__(self, model):
        self.model = model
        
        self.calculate_performance_statistics()

        info('Performance Statistics Processed')

    def calculate_performance_statistics(self):
        '''
        Loop through shows and count how many shows pass between the performance
        of each song
        '''
        #Create an empty dictionary that will store songgaps
        song_tracker = {}
        #Tuple = (times played, total shows played, shows since debut, gap, rotation)

        #Keep a counter on shows played
        show_counter = 0
        #Loop through every show played
        for show in self.model.shows.values():
            #increment the show counter
            show_counter += 1
            #Loop through each song performed at that show
            for song in show.songs.values():
                if song.name not in song_tracker.keys():
                    # If the song is being played for the first time

                    # Load a dictionary with details to track metrics to record
                    song_dict = {
                        'debut': show_counter,
                        'last_time_played': show_counter,
                        'times_played': 1,
                        'gap' : np.nan,
                        'rotation' : np.nan
                    }
                    # Record song details into song tracker
                    song_tracker[song.name] = song_dict
                else:
                    # Check if the song has been played before
                    
                    # Update and increment the song's metrics
                    song_tracker[song.name]['times_played'] += 1
                    song_tracker[song.name]['gap'] = (show_counter
                        - song_tracker[song.name]['last_time_played'])
                    song_tracker[song.name]['rotation'] = (
                        float(song_tracker[song.name]['times_played'])
                        /(show_counter - song_tracker[song.name]['debut']))
                    song_tracker[song.name]['last_time_played'] = show_counter

                #Take items recorded in song_tracker and write them to object
                song.times_played = song_tracker[song.name]['times_played']
                song.gap = song_tracker[song.name]['gap']
                song.rotation  = song_tracker[song.name]['rotation']


import os
import pandas as pd


from logging import debug, info
from collections import OrderedDict
from html.parser import HTMLParser
from program.params import OUTPUTDIR, DATES_ATTENDED

class WriteOutputs():
    '''
    Class takes object-oriented data storage and parses contents into datafranes
    '''
    def __init__(self, phanalytix):
        info('Processing data into output tables')
        self.phanalytix = phanalytix
        self.output_df = pd.DataFrame()

    def process_and_write_outputs(self):
        '''
        Call methods that loop through object model and create outputs
        Next compile output sheets into an Excel File
        '''
        self.process_songs_and_shows()
        info('Songs and Shows dataframe created')

        # Create and initialize excel Output file
        excel_fp = os.path.join(OUTPUTDIR, 'phanalytix_outputs.xlsx')
        excelOutput = pd.ExcelWriter(excel_fp, engine='xlsxwriter')

        #Write each DF to the excel sheet as tabs
        self.output_df.to_excel(excelOutput, sheet_name='Phanalytix')
        
        #Write the excel file to directory
        excelOutput.save()
        info('Model outputs written to directory {}'.format(excel_fp))


    def process_songs_and_shows(self):
        '''
        Loop through the layers of the object model and add values to a dataframe
        row by row reporting our data
        '''
        for show in self.phanalytix.shows.values():
            for song in show.songs.values():
                # Bring in show based indeces
                outputdict = OrderedDict(Date = [show.short_date])
                outputdict['Venue'] = show.venue
                outputdict['City'] = show.city
                outputdict['State'] = show.state
                outputdict['Country'] = show.country
                outputdict['Rating'] = show.rating

                outputdict['Likes'] = song.likes
                
                # Bring in song data
                outputdict['Set'] = song.set_name
                outputdict['Before'] = song.transition_before
                outputdict['Song'] = song.name
                outputdict['After'] = song.transition_after

                outputdict['Duration'] = song.duration
                outputdict['Tags'] = ", ".join(song.tags)
                outputdict['Teases'] = ", ".join(song.teases)
                outputdict['Notes'] = song.notes

                outputdict['Artist'] = song.systemsong.artist
                outputdict['Cover'] = song.systemsong.cover
                outputdict['Debut'] = song.systemsong.debut
                outputdict['Times Played'] = song.systemsong.times

                outputdict['Times Played2'] = song.times_played
                outputdict['Gap'] = song.gap
                outputdict['Rotation'] = song.rotation

                outputdict['Attended'] = show.name in DATES_ATTENDED

                # outputdict['ShowNotes'] = show.notes
                
                row = pd.DataFrame(data = outputdict)
                self.output_df = self.output_df.append(row, ignore_index=True, sort=False)

class Setlist_HTMLParser(HTMLParser):

    def handle_data(self, data):
        self.setlist.append(data)

class ArtistVenue_HTMLParser(HTMLParser):

    def handle_data(self, data):
        self.item = data

class SystemSong_HTMLParser(HTMLParser):

    def handle_data(self, data):
        if data != '\n':
            self.system_song.append(data)

class TeaseChart_HTMLParser(HTMLParser):

    def handle_data(self, data):
        if data != ", ":
            self.original_artist.append(data)
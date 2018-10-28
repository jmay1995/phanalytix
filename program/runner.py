import logging

from logging import debug, info

from program.model import Phanalytix
from program.params import DATES_ATTENDED

def runner():

    #Load the object Model with Show Data
    model = Phanalytix.load_model('Phanalytix', DATES_ATTENDED)
    # model = Phanalytix.load_model('Phanalytix', params, shows_attended, years=['2018'])

    # years = model.years
    # dates = model.dates
    # print(type(model.shows))
    # shows = model.shows
    # print('\n\n', dir(model))
import logging

from logging import debug, info

from program.model import Phanalytix
from program.utils import WriteOutputs
from program.params import DATES_ATTENDED

def runner():

    #Add capacity for click to move args to command line

    # Load the object Model with Show Data
    # model = Phanalytix.load_model('Phanalytix', DATES_ATTENDED)

    #Move away from class method initialization to a direct declaration
    
    model = Phanalytix.load_model('Phanalytix', DATES_ATTENDED, years = ['2018'])

    #Parse contents as dataFrames and write to file
    outputs = WriteOutputs(model)
    outputs.process_and_write_outputs()

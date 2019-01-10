import logging
import click

from logging import debug, info

from program.model import Phanalytix
from program.utils import WriteOutputs
from program.params import DATES_ATTENDED

#Enable default values for the command line
@click.command()
@click.option('--years', default=[], help='Years to limit data pull to, seperated by spaces')
@click.option('--dates', default=[], help='Show dates to limit data pull to, YY-MM-DD, seperated by spaces')
def runner(years, dates):

    # Load the object Model with Show Data
    model = Phanalytix('Phanalytix', DATES_ATTENDED, years, dates)

    #Parse contents as dataFrames and write to file
    outputs = WriteOutputs(model)
    outputs.process_and_write_outputs()

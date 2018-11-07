
import os

# Base URL for the phish.in API
PHISHIN_URL = 'http://phish.in/api/v1'

# Base URL for the Phish.Net API
PHISHNET_URL = 'https://api.phish.net/v3/'

#Phish.Net API Key
PHISHNET_KEY = 'E972636BCF5D4EF75256'

# Phish.net Public Key
PHISHNET_PUBLIC = '4A474082F30E6491601A'

# List of shows Attended
DATES_ATTENDED = ['2014-07-25', '2015-08-14', '2015-08-15', '2015-08-16',
                '2016-06-24', '2016-06-25', '2016-06-26', '2016-08-26',
                '2016-08-28', '2016-10-21', '2016-10-22', '2017-08-01',
                '2017-08-02', '2017-08-04', '2017-08-05', '2017-08-06',
                '2017-12-28', '2017-12-29', '2017-12-30', '2017-12-31',
                '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-07',
                '2018-08-08', '2018-08-10', '2018-08-11', '2018-08-12',
                '2018-10-16', '2018-10-17', '2018-10-19', '2018-10-20',
                '2018-10-21', '2018-10-26', '2018-10-27']

WORKINGDIR = os.getcwd()
OUTPUTDIR = os.path.join(os.getcwd(), 'Outputs')
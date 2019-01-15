
import os

# Base URL for the phish.in API
PHISHIN_URL = 'http://phish.in/api/v1'

# Base URL for the Phish.Net API
PHISHNET_URL = 'https://api.phish.net/v3/'

#Phish.Net API Key
PHISHNET_KEY = 'E972636BCF5D4EF75256'

# List of shows Attended
DATES_ATTENDED = ['2014-07-25', '2015-08-14', '2015-08-15', '2015-08-16',
                '2016-06-24', '2016-06-25', '2016-06-26', '2016-08-26',
                '2016-08-28', '2016-10-21', '2016-10-22', '2017-08-01',
                '2017-08-02', '2017-08-04', '2017-08-05', '2017-08-06',
                '2017-12-28', '2017-12-29', '2017-12-30', '2017-12-31',
                '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-07',
                '2018-08-08', '2018-08-10', '2018-08-11', '2018-08-12',
                '2018-10-16', '2018-10-17', '2018-10-19', '2018-10-20',
                '2018-10-21', '2018-10-26', '2018-10-27', '2018-10-28', 
                '2018-10-31', '2018-11-01', '2018-11-02', '2018-11-03', 
                '2018-12-28', '2018-12-29', '2018-12-30', '2018-12-31']

WORKINGDIR = os.getcwd()
OUTPUTDIR = os.path.join(os.getcwd(), 'Outputs')

#Details for Scraping System Song original data
ORIGINAL_ARTIST_URL = 'https://phish.net/song'
ORIGINAL_ARTIST_CLASS = 'table table-striped table-hover table-responsive'

ORIGINAL_ARTIST_PHISH = ['Phish', 'Trey Anastasio', 'Page McConnell', 'Mike Gordon',
                    'Mike Gordon Band', 'Jon Fishman', 'Tom Marshall', 'Amfibian',
                    'New York!', 'Vida Blue', 'Pork Tornado', 'Touchpants', 
                    'Space Antelope', 'Steve Pollak', 'The Dude of Life', 
                    'The Dude of Life and Phish', 'The Dude of Life (with Phish)',
                    'Jeff Holdsworth', 'Marc Daubert', 'Aaron Woolf']

DATES_TO_EXCLUDE = ['1997-02-26', '1998-08-14', '2009-10-29', '2010-03-15']


TEASE_CHART_URL = 'https://phish.net/tease-chart'
TEASE_CHART_CLASS = 'table table-responsive table-striped'
TEASE_CHART_STOPWORDS = ['Dates','1982-','1983-','1984-','1985-','1986-','1987-',
                        '1988-','1989-','1990-','1991-','1992-','1993-','1994-',
                        '1995-','1996-','1997-','1998-','1999-','2000-','2001-',
                        '2002-','2003-','2004-','2005-','2006-','2007-','2008-',
                        '2009-','2010-','2011-','2012-','2013-','2014-','2015-',
                        '2016-','2017-','2018-','2019-','2020-','2021-','2022-']

SONGNAME_ALIASES = {'Hood': 'Harry Hood',
                    'LxL': 'Limb By Limb',
                    "Wolfman's": "Wolfman's Brother",
                    'Weekapaug': 'Weekapaug Groove',
                    "Mike's": "Mike's Song",
                    'SOAMelt': 'Split Open and Melt',
                    'BOAF': 'Birds of a Feather',
                    'C&P': 'Crosseyed and Painless',
                    'Timber Ho': 'Timber (Jerry The Mule)',
                    'Timber (Jerry)':  'Timber (Jerry The Mule)',
                    'DwD': 'Down with Disease',
                    'CDT': 'Chalk Dust Torture',
                    'NMINML': "No Men In No Man's Land",
                    'Gin': 'Bathtub Gin',
                    'Destiny': 'Destiny Unbound',
                    "Halley's": "Halley's Comet",
                    "Sneakin' Sally": "Sneakin' Sally Through the Alley",
                    'Tweeprise': 'Tweezer Reprise',
                    'Bowie': 'David Bowie',
                    'WotC': 'Walls of the Cave',
                    'Makisupa': 'Makisupa Policeman',
                    'Mockingbird': 'Fly Famous Mockingbird',
                    'Caspian': 'Prince Caspian',
                    'WTU?': "What's the Use?",
                    'SOAMule': 'Scent of a Mule',
                    'Quinn': 'Quinn the Eskimo',
                    'Suzy': 'Suzy Greenberg',
                    'Wedge': 'The Wedge',
                    'Moma': 'The Moma Dance',
                    'Divided': 'Divided Sky',
                    'Theme': 'Theme From the Bottom',
                    'My Friend': 'My Friend, My Friend',
                    'R&R': 'Rock and Roll',
                    'STFTFP': 'Stealing Time From the Faulty Plan',
                    'Boogie On': 'Boogie On Reggae Woman',
                    'KDF': 'Kill Devil Falls',
                    'Bag': 'AC/DC Bag',
                    'Billie Jean': 'Billie Jean Jam',
                    'Mango': 'The Mango Song',
                    'FEFY': 'Fast Enough For You',
                    'Coil': 'The Squirming Coil',
                    'BDTNL': 'Backwards Down the Number Line',
                    'FYF': 'Fuck Your Face',
                    'Slave': 'Slave to the Traffic Light',
                    'Happy Birthday': 'Happy Birthday to You',
                    'CTB': 'Cars Trucks Buses',
                    'Hydrogen': 'I Am Hydrogen',
                    'Alumni': 'Alumni Blues',
                    "'A' Train": "Take the 'A' Train",
                    'McGrupp': 'McGrupp and the Watchful Hosemasters',
                    'Lizards': 'The Lizards',
                    'Golgi': 'Golgi Apparatus',
                    'Landlady': 'The Landlady',
                    'MSO': 'My Sweet On',
                    'DEG': "Dave's Energy Guide ",
                    'IDK': "I Didn't Know",
                    "Bouncin'": 'Bouncing Around the Room',
                    'BBJ': 'Big Ball Jam',
                    'Guelah': 'Guelah Papyrus',
                    'Great Gig in the Sky': 'The Great Gig in the Sky',
                    'Horse': 'The Horse',
                    'Peaches': 'Peaches en Regalia',
                    'Sweet Emotion': 'Sweet Emotion',
                    'Vibration of Life': 'The Vibration of Life',
                    'YEM': 'You Enjoy Myself',
                    'Sample': 'Sample in a Jar',
                    'JBG': 'Johnny B. Goode',
                    'JJLC': 'Jesus Just Left Chicago',
                    'Jibboo': 'Gotta Jibboo',
                    'Light Up': 'Light Up Or Leave Me Alone',
                    'Curtain With': 'The Curtain With',
                    'Sloth': 'The Sloth',
                    'Curtis Loew': 'The Ballad of Curtis Loew',
                    'Llama (Slow)': 'Llama'}
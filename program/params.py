
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

SONGNAME_ALIASES = {'Harry Hood' : 'Hood',
                    'Limb By Limb' : 'LxL',
                    "Wolfman's Brother" : "Wolfman's",
                    'Weekapaug Groove' : 'Weekapaug',
                    "Mike's Song" : "Mike's",
                    'Split Open and Melt' : 'SOAMelt',
                    'Birds of a Feather' : 'BOAF',
                    'Crosseyed and Painless' : 'C&P',
                    'Timber (Jerry The Mule)' : 'Timber Ho',
                    'Down with Disease' : 'DwD',
                    'Chalk Dust Torture' : 'CDT',
                    "No Men In No Man's Land" : 'NMINML',
                    'Bathtub Gin' : 'Gin',
                    'Destiny Unbound' : 'Destiny',
                    "Halley's Comet" : "Halley's",
                    "Sneakin' Sally Through the Alley" : "Sneakin' Sally",
                    'Tweezer Reprise' : 'Tweeprise',
                    'David Bowie' : 'Bowie',
                    'Walls of the Cave' : 'WotC',
                    'Makisupa Policeman' : 'Makisupa',
                    'Fly Famous Mockingbird' : 'Mockingbird',
                    'Prince Caspian' : 'Caspian',
                    "What's the Use?" : 'WTU?',
                    'Scent of a Mule' : 'SOAMule',
                    'Quinn the Eskimo' : 'Quinn',
                    'Suzy Greenberg' : 'Suzy',
                    'The Wedge' : 'Wedge',
                    'The Moma Dance' : 'Moma',
                    'Divided Sky' : 'Divided',
                    'Theme From the Bottom' : 'Theme',
                    'My Friend, My Friend' : 'My Friend',
                    'Rock and Roll' : 'R&R',
                    'Stealing Time From the Faulty Plan' : 'STFTFP',
                    "Boogie On Reggae Woman" : 'Boogie On',
                    "Kill Devil Falls" : 'KDF',
                    "AC/DC Bag" : 'Bag',
                    "Billie Jean Jam" : 'Billie Jean',
                    "The Mango Song" : 'Mango',
                    "Fast Enough For You" : 'FEFY',
                    "The Squirming Coil" : 'Coil',
                    "Backwards Down the Number Line" : 'BDTNL',
                    "Fuck Your Face" : 'FYF',
                    "Slave to the Traffic Light" : 'Slave',
                    "Happy Birthday to You" : 'Happy Birthday',
                    "Cars Trucks Buses" : 'CTB',
                    "I Am Hydrogen" : 'Hydrogen',
                    "Alumni Blues" : 'Alumni',
                    "Take the 'A' Train" : "'A' Train",
                    "McGrupp and the Watchful Hosemasters" : 'McGrupp',
                    "The Lizards" : 'Lizards',
                    "Golgi Apparatus" : 'Golgi',
                    "The Landlady" : 'Landlady',
                    "My Sweet On" : 'MSO',
                    "Dave's Energy Guide " : 'DEG',
                    "I Didn't Know" : 'IDK',
                    "Bouncing Around the Room" : "Bouncin'",
                    "Big Ball Jam" : 'BBJ',
                    "Guelah Papyrus" : 'Guelah',
                    "The Great Gig in the Sky" : 'Great Gig in the Sky',
                    "The Horse" : 'Horse',
                    "Peaches en Regalia" : 'Peaches',
                    "David Bowie" : 'Bowie',
                    "Sweet Emotion" : 'Sweet Emotion',
                    "The Vibration of Life" : 'Vibration of Life',
                    "You Enjoy Myself" : 'YEM',
                    "Sample in a Jar" : 'Sample',
                    "Johnny B. Goode" : 'JBG',
                    "Jesus Just Left Chicago" : 'JJLC',
                    "Gotta Jibboo" : 'Jibboo',
                    "Light Up Or Leave Me Alone" : 'Light Up'}
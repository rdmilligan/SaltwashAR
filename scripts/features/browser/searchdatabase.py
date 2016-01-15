# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

from constants import *

# search table
SEARCH_TABLE = [(ROCK, [('pixies news', 'https://www.teamrock.com/news/2015-06-03/pixies-working-on-6th-record'), ('lush reunion', 'http://www.nme.com/news/lush/88713')]), (SPORT, [('football', 'http://www.dailymail.co.uk/sport/football/index.html'), ('andy murray ice cream', 'http://www.sbnation.com/2015/8/18/9174215/andy-murray-dresses-up-as-an-ice-cream-worker')])]

# match category and term to database record
def search_engine(category, term):
    url = ''

    for record in SEARCH_TABLE:
        if record[0] == category:
            for category_item in record[1]:
                if category_item[0] == term.lower():
                    url = category_item[1]
                    break

        if url: break

    return url
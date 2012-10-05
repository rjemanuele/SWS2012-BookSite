#!/usr/local/bin/python

import sys
import random
import pprint
import pickle
from django.core.cache import cache
import base64
from amazonproduct import NoExactMatchesFound
from amazonproduct import API

AWS_KEY = 'AKIAJ7B6DSAVWVFPC7RQ'
SECRET_KEY = '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'
ASSOCIATE_TAG = 'wwwdarktoneco-20'
TOP = 10

RESULTS_PER_PAGE = 10 # defined by amazon
MAX_PAGES = 10 # defined by amazon
RESULT_LIMIT = RESULTS_PER_PAGE * MAX_PAGES 
CACHE_LIFE = 2 * 60 * 60 # stretch the cache to 2 hours

# the responses are usually in UTF-8, move this somewhere else
reload(sys)
sys.setdefaultencoding("utf-8")

Genres = [{'name':'No Genre Preference', 'value':' ', 'text_field_value':'Genre'},
          {'name':'Arts & Photography'},
          {'name':'Bargain Books'},
          {'name':'Biographies & Memoirs'},
          {'name':'Business & Investing'},
          {'name':'Children\'s Books'},
          {'name':'Christian Books & Bibles'},
          {'name':'Comics & Graphic Novels'},
          {'name':'Cook Books, Food & Wine'},
          {'name':'Crafts Hobbies & Home'},
          {'name':'Computers & Technology'},
          {'name':'Education & Reference'},
          {'name':'Gay & Lesbian'},
          {'name':'Health, Fitness & Dieting'},
          {'name':'History'},
          {'name':'Humor & Entertaining'},
          {'name':'Law'},
          {'name':'Literature & Fiction'},
          {'name':'Medicine'},
          {'name':'Mystery, Thriller & Suspense'},
          {'name':'Parenting & Relationships'},
          {'name':'Politics & Social Sciences'},
          {'name':'Professional & Technical Books'},
          {'name':'Religion & Spirituality'},
          {'name':'Romance'},
          {'name':'Science & Math'},
          {'name':'Science Fiction & Fantasy'},
          {'name':'Sports & Outdoors'},
          {'name':'Teens'},
          {'name':'Travel'},
          ]

BookAges = [{'name':'No Book Age Preference', 'value':-1, 'text_field_value':'Book Age'},
            {'name':'This Year', 'value':1},
            {'name':'Within 2 Years', 'value':2},
            {'name':'Within 5 Years', 'value':5},
            {'name':'Within 10 Years', 'value':10},
            {'name':'Within 20 Years', 'value':20},
            {'name':'Older than 20 Years', 'value':21},
            ]


Popularities = [{'name':'All', 'value':-1, 'text_field_value':'Popularity'},
                {'name':'Top %d'%TOP, 'value':1},
                {'name':'Exclude Top %d'%TOP, 'value':0}
                ]


def power_string(subject, year, before):
    '''
    Creates an Amazon Power Search String

    :param subject: A Subject string
    :param year: Year to search about
    :param before: Boolean for before or after the year
    '''
    if (before):
        param = 'before'
    else:
        param = 'after'

    return 'pubdate:'+param+' '+str(year)+' and binding: not kindle and (subject:'+ subject+')'


def get_book_set(power):
    '''
    Get a set of books from Amazon that match the power search

    :param power: A power searchstring
    '''
    api = API(AWS_KEY, SECRET_KEY, 'us', ASSOCIATE_TAG)

    roots = api.item_search('Books', ResponseGroup='Large,EditorialReview', Power=power, Sort = "salesrank")

    result_count = roots.results
    page_count = roots.pages

    if ( result_count > RESULT_LIMIT ):
        result_count = RESULT_LIMIT

    if ( page_count > MAX_PAGES ):
        page_count = MAX_PAGES

    current_page = 1

    book_set = []

    count = 0
    if (result_count):
        for root in roots:
            nspace = root.nsmap.get(None, '')
            books = root.xpath('//aws:Items/aws:Item', namespaces={'aws' : nspace})
            for book in books:
                result_count = result_count - 1
                count = count + 1
                try:
                    author = book.ItemAttributes.Author
                except:
                    try:
                        author = book.ItemAttributes.Creator
                    except:
                        author = 'Unknown Author'

                #print "%d  %s: %s - %s"%(count, book.ASIN, author, book.ItemAttributes.Title)
                book_set.append(book)

                if (not result_count):
                    break;
            if (not result_count):
                break;

    return book_set


def get_book(genre, popularity, year, before):
    '''
    Get a random book from the Top 100 with some constraints

    :param genre: specify a genre or empty string for all
    :param popularity: -1 = anywhere, 0 = top TOP, 1 = below top TOP
    :param year: a year to search about
    :param before: boolean before or after the year specified
    '''

    genre = genre.replace('&amp;', ' ')
    genre = genre.replace('&', ' ')
    genre = genre.replace(',', ' ')

    power = power_string(genre, year, before)

    try:
        books = pickle.loads(cache.get(base64.b64encode(power)))
    except:
        books = get_book_set(power)
        cache.set(base64.b64encode(power),pickle.dumps(books), CACHE_LIFE)

    if (len(books) < TOP):
        popularity = -1

    if (popularity < 0):
        num = random.randrange(1, len(books))
    elif (popularity):
        num = random.randrange(1, TOP)
    else:
        num = random.randrange(TOP, len(books))

    return books[num-1]


def get_similar_books(ASIN):
    '''
    Get similar Amazon products by ASIN

    :prarm ASIN: Amazon product ID
    '''

    api = API(AWS_KEY, SECRET_KEY, 'us', ASSOCIATE_TAG)
    params = {
        'ResponseGroup' : 'Large',
        'IdType' : 'ASIN'
        }
    for root in api.similarity_lookup(str(ASIN), **params):

        try:
            current_page = root.Items.Request.ItemSearchRequest.ItemPage.pyval
        except AttributeError:
            current_page = 1

        #print 'page %d of %d' % (current_page, total_pages)


        nspace = root.nsmap.get(None, '')
        books = root.xpath('//aws:Items/aws:Item', namespaces={'aws' : nspace})
        similar_items = []
        i = 0
        for book in books:
            if (i==4):
                return similar_items

            similar_items.append(book)

            i = i + 1

def genie_year(age):
    '''
    Convert a publication age to before/after year

    :param age: -1 for all, N years old, if N > 20 get all beyond that
    '''
    year = 2013
    before = False
    if (age < 0):
        year = year
        before = True
    elif (age > 20):
        year = year - 20
        before = True
    else:
        year = year - age - 1

    return(year, before)


def prepopulate_cache():
    '''
    Prepopulate the cache with all the book set combonations
    '''
    for genre_item in Genres:
        try:
            genre = genre_item['value'];
        except:
            genre = genre_item['name'];

        for age_item in BookAges:
            (year, before) = genie_year(age_item['value'])

            genre = genre.replace('&amp;', ' ')
            genre = genre.replace('&', ' ')
            genre = genre.replace(',', ' ')

            power = power_string(genre, year, before)

            books = get_book_set(power)
            print "Power: %s ; Results: %d"%(power,len(books))
            cache.set(base64.b64encode(power),pickle.dumps(books), CACHE_LIFE)


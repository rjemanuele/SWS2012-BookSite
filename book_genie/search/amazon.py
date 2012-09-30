#!/usr/local/bin/python

import sys
import random
import pprint


from amazonproduct import NoExactMatchesFound
from amazonproduct import API

AWS_KEY = 'AKIAJ7B6DSAVWVFPC7RQ'
SECRET_KEY = '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'
ASSOCIATE_TAG = 'wwwdarktoneco-20'
TOP_TEN = 10
RESULT_LIMIT = 89

reload(sys)
sys.setdefaultencoding("utf-8")

def get_book(genre, popularity, pub_era, before):

    api = API(AWS_KEY, SECRET_KEY, 'us', ASSOCIATE_TAG)
    genre = genre.replace('&amp;', ' ')
    genre = genre.replace(',', ' ')

    if (before):
        param = 'before'
    else:
        param = 'after'
    #print param
    randSet = 1
    found = 0

    for root in api.item_search('Books', ResponseGroup='Large,EditorialReview', Power='pubdate:'+param+' '+str(pub_era)+' and binding: not kindle and subject:'+ genre, Sort = "salesrank"):


        total_results = root.Items.TotalResults.pyval
        total_pages = root.Items.TotalPages.pyval

        if (total_results < RESULT_LIMIT):
            upper_bound = total_results
        else:
            upper_bound = RESULT_LIMIT

        if(total_results < TOP_TEN):
            top_results = total_results
        else:
            top_results = TOP_TEN

        #print upper_bound
        #print top_results
        if (randSet):
            if (popularity < 0):
                num = random.randrange(0, upper_bound)
            elif (popularity):
                num = random.randrange(0, top_results)
            else:
                num = random.randrange(top_results, upper_bound)
            print num
            pageNum = num/10 + 1 #starts on page one so if we are under ten this number will be zero
            exact = num%10
            randSet = 0
            print pageNum
            print exact

        try:
            current_page = root.Items.Request.ItemSearchRequest.ItemPage.pyval
        except AttributeError:
            current_page = 1

        #print 'page %d of %d' % (current_page, total_pages)


        nspace = root.nsmap.get(None, '')
        books = root.xpath('//aws:Items/aws:Item', namespaces={'aws' : nspace})
        if (current_page == pageNum):
            i = 0
            for book in books:

                if (i == exact):
                    #output = book.ASIN,
                    #if hasattr(book.ItemAttributes, 'Author'):
                    #	output = output + book.ItemAttributes.Author + ':'
                    #	output = output + book.ItemAttributes.Title
                    #if hasattr(book.ItemAttributes, 'ListPrice'):
                    #	output = output + unicode(book.ItemAttributes.ListPrice.FormattedPrice)
                    #elif hasattr(book.OfferSummary, 'LowestUsedPrice'):
                    #	output = output + u'(used from %s)' % book.OfferSummary.LowestUsedPrice.FormattedPrice
                    return book

                i = i + 1

def get_similar_books(ASIN):

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

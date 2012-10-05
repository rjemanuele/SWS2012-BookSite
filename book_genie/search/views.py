from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random
import amazon
from amazonproduct.errors import NoSimilarityForASIN


class WheelForm(forms.Form):
    genre_field = forms.CharField(required = False)
    popularity_field = forms.IntegerField(required = False, initial = -1)
    age_field = forms.IntegerField(required = False, initial = -1)
    genre_text_field = forms.CharField(required = False)
    popularity_text_field = forms.CharField(required = False)
    age_text_field = forms.CharField(required = False)

def AWSFetchContent(genre, popularity, age):
    (year, before) = amazon.genie_year(age)

    try:
        book = amazon.get_book(genre, popularity, year, before)
        try:
            similar = amazon.get_similar_books(book.ASIN)
        except NoSimilarityForASIN:
            similar = []
            pass
        return Context({
                'Book' : book,
                'Similar' : similar,
                'Tag' : amazon.ASSOCIATE_TAG,
                })
    except Exception as inst:
        return Context({
                'Exception' : str(type(inst)),
                'Args' : str(inst),
                })


def index(request):

    result={}

    if request.method == 'POST': # If the form has been submitted...
        form = WheelForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            print "Yes, VALID data: { %s } { %d } { %d }"%(form.cleaned_data['genre_field'],form.cleaned_data['popularity_field'],form.cleaned_data['age_field'])
            result = AWSFetchContent(form.cleaned_data['genre_field'],form.cleaned_data['popularity_field'],form.cleaned_data['age_field'])

    else:
        form = WheelForm() # An unbound form

    result.update({
            'Genres': amazon.Genres,
            'BookAges': amazon.BookAges,
            'Popularities': amazon.Popularities,
            'form': form,
            })
    return render(request, 'index.html', result)




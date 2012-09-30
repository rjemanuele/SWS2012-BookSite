from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random
import amazon
from amazonproduct.errors import NoSimilarityForASIN

class WheelForm(forms.Form):
    genre_field = forms.CharField()
    popularity_field = forms.IntegerField()
    age_field = forms.IntegerField()
    genre_text_field = forms.CharField()
    popularity_text_field = forms.CharField()
    age_text_field = forms.CharField()

def AWSFetch1of50(genre, popularity, age):
    year = 2012
    before = False
    if (age == -1):
        year = year - 19
        before = True
    else:
        year = year - age - 1
        
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

    if request.method == 'POST': # If the form has been submitted...
        form = WheelForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            print "Yes, VALID data: { %s } { %d } { %d }"%(form.cleaned_data['genre_field'],form.cleaned_data['popularity_field'],form.cleaned_data['age_field'])
            content = AWSFetch1of50(form.cleaned_data['genre_field'],form.cleaned_data['popularity_field'],form.cleaned_data['age_field'])
            # Process the data in form.cleaned_data
            # ...
            content['form'] = form
            return render(request, 'index.html', content)

    else:
        form = WheelForm() # An unbound form

    return render(request, 'index.html', {
        'form': form,
    })
    

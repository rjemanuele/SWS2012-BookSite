from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
import random

from amazonproduct import *

AWS_KEY = 'AKIAJ7B6DSAVWVFPC7RQ'
SECRET_KEY = '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'
ASSOCIATE_TAG = 'wwwdarktoneco-20'



class WheelForm(forms.Form):
    genre_field = forms.CharField(required=True)
    popularity_field = forms.CharField(required=True)
    age_field = forms.CharField(required=True)

def AWSFetch1of50(genre, stars, timedivide):
    return Context({
            'ASIN':'389438948943',
            'Name':'Some Book',
            'Genre':'Histoy',
            'Description':'This is a book\'s description.'
            })


def index(request):

    if request.method == 'POST': # If the form has been submitted...
        form = WheelForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            content = AWSFetch1of50(form.cleaned_data['genre_field'],form.cleaned_data['popularity_field'],form.cleaned_data['age_field'])
            # Process the data in form.cleaned_data
            # ...
            return render(request, 'result.html', content)
    else:
        form = WheelForm() # An unbound form

    return render(request, 'index.html', {
        'form': form,
    })
    

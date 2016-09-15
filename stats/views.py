from django.shortcuts import render
from django.urls import reverse
from django.contrib.sites.models import Site
import requests

from stats.forms.words_form import WordsForm


def words(request):
    print('words - view')
    domain = Site.objects.get_current().domain
    url = 'http://' + domain + reverse('words-list')
    print(url)

    if not request.GET:
        print('not request.GET:')
        form = WordsForm(data=request.POST)
        response = requests.get(url)
        words_to_response = response.json()['results']
        return render(request, 'stats/words.html', {'words': words_to_response,
                                                    'form_element': form})
    else:
        print('request.GET:')

    form = WordsForm(data=request.GET)

    if form.is_valid():
        print('form is valid')
        response = requests.get(url)
    else:
        print('form is not valid')
        response = requests.get(url)

    words_to_response = response.json()['results']

    return render(request, 'stats/words.html', {'words': words_to_response,
                                                'form_element': form})

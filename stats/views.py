from django.shortcuts import render
from django.urls import reverse
from django.contrib.sites.models import Site
import requests

from stats.forms.words_form import WordsForm


def words(request):
    domain = Site.objects.get_current().domain
    url = 'http://' + domain + reverse('words-list')
    response = requests.get(url)

    words_to_response = response.json()['results']
    form = WordsForm()
    return render(request, 'stats/words.html', {'words': words_to_response,
                                                'form_element': form})

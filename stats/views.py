from django.shortcuts import render
from django.urls import reverse
from django.contrib.sites.models import Site
from django.test import Client
import requests

from stats.forms.words_form import WordsForm


def words(request):
    # print('words - view')
    # domain = Site.objects.get_current().domain
    # domain = request.META['HTTP_HOST']
    # print('domain')
    # print(domain)
    # print(request.META['HTTP_HOST'])
    # url = 'http://' + domain + reverse('words-list')
    url = reverse('words-list')
    print(url)

    if not request.GET:
        print('not request.GET:')
        form = WordsForm()
        # response = requests.get(url)
        c = Client()
        response = c.get(url)
        print(response)
        print(response.json())
        words_to_response = response.json()['results']
        print(words_to_response)
        return render(request, 'stats/words.html', {'words': words_to_response,
                                                    'form_element': form})
    else:
        print('request.GET:')

    form = WordsForm(data=request.GET)

    if form.is_valid():
        print('form is valid')
        params = {}
        if 'start_date' in request.GET:
            startdate = request.GET.get('start_date', None)
            if startdate:
                params['startdate'] = startdate
        if 'end_date' in request.GET:
            enddate = request.GET.get('end_date', None)
            if enddate:
                params['enddate'] = enddate
        print(params)
        response = requests.get(url, params=params)
    else:
        print('form is not valid')
        response = requests.get(url)

    words_to_response = response.json()['results']

    return render(request, 'stats/words.html', {'words': words_to_response,
                                                'form_element': form})

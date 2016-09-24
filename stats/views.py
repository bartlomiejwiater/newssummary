from django.shortcuts import render
from django.urls import reverse
from django.test import Client

from stats.forms.words_form import WordsForm
from utils.build_url import build_url


def words(request):
    url = reverse('words-list')

    if request.GET:
        form = WordsForm(data=request.GET)

        if form.is_valid():
            params = {}
            for par in [('start_date', 'startdate'), ('end_date', 'enddate')]:
                p = request.GET.get(par[0], None)
                if p:
                    params[par[1]] = p

            url = build_url('words-list', get=params)
    else:
        form = WordsForm()

    response = Client().get(url)
    words_to_response = response.json()['results']

    return render(request, 'stats/words.html', {'words': words_to_response,
                                                'form_element': form})

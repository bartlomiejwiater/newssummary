from django.shortcuts import render
from django.urls import reverse
from django.test import Client

from stats.forms.words_form import WordsForm
from utils.build_url import build_url


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
    # c = Client()

    if not request.GET:
        # print('not request.GET:')
        # response = requests.get(url)
        response = Client().get(url)
        # print(response)
        # print(response.json())
        words_to_response = response.json()['results']
        # print(words_to_response)

        form = WordsForm()
        return render(request, 'stats/words.html', {'words': words_to_response,
                                                    'form_element': form})
    # else:
    #     print('request.GET:')

    form = WordsForm(data=request.GET)

    if form.is_valid():
        print('form is valid')
        params = {}
        # if 'start_date' in request.GET:
        #     startdate = request.GET.get('start_date', None)
        #     if startdate:
        #         params['startdate'] = startdate
        # if 'end_date' in request.GET:
        #     enddate = request.GET.get('end_date', None)
        #     if enddate:
        #         params['enddate'] = enddate

        for param in [('start_date', 'startdate'), ('end_date', 'enddate')]:
            p = request.GET.get(param[0], None)
            if p:
                params[param[1]] = p
        # params['get'] = params
        # print(params)
        url = build_url('words-list', get=params)
        # print(url)
        # response = requests.get(url, params=params)
        response = Client().get(url)
    else:
        # print('form is not valid')
        # c = Client()
        response = Client().get(url)
        # response = requests.get(url)

    words_to_response = response.json()['results']

    return render(request, 'stats/words.html', {'words': words_to_response,
                                                'form_element': form})

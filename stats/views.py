from django.shortcuts import render


def temp(request):
    print('sdasda')
    return render(request, 'stats/cloud.html', {'bla': 'sdadsdas sdasd'})

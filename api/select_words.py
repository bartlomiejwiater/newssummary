from django_select2.views import AutoResponseView
from django.http import JsonResponse
from core.models import Word
from django.db.models import Sum, F, Q


class SelectWords(AutoResponseView):

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        print('term: ' + term)

        if len(term) < 2:
            return JsonResponse({})

        words = Word.objects.extra(select={'length': 'Length(name)'})\
            .annotate(text=F('name')).values('id', 'text')\
            .filter(Q(name__istartswith=term) | Q(name__icontains=term))\
            .annotate(Sum('rate__weight')).order_by('length')

        print(words)
        data = {'results': list(words)}
        print(data)
        return JsonResponse(data)

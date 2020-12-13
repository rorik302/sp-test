import json

from django.core.exceptions import FieldError
from django.core.serializers import serialize
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import BonusCard


def bonus_cards_list_view(request):
    '''
        Если в запросе есть query параметры, то выполняется поиск.
        Если query параметров нет, то возвращается список всех карт
    '''

    if len(request.GET):
        queryset = filter_by_query_params(request.GET)
    else:
        queryset = BonusCard.objects.all()
    data = serialize('json', queryset)
    return HttpResponse(data, content_type='application/json')


def filter_by_query_params(query_params):
    filter_by = {}
    for field, value in query_params.items():
        filter_by.update({'{}__iexact'.format(field): value})
    try:
        return BonusCard.objects.filter(**filter_by)
    except FieldError:
        return []


def parse_data(data):
    data['expired_at'] = parse_date(data['expired_at'])
    return data


@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    '''Добавление карты'''

    data = parse_data(json.loads(request.body.decode('utf-8')))
    try:
        card = BonusCard.objects.create(**data)
        return HttpResponse(serialize('json', [card]), content_type='application/json', status=201)
    except IntegrityError as e:
        return HttpResponse(status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete(request, pk):
    '''Удаление карты'''

    try:
        card = BonusCard.objects.get(pk=pk)
    except BonusCard.DoesNotExist:
        return HttpResponse(status=404)
    card.delete()
    return HttpResponse(status=200)

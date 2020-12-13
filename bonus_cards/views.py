import json

from django.core.exceptions import FieldError, ValidationError
from django.core.serializers import serialize
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import BonusCard


def list_view(request):
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


@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    '''Добавление карты'''

    data = parse_data(json.loads(request.body.decode('utf-8')))
    card = BonusCard(**data)
    if is_valid(card):
        try:
            card.save()
            return HttpResponse(serialize('json', [card]), content_type='application/json', status=201)
        except IntegrityError as e:
            return HttpResponse(status=400)
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


def filter_by_query_params(query_params):
    '''
        Фильтрация на основании параметров запроса.
        Если запрос валидный, то фильтрует список карт и возвращает. Если невалидный, то возвращает пустой список.
    '''

    filter_by = {}
    for field, value in query_params.items():
        filter_by.update({'{}__iexact'.format(field): value})
    try:
        return BonusCard.objects.filter(**filter_by)
    except FieldError:
        return []


def parse_data(data):
    '''Преобразование входящих данных'''

    data['expired_at'] = parse_date(data['expired_at'])
    return data


def is_valid(card):
    '''Валидация данных'''
    try:
        card.clean_fields()
    except ValidationError:
        return False
    return not BonusCard.objects.filter(serial=card.serial, number=card.number).exists()

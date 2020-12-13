import json

from django.core.serializers import serialize
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import BonusCard


def bonus_cards_list_view(request):
    '''Список карт'''
    data = serialize('json', BonusCard.objects.all())
    return HttpResponse(data, content_type='application/json')


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

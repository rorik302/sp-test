import json

from django.core import serializers
from django.http import HttpResponse

from .models import BonusCard


def bonus_cards_list_view(request):
    cards = serializers.serialize('json', BonusCard.objects.all())
    return HttpResponse(cards, content_type='application/json')

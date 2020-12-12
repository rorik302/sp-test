from django.conf.urls import patterns, url


urlpatterns = patterns('bonus_cards.views',
    url(r'^$', 'bonus_cards_list_view')
)

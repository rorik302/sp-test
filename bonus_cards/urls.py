from django.conf.urls import patterns, url


urlpatterns = patterns('bonus_cards.views',
    url(r'^$', 'list_view'),
    url(r'^create/$', 'create'),
    url(r'^(?P<pk>[0-9]+)/delete/$', 'delete')
)

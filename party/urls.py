from django.conf.urls import patterns, url
from party.views import PartyView, PartyDetailView, PartyAddView, PartyRemoveView
urlpatterns = patterns('',
                       url(r'^$', PartyView.as_view(), name='index'),
                       url(r'^(?P<party_id>\d+)/$', PartyDetailView.as_view(), name='party_detail'),
                       url(r'^add/$', PartyAddView.as_view(), name='party_add' ),
                       url(r'^add/successful/$', PartyView.as_view(), name='add_name_successful'),
                       url(r'^remove/(?P<party_id>\d+)/$', PartyRemoveView.as_view(), name="remove_party"),
                )
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.home),
    url(r'^add$', views.add),
    url(r'^logout$', views.logout),
    url(r'^get_trip/(?P<id>\d$)', views.get_trip),
    url(r'^join_trip/(?P<id>\d$)', views.join_trip),



]

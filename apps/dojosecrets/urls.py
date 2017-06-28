from django.conf.urls import url, include
# from django.contrib import admin
from . import views
urlpatterns = [
    url( r'^$', views.index ),

    url( r'^pokes$', views.pokes ),
    url( r'^poke/(?P<id>\d+)$', views.poke ),

    url( r'^login$', views.login, name="login" ),
    url( r'^reg$', views.reg, name="reg" ),

    url( r'^logout$', views.logout, name="logout" ),

    url( r'^deluser/(?P<id>\d+)$', views.deluser, name="deluser" ),

]

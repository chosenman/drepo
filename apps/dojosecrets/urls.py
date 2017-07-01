from django.conf.urls import url, include
# from django.contrib import admin
from . import views
urlpatterns = [
    url( r'^$', views.index ),

    url( r'^appts$', views.appts ),
    url( r'^add_appt$', views.add_appt ),

    url( r'^appt/(?P<id>\d+)$', views.appt ),
    url( r'^edit_appt$', views.edit_appt ),

    url( r'^login$', views.login, name="login" ),
    url( r'^reg$', views.reg, name="reg" ),

    url( r'^logout$', views.logout, name="logout" ),

    url( r'^deluser/(?P<id>\d+)$', views.deluser, name="deluser" ),
    url( r'^delapptmt/(?P<id>\d+)$', views.delapptmt, name="delapptmt" ),

]

from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^new_user/$', views.new_user, name='new-user'),
    url(r'^edit_info/(?P<userid>[0-9]+)$', views.edit_info, name='edit-info'),
    url(r'^state/(?P<userid>[0-9]+)$', views.state, name='state'),
    url(r'^password/(?P<userid>[0-9]+)$', views.password, name='password'),
    url(r'^profil/(?P<userid>[0-9]+)$', views.profil, name='profil'),
    url(r'^adherer/(?P<userid>[0-9]+)$', views.adherer, name='adherer'),
    url(r'^mon_profil/$', views.mon_profil, name='profile'),
    url(r'^add_listright/$', views.add_listright, name='add-listright'),
    url(r'^edit_listright/(?P<listrightid>[0-9]+)$', views.edit_listright, name='edit-listright'),
    url(r'^del_listright/$', views.del_listright, name='del-listright'),
    url(r'^index_listright/$', views.index_listright, name='index-listright'),
    url(r'^add_clef/$', views.add_clef, name='add-clef'),
    url(r'^edit_clef/(?P<clefid>[0-9]+)$', views.edit_clef, name='edit-clef'),
    url(r'^del_clef/(?P<clefid>[0-9]+)$', views.del_clef, name='del-clef'),
    url(r'^index_clef/$', views.index_clef, name='index-clef'),
    url(r'^history/(?P<object>clef)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^add_adhesion/$', views.add_adhesion, name='add-adhesion'),
    url(r'^edit_adhesion/(?P<adhesionid>[0-9]+)$', views.edit_adhesion, name='edit-adhesion'),
    url(r'^del_adhesion/(?P<adhesionid>[0-9]+)$', views.del_adhesion, name='del-adhesion'),
    url(r'^index_adhesion/$', views.index_adhesion, name='index-adhesion'),
    url(r'^history/(?P<object>adhesion)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^add_right/(?P<userid>[0-9]+)$', views.add_right, name='add-right'),
    url(r'^del_right/$', views.del_right, name='del-right'),
    url(r'^process/(?P<token>[a-z0-9]{32})/$', views.process, name='process'),
    url(r'^reset_password/$', views.reset_password, name='reset-password'),
    url(r'^history/(?P<object>user)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^history/(?P<object>listright)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^$', views.index, name='index'),
    url(r'^index_ajour/$', views.index_ajour, name='index-ajour'),
]

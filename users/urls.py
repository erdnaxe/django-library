from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^new_user/$', views.new_user, name='new-user'),
    url(r'^edit_info/(?P<userid>[0-9]+)$', views.edit_info, name='edit-info'),
    url(r'^state/(?P<userid>[0-9]+)$', views.state, name='state'),
    url(r'^profile/(?P<userid>[0-9]+)$', views.profile, name='profil'),
    url(r'^adherer/(?P<userid>[0-9]+)$', views.adherer, name='adherer'),
    url(r'^mon_profil/$', views.mon_profil, name='profile'),
    url(r'^add_clef/$', views.KeyCreate.as_view(), name='add-clef'),
    url(r'^edit_clef/(?P<clefid>[0-9]+)$', views.KeyUpdate.as_view(), name='edit-clef'),
    url(r'^del_clef/(?P<clefid>[0-9]+)$', views.del_clef, name='del-clef'),
    url(r'^index_clef/$', views.index_clef, name='index-clef'),
    url(r'^add_adhesion/$', views.MembershipCreate.as_view(), name='add-adhesion'),
    url(r'^edit_adhesion/(?P<adhesionid>[0-9]+)$', views.MembershipUpdate.as_view(), name='edit-adhesion'),
    url(r'^del_adhesion/(?P<adhesionid>[0-9]+)$', views.del_adhesion, name='del-adhesion'),
    url(r'^index_adhesion/$', views.index_adhesion, name='index-adhesion'),
    url(r'^$', views.index, name='index'),
    url(r'^index_ajour/$', views.index_ajour, name='index-ajour'),
]

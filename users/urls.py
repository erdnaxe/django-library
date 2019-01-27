from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('users/new/', views.new_user, name='new-user'),
    path('edit_info/<int:userid>', views.edit_info, name='edit-info'),
    path('state/<int:userid>', views.state, name='state'),
    path('profile/<int:userid>', views.profile, name='profil'),
    path('adherer/<int:userid>', views.adherer, name='adherer'),
    path('profile/', views.mon_profil, name='profile'),
    path('', views.index, name='index'),
    path('index_ajour/', views.index_ajour, name='index-ajour'),

    # Keys
    path('keys/', views.index_clef, name='index-clef'),
    path('keys/add/', views.KeyCreate.as_view(), name='add-clef'),
    path('keys/<int:clefid>/edit/', views.KeyUpdate.as_view(),
         name='edit-clef'),
    path('keys/<int:clefid>/del/', views.del_clef, name='del-clef'),

    # Membership
    path('membership/', views.index_adhesion, name='index-adhesion'),
    path('membership/add/', views.MembershipCreate.as_view(),
         name='add-adhesion'),
    path('membership/<int:adhesionid>/edit/',
         views.MembershipUpdate.as_view(), name='edit-adhesion'),
    path('membership/<int:adhesionid>/del/', views.del_adhesion,
         name='del-adhesion'),
]

from django.urls import path

from . import views

app_name = 'media'
urlpatterns = [
    path('auteurs/', views.IndexAuthors.as_view(), name='index-auteurs'),
    path('auteurs/add/', views.add_auteur, name='add-auteur'),
    path('auteurs/<int:pk>/edit/', views.edit_auteur, name='edit-auteur'),
    path('auteurs/<int:pk>/del/', views.del_auteur, name='del-auteur'),
    path('auteurs/<int:pk>/history/', views.history,
         {'object': 'auteur'}, name='history'),
    path('jeux/', views.IndexGames.as_view(), name='index-jeux'),
    path('jeux/add/', views.add_jeu, name='add-jeu'),
    path('jeux/<int:pk>/edit/', views.edit_jeu, name='edit-jeu'),
    path('jeux/<int:pk>/del/', views.del_jeu, name='del-jeu'),
    path('jeux/<int:pk>/history/', views.history,
         {'object': 'jeu'}, name='history'),
    path('media/', views.IndexMedia.as_view(), name='index-medias'),
    path('media/add/', views.add_media, name='add-media'),
    path('media/<int:pk>/edit/', views.edit_media, name='edit-media'),
    path('media/<int:pk>/del/', views.del_media, name='del-media'),
    path('media/<int:pk>/history/', views.history,
         {'object': 'media'}, name='history'),
    path('emprunts/', views.index, name='index'),
    path('emprunts/add/<int:userid>', views.add_emprunt, name='add-emprunt'),
    path('emprunts/<int:pk>/retour/', views.retour_emprunt,
         name='retour-emprunt'),
    path('emprunts/<int:pk>/edit/', views.edit_emprunt, name='edit-emprunt'),
    path('emprunts/<int:pk>/del/', views.del_emprunt, name='del-emprunt'),
    path('emprunts/<int:pk>/history/', views.history,
         {'object': 'emprunt'}, name='history'),
    path('', views.index, name='index'),
]

from django.urls import path

from . import views

app_name = 'media'
urlpatterns = [
    path('auteurs/', views.index_auteurs, name='index-auteurs'),
    path('auteurs/add/', views.add_auteur, name='add-auteur'),
    path('auteurs/<int:auteurid>/edit/', views.edit_auteur, name='edit-auteur'),
    path('auteurs/<int:auteurid>/del/', views.del_auteur, name='del-auteur'),
    path('auteurs/<int:id>/history/', views.history,
         {'object': 'auteur'}, name='history'),
    path('jeux/', views.index_jeux, name='index-jeux'),
    path('jeux/add/', views.add_jeu, name='add-jeu'),
    path('jeux/<int:jeuid>/edit/', views.edit_jeu, name='edit-jeu'),
    path('jeux/<int:jeuid>/del/', views.del_jeu, name='del-jeu'),
    path('jeux/<int:id>/history/', views.history,
         {'object': 'jeu'}, name='history'),
    path('media/', views.index_medias, name='index-medias'),
    path('media/add/', views.add_media, name='add-media'),
    path('media/<int:mediaid>/edit/', views.edit_media, name='edit-media'),
    path('media/<int:mediaid>/del/', views.del_media, name='del-media'),
    path('media/<int:id>/history/', views.history,
         {'object': 'media'}, name='history'),
    path('emprunts/', views.index, name='index'),
    path('emprunts/add/<int:userid>', views.add_emprunt, name='add-emprunt'),
    path('emprunts/<int:empruntid>/retour/', views.retour_emprunt,
         name='retour-emprunt'),
    path('emprunts/<int:empruntid>/edit/', views.edit_emprunt,
         name='edit-emprunt'),
    path('emprunts/<int:empruntid>/del/', views.del_emprunt,
         name='del-emprunt'),
    path('emprunts/<int:id>/history/', views.history,
         {'object': 'emprunt'}, name='history'),
    path('', views.index, name='index'),
]

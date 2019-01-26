from django.urls import path

from . import views

app_name = 'media'
urlpatterns = [
    path('auteurs/', views.AuthorsIndex.as_view(), name='index-auteurs'),
    path('auteurs/add/', views.AuthorsCreate.as_view(), name='add-auteur'),
    path('auteurs/<int:pk>/edit/', views.AuthorsUpdate.as_view(),
         name='edit-auteur'),
    path('auteurs/<int:pk>/del/', views.AuthorsDelete.as_view(),
         name='del-auteur'),
    path('auteurs/<int:pk>/history/', views.history,
         {'object': 'auteur'}, name='history'),
    path('jeux/', views.GamesIndex.as_view(), name='index-jeux'),
    path('jeux/add/', views.GamesCreate.as_view(), name='add-jeu'),
    path('jeux/<int:pk>/edit/', views.GamesUpdate.as_view(), name='edit-jeu'),
    path('jeux/<int:pk>/del/', views.GamesDelete.as_view(), name='del-jeu'),
    path('jeux/<int:pk>/history/', views.history,
         {'object': 'jeu'}, name='history'),
    path('media/', views.MediaIndex.as_view(), name='index-medias'),
    path('media/add/', views.MediaCreate.as_view(), name='add-media'),
    path('media/<int:pk>/edit/', views.MediaUpdate.as_view(),
         name='edit-media'),
    path('media/<int:pk>/del/', views.MediaDelete.as_view(), name='del-media'),
    path('media/<int:pk>/history/', views.history,
         {'object': 'media'}, name='history'),
    path('emprunts/', views.index, name='index'),
    path('emprunts/add/<int:userid>', views.add_emprunt, name='add-emprunt'),
    path('emprunts/<int:pk>/retour/', views.retour_emprunt,
         name='retour-emprunt'),
    path('emprunts/<int:pk>/edit/', views.edit_emprunt, name='edit-emprunt'),
    path('emprunts/<int:pk>/del/', views.BorrowedMediaDelete.as_view(),
         name='del-emprunt'),
    path('emprunts/<int:pk>/history/', views.history,
         {'object': 'emprunt'}, name='history'),
    path('', views.index, name='index'),
]

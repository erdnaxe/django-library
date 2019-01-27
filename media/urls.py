from django.urls import path

from . import views

app_name = 'media'
urlpatterns = [
    # Authors
    path('authors/', views.AuthorsIndex.as_view(), name='index-auteurs'),
    path('authors/add/', views.AuthorsCreate.as_view(), name='add-auteur'),
    path('authors/<int:pk>/edit/', views.AuthorsUpdate.as_view(),
         name='edit-auteur'),
    path('authors/<int:pk>/del/', views.AuthorsDelete.as_view(),
         name='del-auteur'),
    path('authors/<int:pk>/history/', views.history,
         {'object': 'auteur'}, name='history'),

    # Games
    path('games/', views.GamesIndex.as_view(), name='index-jeux'),
    path('games/add/', views.GamesCreate.as_view(), name='add-jeu'),
    path('games/<int:pk>/edit/', views.GamesUpdate.as_view(), name='edit-jeu'),
    path('games/<int:pk>/del/', views.GamesDelete.as_view(), name='del-jeu'),
    path('games/<int:pk>/history/', views.history,
         {'object': 'jeu'}, name='history'),

    # Media
    path('media/', views.MediaIndex.as_view(), name='index-medias'),
    path('media/add/', views.MediaCreate.as_view(), name='add-media'),
    path('media/<int:pk>/edit/', views.MediaUpdate.as_view(),
         name='edit-media'),
    path('media/<int:pk>/del/', views.MediaDelete.as_view(), name='del-media'),
    path('media/<int:pk>/history/', views.history,
         {'object': 'media'}, name='history'),

    # Borrowed media
    path('', views.MyBorrowedMediaIndex.as_view(),
         name='my-borrowed-media-index'),
    path('borrowed/', views.AllBorrowedMediaIndex.as_view(),
         name='all-borrowed-media-index'),
    path('borrowed/add/<int:userid>', views.add_emprunt, name='add-emprunt'),
    path('borrowed/<int:pk>/retour/', views.retour_emprunt,
         name='retour-emprunt'),
    path('borrowed/<int:pk>/edit/', views.edit_emprunt, name='edit-emprunt'),
    path('borrowed/<int:pk>/del/', views.BorrowedMediaDelete.as_view(),
         name='del-emprunt'),
    path('borrowed/<int:pk>/history/', views.history,
         {'object': 'emprunt'}, name='history'),
]

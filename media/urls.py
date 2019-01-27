from django.urls import path

from . import views

app_name = 'media'
urlpatterns = [
    # Authors
    path('authors/', views.AuthorsIndex.as_view(), name='author-index'),
    path('authors/add/', views.AuthorsCreate.as_view(), name='author-add'),
    path('authors/<int:i>/edit/', views.AuthorsUpdate.as_view(),
         name='author-edit'),
    path('authors/<int:i>/del/', views.AuthorsDelete.as_view(),
         name='author-del'),
    # path('authors/<int:i>/history/', views.history, name='author-history'),

    # Games
    path('games/', views.GamesIndex.as_view(), name='game-index'),
    path('games/add/', views.GamesCreate.as_view(), name='game-add'),
    path('games/<int:i>/edit/', views.GamesUpdate.as_view(), name='game-edit'),
    path('games/<int:i>/del/', views.GamesDelete.as_view(), name='game-del'),
    # path('games/<int:pk>/history/', views.history, name='game-history'),

    # Media
    path('media/', views.MediaIndex.as_view(), name='media-index'),
    path('media/add/', views.MediaCreate.as_view(), name='media-add'),
    path('media/<int:i>/edit/', views.MediaUpdate.as_view(), name='media-edit'),
    path('media/<int:i>/del/', views.MediaDelete.as_view(), name='media-del'),
    # path('media/<int:pk>/history/', views.history, name='media-history'),

    # Borrowed media
    path('', views.MyBorrowedMediaIndex.as_view(), name='my-borrowed-index'),
    path('borrowed/', views.AllBorrowedMediaIndex.as_view(),
         name='borrowed-index'),
    path('borrowed/add/<int:userid>', views.add_emprunt, name='borrowed-add'),
    path('borrowed/<int:i>/retour/', views.retour_emprunt,
         name='retour-emprunt'),
    path('borrowed/<int:i>/edit/', views.edit_emprunt, name='borrowed-edit'),
    path('borrowed/<int:i>/del/', views.BorrowedMediaDelete.as_view(),
         name='borrowed-del'),
    # path('borrowed/<int:i>/history/', views.history, name='borrowed-history'),
]

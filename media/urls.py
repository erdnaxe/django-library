from django.urls import path

from . import views

app_name = 'media'
urlpatterns = [
    # Authors
    path('authors/', views.AuthorsIndex.as_view(), name='author-index'),
    # path('authors/<int:i>/history/', views.history, name='author-history'),

    # Games
    path('games/', views.GamesIndex.as_view(), name='game-index'),
    # path('games/<int:pk>/history/', views.history, name='game-history'),

    # Media
    path('media/', views.MediaIndex.as_view(), name='media-index'),
    # path('media/<int:pk>/history/', views.history, name='media-history'),

    # Borrowed media
    path('', views.MyBorrowedMediaIndex.as_view(),
         name='my-borrowed-index'),
    path('borrowed/add/<int:user_id>', views.add_emprunt,
         name='borrowed-add'),
    path('borrowed/<int:i>/back/', views.retour_emprunt,
         name='borrowed-back'),
    path('borrowed/<int:i>/edit/', views.edit_emprunt,
         name='borrowed-edit'),
    # path('borrowed/<int:i>/history/', views.history, name='borrowed-history'),
]

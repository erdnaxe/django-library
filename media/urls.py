from django.urls import path

from . import views

app_name = 'media'
urlpatterns = [
    path('authors/', views.AuthorsIndex.as_view(), name='author-index'),
    path('games/', views.GamesIndex.as_view(), name='game-index'),
    path('media/', views.MediaIndex.as_view(), name='media-index'),
    path('', views.MyBorrowedMediaIndex.as_view(), name='my-borrowed-index'),

    # path('borrowed/add/<int:user_id>', views.add_emprunt,
    #      name='borrowed-add'),
    # path('borrowed/<int:i>/back/', views.retour_emprunt,
    #      name='borrowed-back'),
    # path('borrowed/<int:i>/edit/', views.edit_emprunt,
    #      name='borrowed-edit'),
    # path('borrowed/<int:i>/history/', views.history, name='borrowed-history'),
]

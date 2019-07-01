from haystack import indexes

from .models import Author, Media, Game


class AuthorsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Author


class MediaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    title = indexes.CharField(model_attr='title')
    side_title = indexes.CharField(model_attr='side_title')

    def get_model(self):
        return Media


class GamesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')
    comment = indexes.CharField(model_attr='comment')

    def get_model(self):
        return Game

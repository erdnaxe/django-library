from haystack import indexes

from .models import Media


class MediaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    cote = indexes.CharField(model_attr='cote')

    # auteur = indexes.ManyToManyField(model_attr='auteur')

    def get_model(self):
        return Media

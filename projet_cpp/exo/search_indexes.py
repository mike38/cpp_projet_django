import datetime
from haystack import indexes
from exo.models import Chapitre, Exercice, Fichier, Utilisation


class ChapitreIndex(indexes.SearchIndex, indexes.Indexable):
    nom = indexes.CharField(document=True, use_template=True)
    matiere = indexes.CharField(document=True, use_template=True)
    auteur = indexes.CharField(model_attr='user')
    content_auto = indexes.EdgeNgramField(model_attr='nom')
    content_auto = indexes.EdgeNgramField(model_attr='matiere')


    def get_model(self):
        return Chapitre

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        #filter(pub_date__lte=datetime.datetime.now())
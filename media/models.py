from django.db import models

class Auteur(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Media(models.Model):
    titre = models.CharField(max_length=255)
    cote = models.CharField(max_length=31)
    auteur = models.ForeignKey('Auteur', on_delete=models.PROTECT) 
#    type = TODO

    def __str__(self):
        return str(self.titre) + ' - ' + str(self.auteur)

class Emprunt(models.Model):
    media = models.ForeignKey('Media', on_delete=models.PROTECT) 
    user = models.ForeignKey('users.User', on_delete=models.PROTECT) 
    date_emprunt = models.DateTimeField(help_text='%d/%m/%y %H:%M:%S')
    date_rendu = models.DateTimeField(help_text='%d/%m/%y %H:%M:%S', blank=True, null=True)
    permanencier_emprunt = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='user_permanencier_emprunt')
    permanencier_rendu = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='user_permanencier_rendu', blank=True, null=True) 
 





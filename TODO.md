# Fonctionnalités à ajouter

Idée de PA : pouvoir avoir des commentaires par jeu pour discuter des règles.

Envoyer un mail lors de la création d'un utilisateur.

Lister les permanenciers pour les adhérents.

Être beau dans Google.

Un flag « jeu de la semaine » et une façon de noter le leaderaboard/ les achievements peut être sympa

Bouton pour revert une modif dans les logs. Et changer le nom de la première colonne.

```Python
@login_required
@permission_required('bureau')
def revert_action(request, revision_id):
    try:
        revision = Revision.objects.get(id=revision_id)
    except Revision.DoesNotExist:
        messages.error(request, u"Revision inexistante")
    if request.method == "POST":
        revision.revert()
        messages.success(request, "L'action a été supprimée")
        return redirect("/logs/")
    c = {'objet': revision, 'objet_name': revision.__class__.__name__}
    c.update(csrf(request))
    return render(request, 'logs/delete.html', c)
```

Ce qui serait super bien, ce serait la possibilité de laisser un avis sur un jeu/manga /BD
Avec peut être un système de « notes »
Ou d’étoiles


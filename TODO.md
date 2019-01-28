# Fonctionnalités à ajouter

Idée de PA : pouvoir avoir des commentaires par jeu pour discuter des règles.

Idée de Karnaj : avoir une API.

Page de création/modification d'utilisateurs avec le groupe de permission.

Envoyer un mail lors de la création d'un utilisateur.

Lister les permanenciers pour les adhérents.

Ajouter taille de la boite des jeux. Avec nombre de dimension puis calcul du volume.

Être beau dans Google.

Implémenter l'historique des objets selon :

```Python
def history(request, object, id):
    """ Affichage de l'historique : (acl, argument)
    user : self, userid"""
    if object == 'clef':
        try:
            object_instance = Clef.objects.get(pk=id)
        except Clef.DoesNotExist:
            messages.error(request, "Utilisateur inexistant")
            return redirect("/users/")
    elif not request.user.is_authenticated:
        messages.error(request, "Permission denied")
        return redirect("/users/")
    if object == 'user':
        try:
            object_instance = User.objects.get(pk=id)
        except User.DoesNotExist:
            messages.error(request, "Utilisateur inexistant")
            return redirect("/users/")
        if not request.user.has_perms(
                ('perm',)) and object_instance != request.user:
            messages.error(request,
                           "Vous ne pouvez pas afficher l'historique d'un autre user que vous sans droit admin")
            return redirect("/users/profil/" + str(request.user.id))
    elif object == 'clef':
        try:
            object_instance = Clef.objects.get(pk=id)
        except Clef.DoesNotExist:
            messages.error(request, "Utilisateur inexistant")
            return redirect("/users/")
    elif object == 'adhesion':
        try:
            object_instance = Adhesion.objects.get(pk=id)
        except Adhesion.DoesNotExist:
            messages.error(request, "Utilisateur inexistant")
            return redirect("/users/")
    else:
        messages.error(request, "Objet  inconnu")
        return redirect("/users/")
    reversions = Version.objects.get_for_object(object_instance)
    paginator = Paginator(reversions, PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        reversions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reversions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reversions = paginator.page(paginator.num_pages)
    return render(request, 'med/history.html',
                  {'reversions': reversions, 'object': object_instance})
```
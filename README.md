# Site de la Med

Le projet Med permet la gestion de la base de donnée de la médiathèque de l'ENS Paris-Saclay.
Elle permet de gérer les medias, bd, jeux, emprunts, ainsi que les adhérents de la med.

## Licence

Ce projet est sous la licence GNU public license v2.0.

Il a été forké par Gabriel Détraz il y a bien longtemps à partir de
[re2o](<https://gitlab.rezometz.org/rezo/re2o>).
Néanmoins depuis le code a été majoritairement réécrit dans une optique d'être maintenable à long terme.

# Développement

Le projet utilise Pipenv donc pour avoir un environnement fonctionnel avec les mêmes versions qu'en prod,
il suffit d'executer :

```bash
pipenv install
pipenv shell
```

Ensuite faut déployer les paquets Yarn et
suivre les procédures standards de Django :

```bash
yarn --prod
./manage.py migrate
./manage.py collectstatic
./manage.py runserver
``` 

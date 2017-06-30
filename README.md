# Portail captif

Gnu public license v2.0

## Avant propos 

Ce projet est forké à partir de re2o  (https://gitlab.rezometz.org/rezo/re2o).
Ce portail minimaliste permet aux utilisateurs de s'identifier. Leurs mac sont capturées, et injectée dans une ipset qui leur donne accès à internet.

#Installation

## Installation des dépendances

L'installation comporte 2 parties : le serveur web où se trouve le depot med ainsi que toutes ses dépendances, et le serveur bdd (mysql ou pgsql). Ces 2 serveurs peuvent en réalité être la même machine, ou séparés (recommandé en production).
Le serveur web sera nommé serveur A, le serveur bdd serveur B .

### Prérequis sur le serveur A

Voici la liste des dépendances à installer sur le serveur principal (A).

### Avec apt :

#### Sous debian 8
Paquets obligatoires:
 * python3-django (1.8, jessie-backports)
 * python3-dateutil (jessie-backports)
 * python3-django-reversion (stretch)
 * python3-pip (jessie)

Avec pip3 :
 * django-bootstrap3
 * django-macaddress

Paquet recommandés:
 * python3-django-extensions (jessie)

Moteur de db conseillé (mysql), postgresql fonctionne également.
Pour mysql, il faut installer : 
 * python3-mysqldb (jessie-backports)
 * mysql-client

Postgresql :
 * psycopg2

### Prérequis sur le serveur B

Sur le serveur B, installer mysql ou postgresql, dans la version jessie ou stretch.
 * mysql-server (jessie/stretch) ou postgresql (jessie-stretch)

### Installation sur le serveur principal A

Cloner le dépot med à partir du gitlab, par exemple dans /var/www/med.
Ensuite, il faut créer le fichier settings_local.py dans le sous dossier med, un settings_local.example.py est présent. Les options sont commentées, et des options par défaut existent.

En particulier, il est nécessaire de générer un login/mdp admin pour le ldap et un login/mdp pour l'utilisateur sql (cf ci-dessous), à mettre dans settings_local.py

### Installation du serveur mysql/postgresql sur B

Sur le serveur mysql ou postgresl, il est nécessaire de créer une base de donnée med, ainsi qu'un user med et un mot de passe associé. Ne pas oublier de faire écouter le serveur mysql ou postgresql avec les acl nécessaire pour que A puisse l'utiliser.

Voici les étapes à éxecuter pour mysql :
 * CREATE DATABASE med;
 * CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
 * GRANT ALL PRIVILEGES ON med.* TO 'newuser'@'localhost';
 * FLUSH PRIVILEGES;

Si les serveurs A et B ne sont pas la même machine, il est nécessaire de remplacer localhost par l'ip avec laquelle A contacte B dans les commandes du dessus.
Une fois ces commandes effectuées, ne pas oublier de vérifier que newuser et password sont présents dans settings_local.py

## Configuration initiale

Normalement à cette étape, le ldap et la bdd sql sont configurées correctement.

Il faut alors lancer dans le dépot med '''python3 manage.py migrate''' qui va structurer initialement la base de données.
Les migrations sont normalement comitées au fur et à mesure, néanmoins cette étape peut crasher, merci de reporter les bugs.

## Démarer le site web

Il faut utiliser un moteur pour servir le site web. Nginx ou apache2 sont recommandés.
Pour apache2 :
 * apt install apache2
 * apt install libapache2-mod-wsgi-py3 (pour le module wsgi)

med/wsgi.py permet de fonctionner avec apache2 en production

Pour nginx :
 * apt install nginx
 * apt install gunicorn3


## Configuration avancée

Une fois démaré, le site web devrait être accessible. 
Pour créer un premier user, faire '''python3 manage.py createsuperuser''' qui va alors créer un user admin.
Il est conseillé de créer alors les droits cableur, bureau, trésorier et infra, qui n'existent pas par défaut dans le menu adhérents.
Il est également conseillé de créer un user portant le nom de l'association/organisation, qui possedera l'ensemble des machines.

# Requète en base de donnée

Pour avoir un shell, il suffit de lancer '''python3 manage.py shell'''
Pour charger des objets, example avec User, faire : ''' from users.models import User'''
Pour charger les objets django, il suffit de faire User.objects.all() pour tous les users par exemple. 
Il est ensuite aisé de faire des requètes, par exemple User.objects.filter(pseudo='test')
Des exemples et la documentation complète sur les requètes django sont disponible sur le site officiel.

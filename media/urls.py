# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Goulven Kermarec
# Copyright © 2017  Augustin Lemesle
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from django.conf.urls import url

from . import views

app_name = 'media'
urlpatterns = [
    url(r'^add_auteur/$', views.add_auteur, name='add-auteur'),
    url(r'^edit_auteur/(?P<auteurid>[0-9]+)$', views.edit_auteur, name='edit-auteur'),
    url(r'^del_auteur/(?P<auteurid>[0-9]+)$', views.del_auteur, name='del-auteur'),
    url(r'^index_auteurs/$', views.index_auteurs, name='index-auteurs'),
    url(r'^history/(?P<object>auteur)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^add_jeu/$', views.add_jeu, name='add-jeu'),
    url(r'^edit_jeu/(?P<jeuid>[0-9]+)$', views.edit_jeu, name='edit-jeu'),
    url(r'^del_jeu/(?P<jeuid>[0-9]+)$', views.del_jeu, name='del-jeu'),
    url(r'^index_jeux/$', views.index_jeux, name='index-jeux'),
    url(r'^history/(?P<object>jeu)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^add_media/$', views.add_media, name='add-media'),
    url(r'^edit_media/(?P<mediaid>[0-9]+)$', views.edit_media, name='edit-media'),
    url(r'^del_media/(?P<mediaid>[0-9]+)$', views.del_media, name='del-media'),
    url(r'^index_medias/$', views.index_medias, name='index-medias'),
    url(r'^history/(?P<object>media)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^add_emprunt/(?P<userid>[0-9]+)$', views.add_emprunt, name='add-emprunt'),
    url(r'^retour_emprunt/(?P<empruntid>[0-9]+)$', views.retour_emprunt, name='retour-emprunt'),
    url(r'^edit_emprunt/(?P<empruntid>[0-9]+)$', views.edit_emprunt, name='edit-emprunt'),
    url(r'^del_emprunt/(?P<empruntid>[0-9]+)$', views.del_emprunt, name='del-emprunt'),
    url(r'^index_emprunts/$', views.index, name='index'),
    url(r'^history/(?P<object>emprunt)/(?P<id>[0-9]+)$', views.history, name='history'),
    url(r'^$', views.index, name='index'),
]

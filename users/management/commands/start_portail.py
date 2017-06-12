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
#
# Ce script est appellé avant le démarage du portail, il insère les bonnes règles
# dans l'iptables et active le routage

from django.core.management.base import BaseCommand, CommandError


from users.models import restore_iptables, create_ip_set, fill_ipset, apply
from portail_captif.settings import AUTORIZED_INTERFACES

class Command(BaseCommand):
    help = 'Mets en place iptables et le set ip au démarage'

    def handle(self, *args, **options):
        # Creation de l'ipset
        create_ip_set()
        # Remplissage avec les macs autorisées
        fill_ipset()
        # Restauration de l'iptables
        restore_iptables()
        # Activation du routage sur les bonnes if
        for interface in AUTORIZED_INTERFACES:
            apply(["sudo", "-n", "sysctl",  "net.ipv6.conf.%s.forwarding=1" % interface])
            apply(["sudo", "-n", "sysctl",  "net.ipv4.conf.%s.forwarding=1" % interface])




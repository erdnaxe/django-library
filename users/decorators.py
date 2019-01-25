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

# App de gestion des users pour med
# Goulven Kermarec, Gabriel Détraz, Lemesle Augustin
# Gplv2


import ipaddress

from django.shortcuts import redirect

from med.settings import AUTHORIZED_IP_RANGE, AUTHORIZED_IP6_RANGE


def user_is_in_campus(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            remote_ip = get_ip(request)
            if not ipaddress.ip_address(remote_ip) in ipaddress.ip_network(AUTHORIZED_IP_RANGE) and not ipaddress.ip_address(remote_ip) in ipaddress.ip_network(AUTHORIZED_IP6_RANGE):
                return redirect("/")
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def get_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip

##
# This file is part of the 'I Vote Goat' project.
#
# Copyright (C) 2014 Stefan Wendler <sw@kaltpost.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import pkgutil
import sys
import logging as log
import os


def load(dir_name):

    full_path = "%s/%s" % (os.path.dirname(__file__), dir_name)

    for importer, package_name, _ in pkgutil.iter_modules([full_path]):

        full_package_name = '%s.%s' % (dir_name, package_name)

        if full_package_name not in sys.modules:

            plugin = importer.find_module(package_name).load_module(full_package_name)

            try:
                plugin.EventHandler()
            except Exception as e:
                log.error("PLUGIN - %s" % e.__str__())
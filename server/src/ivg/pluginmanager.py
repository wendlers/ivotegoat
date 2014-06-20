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

import logging as log
import sys
import os


class PluginManager:

    def __init__(self, plugin_dirs):

        self.plugin_dirs = plugin_dirs
        self.plugins = {}

    def plugins_list(self):

        for path in self.plugin_dirs.split(os.pathsep):
            sys.path.append(path)
            for filename in os.listdir(path):
                name, ext = os.path.splitext(filename)
                if ext.endswith(".py"):
                    yield name

    def import_plugins(self, env):

        for plugin in self.plugins_list():
            log.info("Loading module: %s" % plugin)
            module = __import__(plugin, env)
            env[plugin] = module
            instance = module.Plugin()
            self.plugins[instance.name] = instance

    def get_plugin(self, name):

        try:
            return self.plugins[name]
        except Exception as e:
            log.warning("PLUGIN - %s" % e.__str__())

        return None

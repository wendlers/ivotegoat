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

APP = "ivgd"
VERSION = "0.0.1 alpha"

HTTP_HOST = '0.0.0.0'
HTTP_PORT = 8080
HTTP_DOC_ROOT = '/opt/ivotegoat/client/www'

DATA_BASE = '/opt/ivotegoat/server/db/ivotegote.db'

LOG_LEVEL = log.DEBUG
LOG_FILE = None

# default sysconfig - might be overwritten from DB values
sysconf = {
    "PLUGIN_DIRS": "../plugins",
    "POINTS_MAX": 4,
    "POINTS_OFFTIME": 60,
    "DECAY_AMOUNT": 1,
    "DECAY_INTERVAL": 60
}
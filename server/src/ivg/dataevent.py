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
import datapool as dp


class DataEvent:

    def __init__(self, name):

        self.name = name
        self.dp = dp.DataPool()
        self.dp.register_event_handler(self)

    def add_point(self, nickname, points_left):
        log.warning("Not implemented: add_point: %s (%d)" % (nickname, points_left))

    def del_point(self, nickname, points_left):
        log.warning("Not implemented: del_point: %s (%d)" % (nickname, points_left))

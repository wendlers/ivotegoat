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

import threading as thrd
import datapool as dp
import config as cfg
import time
import logging as log


class PointDecayThread(thrd.Thread):

    def __init__(self):
        thrd.Thread.__init__(self)

        self.daemon = True
        self.dp = dp.DataPool()

        log.info("Decay interval: %d (%d)" % (cfg.DECAY_INTERVAL, cfg.DECAY_AMOUNT))

    def run(self):

        while True:
            time.sleep(cfg.DECAY_INTERVAL)

            try:
                self.dp.decay_points(cfg.DECAY_AMOUNT)
            except Exception as e:
                log.error("Error while decaying points: %s" % e.__str__())
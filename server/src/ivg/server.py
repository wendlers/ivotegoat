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

import bottle as bot
import datapool as dp
import config as cfg
import pointdecay as pdec
import logging as log
import sqlite3 as sqlite
import optparse as par

from daemonize import Daemonize

class Server:

    def __init__(self):
        """


        :type self: object
        """

        try:

            log.basicConfig(level=cfg.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s', filename=cfg.LOG_FILE)
            log.info("%s: %s", cfg.APP, cfg.VERSION)

            log.debug("Setting up routing")
            self.setup_routing()

            log.debug("Creating data pool")
            self.dp = dp.DataPool()

            log.debug("Starting point decay thread")
            self.pdec = pdec.PointDecayThread()
            self.pdec.start()

            log.debug("Starting HTTP server")
            log.info("HTTP Server: %s:%s (%s)" % (cfg.HTTP_HOST, cfg.HTTP_PORT, cfg.HTTP_DOC_ROOT))
            bot.run(host=cfg.HTTP_HOST, port=cfg.HTTP_PORT, quiet=True)

        except Exception as e:
            log.error("ABORTING - %s" % e.__str__())
            exit(1)

    def setup_routing(self):
        """


        :type self: object
        :rtype : object
        """

        bot.route('/users', 'POST', self.handle_add_user)
        bot.route('/users', 'GET', self.handle_list_users)
        bot.route('/users/<nickname>', 'GET', self.handle_get_user)
        bot.route('/users/<nickname>', 'DELETE', self.handle_del_user)

        bot.route('/points', 'POST', self.handle_add_point)
        bot.route('/points/<nickname>', 'DELETE', self.handle_del_user_points)

        bot.route('/<subdir>/<filename:path>', 'GET', self.handle_static)
        bot.route('/', 'GET', self.handle_index)

    def handle_list_users(self):
        """


        :return:
        """

        bot.response.set_header('Content-Type', 'application/json')

        return self.dp.list_users(True)

    def handle_add_user(self):
        """

        :type name: object
        """

        nickname = bot.request.forms.get('nickname')
        fullname = bot.request.forms.get('fullname')

        if not nickname or len(nickname) == 0:
            log.error("Missing parameter: nickname")
            return bot.abort(code=400, text="Missing parameter: nickname")

        if not fullname or len(fullname) == 0:
            log.error("Missing parameter: fullname")
            return bot.abort(code=400, text="Missing parameter: fullname")

        try:
            self.dp.add_user(nickname, fullname)
        except sqlite.IntegrityError as e:
            log.error("SQL - %s" % e.__str__())
            return bot.abort(code=400, text=e.__str__())

        return bot.abort(code=201, text="Added user: %s" % nickname)

    def handle_get_user(self, nickname):
        """


        :return:
        """

        bot.response.set_header('Content-Type', 'application/json')

        return self.dp.get_user(nickname, True)

    def handle_del_user(self, nickname):
        """

        :param nickname:
        :return:
        """

        self.dp.del_user(nickname)

    def handle_add_point(self):

        nickname = bot.request.forms.get('nickname')
        weight = int(bot.request.forms.get('weight'))

        if not nickname or len(nickname) == 0:
            log.error("Missing parameter: nickname")
            return bot.abort(code=400, text="Missing parameter: nickname")

        if not weight:
            log.error("Missing parameter: weight")
            return bot.abort(code=400, text="Missing parameter: weight")

        try:
            num_points = self.dp.count_points(nickname)
            if num_points >= cfg.MAX_USER_POINTS:
                log.info("Maximum number of points reached: %s (%d)" % (nickname, num_points))
                return bot.abort(code=460, text="Maximum number of points reached: %s (%d)" %
                                                (nickname, num_points))

            offtime_points = self.dp.count_points_offtime(nickname, cfg.OFFTIME_USER_POINTS)
            if offtime_points > 0:
                log.info("User already got points within off time: %s (%d)" % (nickname, offtime_points))
                return bot.abort(461, "User already got points within off time: %s (%d)"
                                 % (nickname, offtime_points))

            self.dp.add_point(nickname, weight)
        except sqlite.IntegrityError as e:
            log.error("SQL - %s" % e.__str__())
            return bot.abort(code=400, text=e.__str__())

        return bot.abort(code=201, text="Added point to user: %s (%d)" % (nickname, weight))

    def handle_del_user_points(self, nickname):
        """


        :return:
        """

        self.dp.del_user_points(nickname)

    def handle_index(self):
        """

        :param filename:
        :return:
        """

        return bot.static_file("index.html", root=cfg.HTTP_DOC_ROOT)

    def handle_static(self, subdir, filename):
        """

        :param filename:
        :return:
        """

        path = subdir + "/" + filename

        return bot.static_file(path, root=cfg.HTTP_DOC_ROOT)


def server_main_daemon():

    log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='/tmp/ivgd.log')
    Server()


def server_main_foreground():

    log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    Server()


if __name__ == "__main__":

    usage = "usage: %prog [options]"

    parser = par.OptionParser(usage)
    parser.add_option("-d", "--daemonize", action="store_true",
                      help="run as daemon")
    parser.add_option("-p", "--pid",  dest="pid", default="ivgd.pid",
                      help="pid file when run as daemon")
    parser.add_option("-l", "--logfile",  dest="logfile", default=cfg.LOG_FILE,
                      help="log file")
    parser.add_option("-L", "--loglevel",  dest="loglevel", default="debug",
                      help="log level (debug|info|warning|error)")
    parser.add_option("-H", "--host",  dest="host", default=cfg.HTTP_HOST,
                      help="host name/ip to bind server to")
    parser.add_option("-P", "--port",  dest="port", default=cfg.HTTP_PORT,
                      help="port to bind server to")
    parser.add_option("-D", "--docroot",  dest="docroot", default=cfg.HTTP_DOC_ROOT,
                      help="document root of server")
    parser.add_option("-B", "--database",  dest="database", default=cfg.DATA_BASE,
                      help="location of database")
    parser.add_option("-I", "--decayinterval",  dest="decayinterval", default=cfg.DECAY_INTERVAL,
                      help="interval within to decay points")
    parser.add_option("-A", "--decayamount",  dest="decayamount", default=cfg.DECAY_AMOUNT,
                      help="amount (weight) to remove each decay interval")
    parser.add_option("-T", "--offtime",  dest="offtime", default=cfg.OFFTIME_USER_POINTS,
                      help="off time between each new user points")

    (options, args) = parser.parse_args()

    if options.loglevel == "debug":
        cfg.LOG_LEVEL = log.DEBUG
    elif options.loglevel == "info":
        cfg.LOG_LEVEL = log.INFO
    elif options.loglevel == "warning":
        cfg.LOG_LEVEL = log.WARNING
    elif options.loglevel == "error":
        cfg.LOG_LEVEL = log.ERROR
    else:
        print("Unkown log level: %s" % options.loglevel)
        exit(1)

    # overwrite defaults ...
    cfg.LOG_FILE = options.logfile
    cfg.HTTP_HOST = options.host
    cfg.HTTP_PORT = int(options.port)
    cfg.HTTP_DOC_ROOT = options.docroot
    cfg.DATA_BASE = options.database
    cfg.DECAY_INTERVAL = int(options.decayinterval)
    cfg.DECAY_AMOUNT = int(options.decayamount)
    cfg.OFFTIME_USER_POINTS = int(options.offtime)

    if options.daemonize:
        daemon = Daemonize(app="ivgd", pid=options.pid, action=Server)
        daemon.start()
    else:
        Server()

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

class Server:

    def __init__(self):
        """


        :type self: object
        :param host:
        :param port:
        """

        self.doc_root = cfg.HTTP_DOC_ROOT

        self.setup_routing()

        self.dp = dp.DataPool()

        self.pdec = pdec.PointDecayThread()
        self.pdec.start()

        bot.run(host=cfg.HTTP_HOST, port=cfg.HTTP_PORT, quiet=False)

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
            return bot.abort(code=400, text="Missing parameter: nickname")

        if not fullname or len(fullname) == 0:
            return bot.abort(code=400, text="Missing parameter: fullname")

        try:
            self.dp.add_user(nickname, fullname)
        except Exception as e:
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
            return bot.abort(code=400, text="Missing parameter: nickname")

        if not weight:
            return bot.abort(code=400, text="Missing parameter: weight")

        try:
            num_points = self.dp.count_points(nickname)
            if num_points >= cfg.MAX_USER_POINTS:
                return bot.abort(code=400, text="Maximum number of points reached: %s (%d)" %
                                                (nickname, num_points))
            else:
                self.dp.add_point(nickname, weight)
        except Exception as e:
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

        return bot.static_file("index.html", root=self.doc_root)

    def handle_static(self, subdir, filename):
        """

        :param filename:
        :return:
        """

        path = subdir + "/" + filename

        return bot.static_file(path, root=self.doc_root)


if __name__ == "__main__":

    log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    log.info("Server started")
    s = Server()

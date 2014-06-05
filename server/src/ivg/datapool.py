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

import sqlite3 as sqlite
import config as cfg
import logging as log

from singleton import Singleton


@Singleton
class DataPool:

    def __init__(self):
        """

        :type self: object
        """

        self.con = sqlite.connect(cfg.DATA_BASE, check_same_thread=False)
        
        self.setup_tables()

    def setup_tables(self):
        """



        :type self: object
        """
        with self.con:
            cur = self.con.cursor()

            # users table
            cur.execute("CREATE TABLE IF NOT EXISTS users(nickname TEXT, fullname TEXT)")
            cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS index_users_nickname ON users (nickname)")

            # user points table
            cur.execute("CREATE TABLE IF NOT EXISTS points(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "nickname TEXT, weight INT)")

    def list_users(self, with_points=False):

        users = {'users': []}

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT nickname, fullname FROM users")

            rows = cur.fetchall()

            for row in rows:
                if not with_points:
                    users['users'].append({'nickname': row[0], 'fullname': row[1]})
                else:
                    users['users'].append({'nickname': row[0], 'fullname': row[1],
                                           'points': self.list_user_points(row[0])["points"]})

        return users

    def get_user(self, nickname, with_points=False):

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT nickname, fullname FROM users WHERE nickname = '%s'" % nickname)

            row = cur.fetchone()

            if not with_points:
                user = {'user': {'nickname': row[0], 'fullname': row[1]}}
            else:
                user = {'user': {'nickname': row[0], 'fullname': row[1],
                                 'points': self.list_user_points(row[0])["points"]}}

        return user

    def add_user(self, nickname, fullname):
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO users (nickname, fullname) values ('%s', '%s')" % (nickname, fullname))

    def del_user(self, nickname):
        with self.con:
            cur = self.con.cursor()
            cur.execute("DELETE FROM users WHERE nickname = '%s'" % nickname)

        self.del_user_points(nickname)

    def add_point(self, nickname, weight):
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO points (nickname, weight) values ('%s', %d)" % (nickname, weight))

    def count_points(self, nickname):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM points WHERE nickname='%s'" % nickname)
            res = cur.fetchone()
            return res[0]

    def list_user_points(self, nickname):

        points = {'points': []}

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT weight FROM points WHERE nickname = '%s' ORDER BY weight ASC" % nickname)

            rows = cur.fetchall()

            for row in rows:
                points['points'].append(row[0])

        return points

    def del_user_points(self, nickname):

        with self.con:
            cur = self.con.cursor()
            cur.execute("DELETE FROM points WHERE nickname = '%s'" % nickname)

    def decay_user_points(self, nickname, decay):

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT weight FROM points WHERE id = (SELECT min(id) FROM points WHERE nickname = '%s')" %
                        nickname)

            row = cur.fetchone()

            if not row:
                return

            if row[0] - decay <= 0:
                cur.execute("DELETE FROM points WHERE id = (SELECT min(id) FROM points WHERE nickname = '%s')" % nickname)
                log.info("deleted point for user: %s" % nickname)
            else:
                cur.execute("UPDATE points SET weight = weight-%d WHERE "
                            "id = (SELECT min(id) FROM points  WHERE nickname = '%s')" % (decay, nickname))
                log.info("decayed point for user: %s (%d)" % (nickname, decay))

    def decay_points(self, decay):

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT nickname FROM users")

            rows = cur.fetchall()

            for row in rows:
                self.decay_user_points(row[0], decay)
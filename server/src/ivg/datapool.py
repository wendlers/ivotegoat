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
        self.event_handlers = []

        log.info("Data base: %s" % cfg.DATA_BASE)
        log.info("Point off-time: %d" % cfg.sysconf["POINTS_OFFTIME"])

    def register_event_handler(self, handler):

        log.info("Registered new handler: %s" % handler.name)
        self.event_handlers.append(handler)

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
                        "nickname TEXT, weight INT, created datetime)")

            # plugin config
            cur.execute("CREATE TABLE IF NOT EXISTS plugconf(plugin TEXT, key TEXT, value TEXT, type INT)")
            cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS index_plugconf_plugin_key ON plugconf (plugin, key)")

            # system config
            cur.execute("SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'sysconf'")
            row = cur.fetchone()

            if row:
                # read settings from table
                cur.execute("SELECT key, value, type FROM sysconf")
                rows = cur.fetchall()

                for row in rows:
                    key = row[0]
                    val = row[1]
                    typ = row[2]

                    try:
                        if typ == 1:
                            val = int(row[1])

                        log.debug("Overwriting key:value in sysconf: %s=%s (%d)" % (key, val, typ))
                        cfg.sysconf[key] = val

                    except Exception as e:
                        log.warning("SYSCONF - %s" & e.__str__())

            else:
                # write defaults to table
                cur.execute("CREATE TABLE sysconf(key TEXT, value TEXT, type INT)")
                cur.execute("CREATE UNIQUE INDEX index_sysconf_key ON sysconf (key)")

                for key in cfg.sysconf:

                    val = cfg.sysconf[key]
                    typ = 0

                    if isinstance(val, int):
                        typ = 1

                    log.debug("Adding default key:value to sysconf: %s=%s (%d)" % (key, val, typ))
                    cur.execute("INSERT INTO sysconf ('key', 'value', 'type') values ('%s', '%s', %d)" %
                                (key, val, typ))

    def list_sysconf(self):

        conf = {'sysconf': []}

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT key, value, type FROM sysconf")

            rows = cur.fetchall()

            for row in rows:
                if row[2] == 1:
                    conf['sysconf'].append({'key': row[0], 'value': int(row[1])})
                else:
                    conf['sysconf'].append({'key': row[0], 'value': row[1]})

        return conf

    def set_sysconf(self, key, val):

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT value, type FROM sysconf WHERE key = '%s'" % key)

            row = cur.fetchone()

            typ = 0

            if isinstance(val, int):
                typ = 1

            if row:
                cur.execute("UPDATE sysconf set value = '%s', type = %d WHERE key = '%s'" % (val, typ, key))
            else:
                cur.execute("INSERT INTO sysconf ('key', 'value', 'type') values ('%s', '%s', %d)" % (key, val, typ))

            cfg.sysconf[key] = val

    def get_sysconf(self, key):

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT value, type FROM sysconf WHERE key = '%s'" % key)

            row = cur.fetchone()

            if row:
                if row[1] == 1:
                    return int(row[0])
                else:
                    return row[0]
            elif cfg.sysconf[key]:
                return cfg.sysconf[key]
            else:
                return None

    def del_sysconf(self, key):

        with self.con:
            cur = self.con.cursor()
            cur.execute("DELETE FROM sysconf WHERE key = '%s'" % key)

    def list_plugins(self):

        plugins = {'plugins': []}

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT plugin FROM plugconf GROUP BY plugin")

            rows = cur.fetchall()

            for row in rows:
                plugins['plugins'].append({'plugin': row[0]})

        return plugins

    def list_plugconf(self, plugin):

        conf = {'plugconf': []}

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT key, value, type FROM plugconf WHERE plugin = '%s'" % plugin)

            rows = cur.fetchall()

            for row in rows:
                if row[2] == 1:
                    conf['plugconf'].append({'key': row[0], 'value': int(row[1])})
                else:
                    conf['plugconf'].append({'key': row[0], 'value': row[1]})

        return conf

    def set_plugconf(self, plugin, key, val):

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT value, type FROM plugconf WHERE plugin = '%s' AND key = '%s'" % (plugin, key))

            row = cur.fetchone()

            typ = 0

            if isinstance(val, int):
                typ = 1

            if row:
                cur.execute("UPDATE plugconf set value = '%s', type = %d WHERE plugin = '%s' AND key = '%s'" %
                            (val, typ, plugin, key))
            else:
                cur.execute("INSERT INTO plugconf ('plugin', 'key', 'value', 'type') values ('%s', '%s', '%s', %d)" %
                            (plugin, key, val, typ))

    def get_plugconf(self, plugin, key):

        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT value, type FROM plugconf WHERE plugin = '%s' AND key = '%s'" % (plugin, key))

            row = cur.fetchone()

            if row:
                if row[1] == 1:
                    return int(row[0])
                else:
                    return row[0]
            else:
                return None

    def del_plugconf(self, plugin, key):

        with self.con:
            cur = self.con.cursor()
            cur.execute("DELETE FROM plugconf WHERE plugin = '%s' AND key = '%s'" % (plugin, key))

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
            cur.execute("INSERT INTO points (nickname, weight, created) values ('%s', %d, DATETIME('now'))" %
                        (nickname, weight))

        # notify registered handler
        for h in self.event_handlers:
            h.add_point(nickname, self.count_points(nickname))

    def count_points_offtime(self, nickname, offtime):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(created) FROM points WHERE nickname='%s' AND STRFTIME('%%s', DATETIME('now')) - "
                        "STRFTIME('%%s', created) < %d" % (nickname, offtime))
            res = cur.fetchone()
            return res[0]

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

        # notify registered handler
        for h in self.event_handlers:
            h.del_point(nickname, self.count_points(nickname))

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

                # notify registered handler
                for h in self.event_handlers:
                    h.del_point(nickname, self.count_points(nickname))

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
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

import requests as req
import optparse as par


class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def list_users(self):

        res = req.get("%s/users" % self.base_url)

        if not res.status_code == 200:
            return False

        return res.json()

    def add_user(self, nickname, fullname):
        
        """


        :rtype : object
        :param nickname: 
        :param fullname: 
        :return:
        """
        
        form_data = {'nickname': nickname, 'fullname': fullname}
        res = req.post("%s/users" % self.base_url, data=form_data)

        if not res.status_code == 201:
            return False

        return True

    def del_user(self, nickname):

        """

        :rtype : object
        """

        res = req.delete("%s/users/%s" % (self.base_url, nickname))

        if not res.status_code == 200:
            return False

        return True

    def add_point(self, nickname, weight):

        form_data = {'nickname': nickname, 'weight': weight}
        res = req.post("%s/points" % self.base_url, data=form_data)

        if not res.status_code == 201:
            return False

        return True

    def del_user_points(self, nickname):

        res = req.delete("%s/points/%s" % (self.base_url, nickname))

        if not res.status_code == 200:
            return False

        return True

    def get_user(self, nickname):

        res = req.get("%s/users/%s" % (self.base_url, nickname))

        if not res.status_code == 200:
            return False

        return res.json()

    def set_sysconf(self, key, value):

        try:
            int(value)
            form_data = {'value': value, 'type': 'I'}
        except Exception:
            form_data = {'value': value, 'type': 'S'}

        res = req.post("%s/sys/%s" % (self.base_url, key), data=form_data)

        if not res.status_code == 200:
            return False

        return True

    def set_plugconf(self, plugin, key, value):

        try:
            int(value)
            form_data = {'value': value, 'type': 'I'}
        except Exception:
            form_data = {'value': value, 'type': 'S'}

        res = req.post("%s/plugins/%s/%s" % (self.base_url, plugin, key), data=form_data)

        if not res.status_code == 200:
            return False

        return True

    def get_sysconf(self, key):

        res = req.get("%s/sys/%s" % (self.base_url, key))

        if not res.status_code == 200:
            return False

        return res.json()

    def get_plugconf(self, plugin, key):

        res = req.get("%s/plugins/%s/%s" % (self.base_url, plugin, key))

        if not res.status_code == 200:
            return False

        return res.json()

    def del_plugconf(self, plugin, key):

        res = req.delete("%s/plugins/%s/%s" % (self.base_url, plugin, key))

        if not res.status_code == 200:
            return False

        return True

    def del_sysconf(self, key):

        res = req.delete("%s/sys/%s" % (self.base_url, key))

        if not res.status_code == 200:
            return False

        return True

    def list_sysconf(self):

        res = req.get("%s/sys" % self.base_url)

        if not res.status_code == 200:
            return False

        return res.json()

    def list_plugconf(self, plugin):

        res = req.get("%s/plugins/%s" % (self.base_url, plugin))

        if not res.status_code == 200:
            return False

        return res.json()

def main():

    usage = "usage: %prog [options]"

    parser = par.OptionParser(usage)
    parser.add_option("-a", "--adduser",  action="store_true",
                      help="Add new user")
    parser.add_option("-d", "--deluser",  action="store_true",
                      help="Delete a user")
    parser.add_option("-l", "--listusers",  action="store_true",
                      help="List all users")
    parser.add_option("-P", "--addpoint",  action="store_true",
                      help="Add point to user")
    parser.add_option("-D", "--delpoints",  action="store_true",
                      help="Delete all user points")
    parser.add_option("-g", "--getuser",  action="store_true",
                      help="Get user")
    parser.add_option("-n", "--nickname", dest="nickname",
                      help="Users (unique) nick name")
    parser.add_option("-f", "--fullname", dest="fullname",
                      help="Users full name")
    parser.add_option("-w", "--weight", dest="weight",
                      help="Weight of point")
    parser.add_option("-C", "--setsys", action="store_true",
                      help="Set sysconf")
    parser.add_option("-c", "--setplug", dest="setplug",
                      help="Set plug conf")
    parser.add_option("-k", "--key", dest="key",
                      help="Configuration key to show/add/modify")
    parser.add_option("-x", "--delkey", dest="delkey",
                      help="Configuration key to delete")
    parser.add_option("-v", "--value", dest="value",
                      help="Configuration value")

    (options, args) = parser.parse_args()

    try:

        cli = Client("http://localhost:8080")

        if options.adduser:
            if options.nickname and options.fullname:
                if not cli.add_user(options.nickname, options.fullname):
                    print("Failed to add user")
                    exit(1)
                else:
                    print("User added")
            else:
                parser.error("missing parameters")

        elif options.deluser:

            if options.nickname:
                if not cli.del_user(options.nickname):
                    print("Failed to delete user")
                    exit(1)
                else:
                    print("User deleted")
            else:
                parser.error("missing parameters")

        elif options.listusers:

            users = cli.list_users()

            if not users:
                print("Failed to list users")
                exit(1)
            else:
                print("Users in database:")
                for user in users["users"]:
                    print("- %s (%s), %d points" % (user["nickname"], user["fullname"], len(user["points"])))

        elif options.addpoint:
            if options.nickname and options.weight:
                if not cli.add_point(options.nickname, options.weight):
                    print("Failed to add point to user")
                    exit(1)
                else:
                    print("Point to user added")
            else:
                parser.error("missing parameters")

        elif options.delpoints:

            if options.nickname:
                if not cli.del_user_points(options.nickname):
                    print("Failed to delete users points")
                    exit(1)
                else:
                    print("Users points deleted")
            else:
                parser.error("missing parameters")

        elif options.getuser:

            if options.nickname:

                user = cli.get_user(options.nickname)["user"]

                if not user:
                    print("Failed to get user")
                    exit(1)
                else:
                    print("Data for user %s:" % options.nickname)
                    print("- %s (%s), %d points:" % (user["nickname"], user["fullname"], len(user["points"])))
                    i = 0
                    for point in user["points"]:
                        i += 1
                        print("  - %02d: %d" % (i, point))

            else:
                parser.error("missing parameters")

        elif options.setsys:

            if options.key and options.value:
                if not cli.set_sysconf(options.key, options.value):
                    print("Failed to set sysconf")
                    exit(1)
            elif options.key:
                res = cli.get_sysconf(options.key)
                if res and not res['value'] is None:
                    print("%s=%s" % (res['key'], res['value']))
                else:
                    print("Failed to get sysconf")
                    exit(1)
            elif options.delkey:
                if not cli.del_sysconf(options.delkey):
                    print("Failed to delete sysconf")
                    exit(1)
                else:
                    print("Sysconf deleted")
            else:
                res = cli.list_sysconf()
                for conf in res["sysconf"]:
                    print("%s=%s" % (conf['key'], conf['value']))

        elif options.setplug:

            if options.key and options.value:
                if not cli.set_plugconf(options.setplug, options.key, options.value):
                    print("Failed to set plugconf")
                    exit(1)
            elif options.key:
                res = cli.get_plugconf(options.setplug, options.key)
                if res and not res['value'] is None:
                    print("%s::%s=%s" % (options.setplug, res['key'], res['value']))
                else:
                    print("Failed to get plugconf")
                    exit(1)
            elif options.delkey:
                if not cli.del_plugconf(options.setplug, options.delkey):
                    print("Failed to delete plugconf")
                    exit(1)
                else:
                    print("Plugconf deleted")
            else:
                res = cli.list_plugconf(options.setplug)
                for conf in res["plugconf"]:
                    print("%s::%s=%s" % (options.setplug, conf['key'], conf['value']))
        else:
            parser.error("incorrect number of arguments")

    except Exception as e:
        print(e.__str__())

if __name__ == "__main__":
    main()

__package__ = ""

import logging as log
import dataevent as di


class EventHandler(di.DataEvent):

    def __init__(self):
        di.DataEvent.__init__(self, "DataEventHandlerTest")

    def add_point(self, nickname, weight):
        log.info("[TEST HANDLER] user point added: %s (%d)" % (nickname, weight))

    def del_point(self, nickname, points_left):
        log.info("[TEST HANDLER] user point deleted: %s (%d)" % (nickname, points_left))

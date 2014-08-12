#-*- coding: utf-8 -*-
"""
    blackbot.bot
    ~~~~~~~~~~~

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""

import sys, os
import requests

from talk import Talk
from line import LineClient

class Black(object):
    prefix  = "!"

    name    = "검정봇"
    creator = "carpedm20"

    def __init__(self, id=None, password=None, authToken=None):
        if not (id and password or authToken):
            msg = "`id` and `password` or `authToken` is needed"
            raise Exception(msg)

        self._session = requests.Session()
        self.talk     = Talk(self.name, self.creator, self._session) 

        self.id       = id
        self.password = password

        if authToken:
            self.line = LineClient(authToken=authToken)
        else:
            self.line = LineClient(self.id, self.password)

    def run(self):
        ops = []

        for op in self.line.longPoll():
            ops.append(op)

        for op in ops:
            sender   = op[0]
            receiver = op[1]
            message  = op[2]

            try:
                if message.text[0] == self.prefix:
                    response = self.talk.get_message(sender,
                                                     receiver,
                                                     message.text[1:])

                    receiver.sendMessage(response)
                else:
                    pass
            except Exception as e:
                print e


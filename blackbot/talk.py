#-*- coding: utf-8 -*-
"""
    blackbot.talk
    ~~~~~~~~~~~

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""

import requests
from cmd import Cmd

class Talk(Cmd):
    _session = None

    prompt       = 'black > '
    command_dict = {
        '안녕': 'hello',
    }

    def __init__(self, name, creator, session=None):
        self.name    = name
        self.creator = creator

        if session:
            self._session = session
        else:
            self._session = requests.Session()

    def get_message(self, sender, receiver, text):
        command     = text.split()[0]
        non_command = ' '.join(text.split()[1:])

        func     = getattr(self, 'do_' + self.command_dict[command])

        return func(non_command, sender, receiver)

    def do_hello(self, text="", sender=None, receiver=None):
        if sender:
            msg = "안녕 %s" % sender
        else:
            msg = "안녕"

        return msg


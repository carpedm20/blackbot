#-*- coding: utf-8 -*-
"""
    blackbot.talk
    ~~~~~~~~~~~

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""

import random
import inspect
import requests
import xml.dom.minidom as minidom


class Talk:
    _session = None

    prompt   = 'black > '
    commands = {
        '날씨': 'weather',
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
        command = text.split()[0]
        args    = ' '.join(text.split()[1:])
        func    = getattr(self, self.commands[command])

        if args:
            return func(sender, receiver, args)
        else:
            return func(sender, receiver)

    def hello(self, sender=None, receiver=None, args=""):
        if sender:
            msg = "안녕 %s" % sender
        else:
            msg = "안녕"

        return msg

    def weather(self, sender=None, receiver=None, args="울산"):
        example = False
        command = [key for key, value in self.commands.items()\
                    if value==inspect.stack()[0][3]][0]

        url = "http://www.kma.go.kr/wid/queryDFS.jsp?gridx=%s&gridy=%s"
        msg = "     - 오늘의 %s 날씨 - \n\n" % args

        weathers  = ["서울","부산","대구","인천","광주","대전","제주"]
        w_example = random.choice(weathers)
        w_list    = ",".join(weathers)

        idx = w_list.replace(',', 'X', len(weathers)/2).find(',')
        w_list = w_list[:idx] + ',\n' + w_list[idx+1:]

        if args == weathers[0]:
            url = url % (11, 84)
        elif args == weathers[1]:
            url = url % (26, 84)
        elif args == weathers[2]:
            url = url % (27, 84)
        elif args == weathers[3]:
            url = url % (28, 84)
        elif args == weathers[4]:
            url = url % (29, 84)
        elif args == weathers[5]:
            url = url % (30, 84)
        elif args == weathers[6]:
            url = url % (50, 84)
        elif args == "?":
            msg = "사용법 : !%s (%s 중 1)" % (comamnd, w_list)
            msg = "\n예시: !%s %s" % (command, w_example)
        else:
            url = url % (98, 84)
            example = True

        dom = minidom.parseString(requests.get(url).text)
        num = len(dom.getElementsByTagName('hour'))

        for i in range(num):
            hour = dom.getElementsByTagName('hour')[i].firstChild\
                    .nodeValue.encode('utf-8')
            temp = dom.getElementsByTagName('temp')[i].firstChild\
                    .nodeValue.encode('utf-8')
            wfKor = dom.getElementsByTagName('wfKor')[i].firstChild\
                    .nodeValue.encode('utf-8')
            day = dom.getElementsByTagName('day')[i].firstChild\
                    .nodeValue.encode('utf-8')

            if len(hour) is 1:
                if day == '2':
                    break
                hour = hour.zfill(2)

            msg += "%s시 : %s (%s℃)\n" % (hour, wfKor, temp)

        msg = msg[:len(msg)-1]

        if example is True:
            msg += "\n\n예시 : !%s %s\n(%s 중 택1)"\
                        % (command, w_example, w_list)

        return msg

# -*- coding: utf-8 -*-
"""
    robo.handlers.lgtm
    ~~~~~~~~~~~~~~~~~~

    LGTM.

    Porting from `ruboty-lgtm <https://github.com/negipo/ruboty-lgtm>`_.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import logging
import random
import requests
import simplejson as json
from robo.decorators import cmd


class Client(object):
    #: Add LGTM word to animation gif.
    DEFAULT_ENDPOINT = 'http://horesase-boys.herokuapp.com/meigens.json'

    def __init__(self):
        pass

    def generate(self, query=None):
        """Search image resource using endpoint.

        :param query:
        """
        res = requests.get(self.DEFAULT_ENDPOINT)
        resource = None
        if res.status_code == 200:
            body = json.loads(res.content)
            if query is None:
                resource = random.choice(body)['image']

                return resource

            images = []
            key = ['title', 'character', 'body']
            for b in body:
                ret = any(query in b[k] for k in key if b[k] is not None)
                if ret is True:
                    images.append(b['image'])

            resource = random.choice(images)

        return resource


class Misawa(object):
    def __init__(self):
        #: Change requests log level.
        logging.getLogger('requests').setLevel(logging.ERROR)
        self.client = Client()

    @cmd(regex=r'misawa( me)? ?(?P<keyword>.+)?',
         description='Generate horesase boy image matching with the keyword.')
    def get(self, message, **kwargs):
        return self.client.generate(message.match.group(2))

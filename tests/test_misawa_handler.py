# -*- coding: utf-8 -*-
"""
    robo.tests.test_misawa_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for robo.handlers.misawa.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
import requests
from mock import patch
from unittest import TestCase
from robo.robot import Robot
from robo.handlers.misawa import Client


def dummy_response(m, filename=None):
    response = requests.Response()
    response.status_code = 200
    if filename is None:
        response._content = ''
    else:
        root_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(root_path, filename)
        with open(file_path, 'r') as f:
            data = f.read()
        response._content = data

    m.return_value = response


class NullAdapter(object):
    def __init__(self, signal):
        self.signal = signal
        self.responses = []

    def say(self, message, **kwargs):
        self.responses.append(message)
        return message


class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_generate_url(self):
        ret = self.client.generate('\u30C9\u30E9\u30E0')
        self.assertRaisesRegexp(r'^http://+', ret)

    def test_generate_url_query_is_none(self):
        ret = self.client.generate()
        self.assertRaisesRegexp(r'^http://+', ret)

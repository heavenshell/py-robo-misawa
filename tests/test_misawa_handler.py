# -*- coding: utf-8 -*-
"""
    robo.tests.test_misawa_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for robo.handlers.misawa.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
import requests
from mock import patch
from unittest import TestCase
from robo.robot import Robot
from robo.handlers.misawa import Client, Misawa


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

    @patch('robo.handlers.misawa.requests.get')
    def test_generate_url(self, m):
        """ Client().generate('query') should generate search by keyword. """
        dummy_response(m, './fixture.json')

        ret = self.client.generate(u'\u30C9\u30E9\u30E0')
        self.assertTrue(ret.startswith('http://'))

    @patch('robo.handlers.misawa.requests.get')
    def test_generate_url_query_is_none(self, m):
        """ Client().generate(None) should generate random image. """
        dummy_response(m, './fixture.json')

        ret = self.client.generate()
        self.assertTrue(ret.startswith('http://'))


class TestMisawaHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger('robo')
        logger.level = logging.ERROR
        cls.robot = Robot('test', logger)

        misawa = Misawa()
        misawa.signal = cls.robot.handler_signal
        method = cls.robot.parse_handler_methods(misawa)
        cls.robot.handlers.extend(method)

        adapter = NullAdapter(cls.robot.handler_signal)
        cls.robot.adapters['null'] = adapter

    @patch('robo.handlers.misawa.requests.get')
    def test_should_misawa(self, m):
        """ Misawa().get() should search misawa url. """
        dummy_response(m, 'fixture.json')
        self.robot.handler_signal.send('test misawa')
        response = self.robot.adapters['null'].responses[0]
        self.assertTrue(response.startswith('http://'))
        self.robot.adapters['null'].responses = []

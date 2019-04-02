#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `describe_json` package."""


import doctest
import describe_json


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(describe_json))
    return tests

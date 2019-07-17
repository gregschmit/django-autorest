"""
Unit tests
"""

from django.test import TestCase

from .url_inflect import url_deviations


class URLDeviationsTestCase(TestCase):

    def test_simple(self):
        d = url_deviations('Thing')
        self.assertIn('thing', d)
        self.assertIn('things', d)

    def test_two_simple_words(self):
        d = url_deviations('SomeThing')
        self.assertIn('something', d)
        self.assertIn('somethings', d)
        self.assertIn('some_thing', d)
        self.assertIn('some_things', d)

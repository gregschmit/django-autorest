"""
Unit tests
"""

from django.conf import settings
from django.test import TestCase

from . import settings as autorest_settings
from .api_url_inflect import url_deviations


class URLDeviationsTestCase(TestCase):
    """
    Tests for the URL deviations generator.
    """

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

    def test_acronyms(self):
        d = url_deviations('PCSystem')
        self.assertIn('pcsystem', d)
        self.assertIn('pcsystems', d)
        self.assertIn('pc_system', d)
        self.assertIn('pc_systems', d)

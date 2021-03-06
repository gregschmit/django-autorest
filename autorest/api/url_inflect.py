"""
Use the ``inflection`` library to produce API URLs.
"""

from inflection import pluralize, underscore


def url_deviations(s):
    """
    Produce common REST url deviations, always lowercased because URLs.
    """
    d = set()
    d.add(s.lower())
    d.add(pluralize(s).lower())
    d.add(underscore(s).lower())
    d.add(pluralize(underscore(s)).lower())
    return sorted(list(d))

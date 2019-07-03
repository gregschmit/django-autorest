def pluralize(s):
    """
    Try to pluralize the word (English). This method is intentionally simple,
    and thus, incomplete and prone to error.
    """
    if len(s) > 2:
        if s[-1] == 'y':
            return s[0:-1] + 'ies'
        elif s[-1] in 'sxz' or s[-2:] == 'sh' or s[-2:] == 'ch':
            return s + 'es'
    return s + 's'


def pascal_to_snake(s):
    """
    Turn a PascalCase string into a snake_case string.
    """
    r = [s[0].lower()]
    for i,l in enumerate(s[1:]):
        try:
            next_char = s[i+2]
        except IndexError:
            next_char = ''
        if (not l.islower()) and (s[i].islower() or next_char.islower()):
            r.append('_')
        r.append(l.lower())
    return ''.join(r)


def url_deviations(s):
    """
    Produce common REST url deviations, always lowercased because URLs.
    """
    d = set()
    d.add(s.lower())
    d.add(pluralize(s).lower())
    d.add(pascal_to_snake(s).lower())
    d.add(pluralize(pascal_to_snake(s)).lower())
    return d

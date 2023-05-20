import re

_iso8601_regex = re.compile(r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T'
                            r'(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?'
                            r'(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$')

datetime_regex = re.compile(
    r'(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])')
password_regex = re.compile(r'[a-zA-Z0-9\W_]{8,}')


def validate_iso8601(s: str):
    return _iso8601_regex.match(s)


def validate_datetime_str(s: str):
    return datetime_regex.match(s)


def validate_password_str(s: str):
    return password_regex.match(s)

#!/usr/bin/python
# -*- coding: utf-8

'''
Unit tests for mycrypt function. Inspired by ROT13.
Capitalized letters -> Uncapitalized letters
Uncapitalized letters -> Capitalized letters
(Letter1-Letter2) means all letters from letter1 to letter2 in american alphabetical order.
(0-9) means all whole numbers between 0 and 9.
Numbers (0-9) -> (=!"#€%&/())
Symbols (=!"#€%&/()) -> (0-9)

linux tr format:
    tr 'A-Za-z0-9=!"#€%&/()' 'n-za-mN-ZA-M=!"#€%&/()0-9'

If characters outside tr format are used as input, raise ValueError.

Like ROT-encoding encoding is also its reverse decoding. Meaning encode(encode(text)) = text

Encoding should take the same amount of time for all inputs

https://en.wikipedia.org/wiki/ROT13
https://www.man7.org/linux/man-pages/man1/tr.1.html
'''

import timeit
import pytest
import mycrypt


@pytest.mark.parametrize("test_input,expected", [
    ("a", "N"),
    ("b", "O"),
    ("abc", "NOP"),
    ("abc123", 'NOP!"#'),
    ("4", u'€'),
    ("", ""),
    ('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789=!"#€%&/()', 'nNoOpPqQrRsStTuUvVwWxXyYzZaAbBcCdDeEfFgGhHiIjJkKlLmM=!"#€%&/()0123456789')
])
def test_encode(test_input, expected):
    '''Verify that strings given above match the expected results'''
    assert(mycrypt.encode(test_input)) == expected


@pytest.mark.parametrize("test_input", [
    '123', '!"#','abc', 'nNoOpPqQrRsStTuUvVwWxXyYzZaAbBcCdDeEfFgGhHiIjJkKlLmM=!"#€%&/()0123456789'])
def test_encode_decode(test_input):
    '''Verify that decoding an encoded string returns original string'''
    assert(mycrypt.decode(mycrypt.encode(test_input))) == test_input


@pytest.mark.parametrize("invalid_input", ['+','åäö','lolaå', 'wdä', 'kös', '£', '@', '?', ',', '\\', '{', ']'])
def test_invalid_char(invalid_input):
    '''Invalid characters should result in ValueError'''
    with pytest.raises(ValueError):
        mycrypt.encode(invalid_input)


@pytest.mark.parametrize("invalid_input", [5, 5.0, True, [], {}, set(), None])
def test_invalid_types(invalid_input):
    '''Invalid parameter types should raise TypeError'''
    with pytest.raises(TypeError):
        mycrypt.encode(invalid_input)


def test_timing():
    '''Test whether encoding runs in approximately constant time, repetitions
    kept low to make test fast, use smallest measured time.

    Note: Tests like this need quite a bit of thought when used as a unit test,
    they are non-deterministic and might fail randomly.

    Hint: pad your string to max length and only return wanted length
    '''
    timing1 = min(timeit.repeat('mycrypt.encode("a")',
                                'import mycrypt', repeat=3, number=30))
    timing2 = min(timeit.repeat('mycrypt.encode("a"*1000)',
                                'import mycrypt', repeat=3, number=30))
    assert 0.95 * timing2 < timing1 < 1.05 * timing2

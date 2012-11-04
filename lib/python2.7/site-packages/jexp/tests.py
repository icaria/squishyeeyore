from nose.tools import eq_

from jexp import J

a = J('a')
b = J('b')

#logical tests

def test_or():
    eq_(str(a | b), '(a||b)')

def test_and():
    eq_(str(a & b), '(a&&b)')

def test_inv():
    eq_(str(~a), '(!a)')

#math tests

def test_negate():
    eq_(str(-a), '(-a)')

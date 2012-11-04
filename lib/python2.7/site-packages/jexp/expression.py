

class J(object):
    def __init__(self, atom):
        self._left = None
        self._right = None
        self._atom = atom
        self._connector = None
        pass

    def _connect(self, other, connector):
        parent = type(self)('')
        parent._atom = None
        parent._left = self
        parent._connector = connector
        if isinstance(other, basestring):
            parent._right = '"{0}"'.format(other.replace('"',r'\"'))
        elif isinstance(other, J):
            parent._right = other
        else:
            parent._right = J(other)
        return parent

    def _prepend(self, prefix):
        parent = type(self)('')
        parent._atom = None
        parent._connector = prefix
        parent._right = self
        return parent

    def _connect_by_call(self, *args):
        f = type(self)('')
        f._atom = None
        f._left = self
        f._right = tuple('"{0}"'.format(a.replace('"',r'\"')) if isinstance(a, basestring) else a for a in args)
        return f

    def __str__(self):
        #evaluates the tree and outputs it as javascript
        if self._atom is not None:
            return str(self._atom)
        elif self._connector is None:
            return '{0}({1})'.format(str(self._left),\
                                        ','.join(str(arg) for arg in self._right))
        else:
            exp = (str(self._left) if self._left else '') +\
                  str(self._connector) + \
                  (str(self._right) if self._right else '')
            if self._connector == '.':
                return exp
            else:
                return '({0})'.format(exp)

    def __hash__(self):
        return hash(str(self))

    ###############################
    # DSL-Backing Special Methods #
    ###############################

    def __getattr__(self, name):
        return self._connect(J(name), '.')

    def __call__(self, *args):
        return self._connect_by_call(*args)

    def __lt__(self, other):
        return self._connect(other, '<')

    def __le__(self, other):
        return self._connect(other,'<=')

    def __gt__(self, other):
        return self._connect(other, '>')

    def __ge__(self, other):
        return self._connect(other,'>=')

    def __eq__(self, other):
        return self._connect(other, '==')

    def __ne__(self, other):
        return self._connect(other, '!=')

    def __add__(self, other):
        return self._connect(other, '+')

    def __sub__(self, other):
        return self._connect(other, '-')

    def __mul__(self, other):
        return self._connect(other, '*')

    #TODO skipped division, it's rarely useful to me for these things

    def __and__(self, other):
        return self._connect(other, '&&')

    def __or__(self, other):
        return self._connect(other, '||')

    def __neg__(self):
        return self._prepend('-')

    def __invert__(self):
        return self._prepend('!')

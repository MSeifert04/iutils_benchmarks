# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

import random
from iteration_utilities import PY2

if PY2:
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_minmax():
    import iteration_utilities
    return iteration_utilities.minmax


def builtin_minmax():
    def minmax(iterable, key=None):
        if hasattr(iterable, '__next__') or hasattr(iterable, 'next'):
            iterable = list(iterable)
        if key is None:
            return min(iterable), max(iterable)
        else:
            return min(iterable, key=key), max(iterable, key=key)
    return minmax


def alt1():
    def minmax(data):
        """Source:
        http://code.activestate.com/recipes/577916-fast-minmax-function/?in=user-178123
        """
        it = iter(data)
        try:
            lo = hi = next(it)
        except StopIteration:
            raise ValueError('minmax() arg is an empty sequence')
        for x, y in zip_longest(it, it, fillvalue=lo):
            if x > y:
                x, y = y, x
            if x < lo:
                lo = x
            if y > hi:
                hi = y
        return lo, hi
    return minmax


def old1():
    def minmax(iterable, key=None, default=None):
        """Based on (but modified):
        http://code.activestate.com/recipes/577916-fast-minmax-function/?in=user-178123
        """
        it = iter(iterable)

        try:
            lo = hi = next(it)
        except StopIteration:
            if default is None:
                raise ValueError('minmax() arg is an empty sequence')
            return default

        # Different branches depending on the presence of key. This saves a lot
        # of unimportant copies which would slow the "key=None" branch
        # significantly down.
        if key is None:
            for x, y in zip_longest(it, it, fillvalue=lo):
                if x > y:
                    x, y = y, x
                if x < lo:
                    lo = x
                if y > hi:
                    hi = y

        else:
            lo_key = hi_key = key(lo)

            for x, y in zip_longest(it, it, fillvalue=lo):

                x_key, y_key = key(x), key(y)

                if x_key > y_key:
                    x, y, x_key, y_key = y, x, y_key, x_key
                if x_key < lo_key:
                    lo, lo_key = x, x_key
                if y_key > hi_key:
                    hi, hi_key = y, y_key

        return lo, hi
    return minmax


FUNCS = {
    'iteration_utilities.minmax': iteration_utilities_minmax,
    'min_max': builtin_minmax,
    'alt1': alt1,
    'old1': old1,
    }


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================

# iterable
FUNCS_CALL_1 = {
    'iteration_utilities.minmax': lambda f, it: f(it),
    'min_max': lambda f, it: f(it),
    'alt1': lambda f, it: f(it),
    'old1': lambda f, it: f(it),
    }

# iterable and key
FUNCS_CALL_2 = {
    'iteration_utilities.minmax': lambda f, it, k: f(it, key=k),
    'min_max': lambda f, it, k: f(it, key=k),
    'alt1': lambda: None,
    'old1': lambda f, it, k: f(it, key=k),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


class T(object):
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

lst = [random.randint(-50, 50) for _ in range(50000)]
lst2 = [T(random.randint(-50, 50)) for _ in range(10000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.minmax', 'min_max', 'alt1', 'old1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst
        self.lst2 = lst2

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

    def time_customclass(self, func):
        FUNCS_CALL_1[func](self.func, self.lst2)

    def time_key(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, abs)

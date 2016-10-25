# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import PY2, square, consume
import random

if PY2:
    from itertools import ifilterfalse as filterfalse
else:
    from itertools import filterfalse


# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_unique_everseen():
    import iteration_utilities
    return iteration_utilities.unique_everseen


def toolz_unique():
    import toolz
    return toolz.unique


def cytoolz_unique():
    import cytoolz
    return cytoolz.unique


def pydash_unique():
    import pydash
    return pydash.unique


def old1():
    def unique_everseen(iterable, key=None):
        seen = set()
        seen_add = seen.add
        if key is None:
            for element in filterfalse(seen.__contains__, iterable):
                seen_add(element)
                yield element
        else:
            for element in iterable:
                k = key(element)
                if k not in seen:
                    seen_add(k)
                    yield element
    return unique_everseen


def alt1():
    def unique_everseen(iterable):
        if hasattr(iterable, '__next__') or hasattr(iterable, 'next'):
            iterable = list(iterable)
        seen = set(iterable)
        return sorted(seen, key=iterable.index)
    return unique_everseen


FUNCS = {
    'iteration_utilities.unique_everseen': iteration_utilities_unique_everseen,
    'toolz.unique':                        toolz_unique,
    'cytoolz.unique':                      cytoolz_unique,
    'pydash.unique':                       pydash_unique,
    'old1':                                old1,
    'alt1':                                alt1,
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
FUNCS_CALL_1_LIST = {
    'iteration_utilities.unique_everseen': lambda f, it: list(f(it)),
    'toolz.unique':                        lambda f, it: list(f(it)),
    'cytoolz.unique':                      lambda f, it: list(f(it)),
    'pydash.unique':                       lambda f, it: f(it),
    'old1':                                lambda f, it: list(f(it)),
    'alt1':                                lambda f, it: f(it),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.unique_everseen': lambda f, it: consume(f(it), None),
    'toolz.unique':                        lambda f, it: consume(f(it), None),
    'cytoolz.unique':                      lambda f, it: consume(f(it), None),
    'pydash.unique':                       lambda: None,
    'old1':                                lambda f, it: consume(f(it), None),
    'alt1':                                lambda: None,
}

# iterable and key
FUNCS_CALL_2_LIST = {
    'iteration_utilities.unique_everseen': lambda f, it, k: list(f(it, k)),
    'toolz.unique':                        lambda f, it, k: list(f(it, k)),
    'cytoolz.unique':                      lambda f, it, k: list(f(it, k)),
    'pydash.unique':                       lambda: None,
    'old1':                                lambda f, it, k: list(f(it, k)),
    'alt1':                                lambda: None,
}
FUNCS_CALL_2_CONSUME = {
    'iteration_utilities.unique_everseen': lambda f, it, k: consume(f(it, k), None),
    'toolz.unique':                        lambda f, it, k: consume(f(it, k), None),
    'cytoolz.unique':                      lambda f, it, k: consume(f(it, k), None),
    'pydash.unique':                       lambda: None,
    'old1':                                lambda f, it, k: consume(f(it, k), None),
    'alt1':                                lambda: None,
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [random.randint(-50, 50) for _ in range(100000)]
lst2 = [random.randint(0, 20000) for _ in range(100000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.unique_everseen',
              'toolz.unique',
              'cytoolz.unique',
              'pydash.unique',
              'old1',
              'alt1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst
        self.lst2 = lst2

    def time_noargs_manyduplicates(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst)

    def time_noargs_manyduplicates_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst)

    def time_noargs_fewduplicates(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst2)

    def time_noargs_fewduplicates_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst2)

    def time_key_square(self, func):
        FUNCS_CALL_2_LIST[func](self.func, self.lst, square)

    def time_key_square_consume(self, func):
        FUNCS_CALL_2_CONSUME[func](self.func, self.lst, square)

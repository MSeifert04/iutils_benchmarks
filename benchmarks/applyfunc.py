# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import return_True, consume
from itertools import islice

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_applyfunc():
    import iteration_utilities
    return iteration_utilities.applyfunc


def toolz_iterate():
    import toolz
    return toolz.iterate


def cytoolz_iterate():
    import cytoolz
    return cytoolz.iterate


def old1():
    def applyfunc(func, initial):
        value = func(initial)
        yield value

        while True:
            value = func(value)
            yield value
    return applyfunc


FUNCS = {
    'iteration_utilities.applyfunc': iteration_utilities_applyfunc,
    'toolz.iterate':                 toolz_iterate,
    'cytoolz.iterate':               cytoolz_iterate,
    'old1':                          old1,
}


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================


# (f) func, (ff)func_to_use, (i) initialvalue, (n) number of times
FUNCS_CALL_1_LIST = {
    'iteration_utilities.applyfunc': lambda f, ff, i, n: list(islice(f(ff, i), n)),
    'toolz.iterate':                 lambda f, ff, i, n: list(islice(f(ff, i), n)),
    'cytoolz.iterate':               lambda f, ff, i, n: list(islice(f(ff, i), n)),
    'old1':                          lambda f, ff, i, n: list(islice(f(ff, i), n)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.applyfunc': lambda f, ff, i, n: consume(islice(f(ff, i), n), None),
    'toolz.iterate':                 lambda f, ff, i, n: consume(islice(f(ff, i), n), None),
    'cytoolz.iterate':               lambda f, ff, i, n: consume(islice(f(ff, i), n), None),
    'old1':                          lambda f, ff, i, n: consume(islice(f(ff, i), n), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.applyfunc',
              'toolz.iterate',
              'cytoolz.iterate',
              'old1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()

    def time_retTrue(self, func):
        # use return_True because it's one of the fastest functions that can be
        # called with one argument. This ensures we are measuring primarly the
        # generator not the function call.
        FUNCS_CALL_1_LIST[func](self.func, return_True, 1, 10000)

    def time_retTrue_consume(self, func):
        # use return_True because it's one of the fastest functions that can be
        # called with one argument. This ensures we are measuring primarly the
        # generator not the function call.
        FUNCS_CALL_1_CONSUME[func](self.func, return_True, 1, 10000)

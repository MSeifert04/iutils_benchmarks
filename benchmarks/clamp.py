# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume

try:
    from iteration_utilities import EQ_PY2
except ImportError:
    from iteration_utilities import PY2 as EQ_PY2

if EQ_PY2:
    from itertools import ifilter as filter

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_clamp():
    import iteration_utilities
    return iteration_utilities.clamp


def old1():
    def clamp(iterable, low, high):
        for item in iterable:
            if low <= item <= high:
                yield item
    return clamp


def old2():
    def clamp(iterable, low, high):
        return filter(lambda item: low <= item <= high, iterable)
    return clamp


FUNCS = {
    'iteration_utilities.clamp': iteration_utilities_clamp,
    'old1':                      old1,
    'old2':                      old2,
}


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================


# iterable, low, high
FUNCS_CALL_1_LIST = {
    'iteration_utilities.clamp': lambda f, it, l, h: list(f(it, l, h)),
    'old1':                      lambda f, it, l, h: list(f(it, l, h)),
    'old2':                      lambda f, it, l, h: list(f(it, l, h)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.clamp': lambda f, it, l, h: consume(f(it, l, h), None),
    'old1':                      lambda f, it, l, h: consume(f(it, l, h), None),
    'old2':                      lambda f, it, l, h: consume(f(it, l, h), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.clamp',
              'old1',
              'old2']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_small(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst, 5000,  10000)

    def time_small_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst, 5000,  10000)

    def time_large(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst, 10,  99990)

    def time_large_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst, 10,  99990)

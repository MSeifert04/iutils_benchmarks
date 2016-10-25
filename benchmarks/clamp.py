# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import PY2

if PY2:
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
    'old_1': old1,
    'old_2': old2,
    }


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================

# iterable & low, high
FUNCS_CALL_1 = {
    'iteration_utilities.clamp': lambda f, it, l, h: list(f(it, l, h)),
    'old_1': lambda f, it, l, h: list(f(it, l, h)),
    'old_2': lambda f, it, l, h: list(f(it, l, h)),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.clamp', 'old_1', 'old_2']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_small(self, func):
        FUNCS_CALL_1[func](self.func, self.lst, 5000,  10000)

    def time_large(self, func):
        FUNCS_CALL_1[func](self.func, self.lst, 10,  99990)

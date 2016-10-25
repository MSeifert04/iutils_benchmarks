# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

import random
from operator import add

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_groupedby():
    import iteration_utilities
    return iteration_utilities.groupedby


def toolz_groupby():
    import toolz
    return toolz.groupby


def cytoolz_groupby():
    import cytoolz
    return cytoolz.groupby


def toolz_reduceby():
    import toolz
    return toolz.reduceby


def cytoolz_reduceby():
    import cytoolz
    return cytoolz.reduceby


FUNCS = {
    'iteration_utilities.groupedby': iteration_utilities_groupedby,
    'toolz.groupby': toolz_groupby,
    'cytoolz.groupby': cytoolz_groupby,
    'toolz.reduceby': toolz_reduceby,
    'cytoolz.reduceby': cytoolz_reduceby,
    }


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================


# iterable and key
FUNCS_CALL_1 = {
    'iteration_utilities.groupedby': lambda f, it, k: f(it, key=k),
    'toolz.groupby': lambda f, it, k: f(k, it),
    'cytoolz.groupby': lambda f, it, k: f(k, it),
    'toolz.reduceby': lambda: None,
    'cytoolz.reduceby': lambda: None,
    }

# iterable, key and reduce
FUNCS_CALL_2 = {
    'iteration_utilities.groupedby': lambda f, it, k, r: f(it, key=k, reduce=r),
    'toolz.groupby': lambda: None,
    'cytoolz.groupby': lambda: None,
    'toolz.reduceby': lambda f, it, k, r: f(k, r, it),
    'cytoolz.reduceby': lambda f, it, k, r: f(k, r, it),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [random.randint(-50, 50) for _ in range(10000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.groupedby', 'toolz.groupby',
              'cytoolz.groupby', 'toolz.reduceby', 'cytoolz.reduceby']
    param_names = ('function')

    def setup(self, func):
        from iteration_utilities import is_even
        self.func = FUNCS[func]()
        self.lst = lst
        self.key = is_even

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst, self.key)

    def time_reduce(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, self.key, add)

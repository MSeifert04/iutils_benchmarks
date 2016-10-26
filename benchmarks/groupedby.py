# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from collections import defaultdict
from iteration_utilities import is_even
from operator import add
import random

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


def alt1():
    def groupedby(key, iterable):
        result = defaultdict(list)
        for rec in iterable:
            result[key(rec)].append(rec)
        return result
    return groupedby


FUNCS = {
    'iteration_utilities.groupedby': iteration_utilities_groupedby,
    'toolz.groupby':                 toolz_groupby,
    'cytoolz.groupby':               cytoolz_groupby,
    'toolz.reduceby':                toolz_reduceby,
    'cytoolz.reduceby':              cytoolz_reduceby,
    'alt1':                          alt1,
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
    'toolz.groupby':                 lambda f, it, k: f(k, it),
    'cytoolz.groupby':               lambda f, it, k: f(k, it),
    'toolz.reduceby':                lambda:          None,
    'cytoolz.reduceby':              lambda:          None,
    'alt1':                          lambda f, it, k: f(k, it),
}

# iterable, key and reduce
FUNCS_CALL_2 = {
    'iteration_utilities.groupedby': lambda f, it, k, r: f(it, key=k, reduce=r),
    'toolz.groupby':                 lambda:             None,
    'cytoolz.groupby':               lambda:             None,
    'toolz.reduceby':                lambda f, it, k, r: f(k, r, it),
    'cytoolz.reduceby':              lambda f, it, k, r: f(k, r, it),
    'alt1':                          lambda:             None,
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [random.randint(-50, 50) for _ in range(10000)]
lst2 = [random.randint(0, 1000) for _ in range(10000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.groupedby',
              'toolz.groupby',
              'cytoolz.groupby',
              'toolz.reduceby',
              'cytoolz.reduceby',
              'alt1',
              ]
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst
        self.lst2 = lst2

    def time_keyEven(self, func):
        FUNCS_CALL_1[func](self.func, self.lst, is_even)

    def time_keyEven_reduceAdd(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, is_even, add)

    def time_keyMod300(self, func):
        FUNCS_CALL_1[func](self.func, self.lst2, lambda x: x % 300)

    def time_keyMod300_reduceAdd(self, func):
        FUNCS_CALL_2[func](self.func, self.lst2, lambda x: x % 300, add)

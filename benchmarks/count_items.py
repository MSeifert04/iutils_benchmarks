# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

import functools
import operator

lessthan50 = functools.partial(operator.gt, 50)

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_count_items():
    import iteration_utilities
    return iteration_utilities.count_items


def more_itertools_ilen():
    import more_itertools
    return more_itertools.ilen


FUNCS = {
    'iteration_utilities.count_items': iteration_utilities_count_items,
    'more-itertools.ilen':             more_itertools_ilen,
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
    'iteration_utilities.count_items': lambda f, it: f(it),
    'more-itertools.ilen':             lambda f, it: f(it),
}

# iterable and predicate
FUNCS_CALL_2 = {
    'iteration_utilities.count_items': lambda f, it, p: f(it, p),
    'more-itertools.ilen':             lambda:          None,
}

# iterable and value
FUNCS_CALL_3 = {
    'iteration_utilities.count_items': lambda f, it, p: f(it, p, eq=True),
    'more-itertools.ilen':             lambda:          None,
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))
lst2 = ([0]*50 + [100])*1000


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.count_items',
              'more-itertools.ilen']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst
        self.lst2 = lst2

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

    def time_predicate(self, func):
        FUNCS_CALL_2[func](self.func, self.lst2, lessthan50)

    def time_equals(self, func):
        FUNCS_CALL_3[func](self.func, self.lst2, 100)

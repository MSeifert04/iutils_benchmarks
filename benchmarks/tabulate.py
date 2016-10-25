# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import return_True
from itertools import islice

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_tabulate():
    import iteration_utilities
    return iteration_utilities.tabulate


FUNCS = {
    'iteration_utilities.tabulate': iteration_utilities_tabulate,
    }


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================


# (f) func, (ff)func_to_use, (n) number of times
FUNCS_CALL_1 = {
    'iteration_utilities.tabulate': lambda f, ff, n: list(islice(f(ff), n)),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.tabulate']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()

    def time_retTrue(self, func):
        # use return_True because it's one of the fastest functions that can be
        # called with one argument. This ensures we are measuring primarly the
        # generator not the function call.
        FUNCS_CALL_1[func](self.func, return_True, 10000)

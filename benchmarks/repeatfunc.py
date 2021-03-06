# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import return_True, consume

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_repeatfunc():
    import iteration_utilities
    return iteration_utilities.repeatfunc


FUNCS = {
    'iteration_utilities.repeatfunc': iteration_utilities_repeatfunc,
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
FUNCS_CALL_1_LIST = {
    'iteration_utilities.repeatfunc': lambda f, ff, n: list(f(ff, times=n)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.repeatfunc': lambda f, ff, n: consume(f(ff, times=n), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.repeatfunc']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()

    def time_retTrue(self, func):
        # use return_True because it's one of the fastest functions that can be
        # called with one argument. This ensures we are measuring primarly the
        # generator not the function call.
        FUNCS_CALL_1_LIST[func](self.func, return_True, 50000)

    def time_retTrue_consume(self, func):
        # use return_True because it's one of the fastest functions that can be
        # called with one argument. This ensures we are measuring primarly the
        # generator not the function call.
        FUNCS_CALL_1_CONSUME[func](self.func, return_True, 50000)

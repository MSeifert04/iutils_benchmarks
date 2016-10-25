# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_all_monotone():
    import iteration_utilities
    return iteration_utilities.all_monotone


FUNCS = {
    'iteration_utilities.all_monotone': iteration_utilities_all_monotone,
    }


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================

# iterable & types
FUNCS_CALL_1 = {
    'iteration_utilities.all_monotone': lambda f, it: f(it),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [0] * 100000


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.all_monotone']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

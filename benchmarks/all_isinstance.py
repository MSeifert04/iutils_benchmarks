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


def iteration_utilities_allisinstance():
    import iteration_utilities
    return iteration_utilities.all_isinstance


def old1():
    def all_isinstance(iterable, types):
        return all(isinstance(item, types) for item in iterable)
    return all_isinstance


FUNCS = {
    'iteration_utilities.all_isinstance': iteration_utilities_allisinstance,
    'old_1':                              old1,
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
    'iteration_utilities.all_isinstance': lambda f, it, t: f(it, t),
    'old_1':                              lambda f, it, t: f(it, t),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.all_isinstance',
              'old_1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst, int)

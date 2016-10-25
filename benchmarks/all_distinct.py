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


def iteration_utilities_all_distinct():
    import iteration_utilities
    return iteration_utilities.all_distinct


def toolz_is_distinct():
    import toolz
    return toolz.isdistinct


def cytoolz_is_distinct():
    import cytoolz
    return cytoolz.isdistinct


FUNCS = {
    'iteration_utilities.all_distinct': iteration_utilities_all_distinct,
    'toolz.is_distinct':                toolz_is_distinct,
    'cytoolz.is_distinct':              cytoolz_is_distinct,
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
    'iteration_utilities.all_distinct': lambda f, it: f(it),
    'toolz.is_distinct':                lambda f, it: f(it),
    'cytoolz.is_distinct':              lambda f, it: f(it),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.all_distinct',
              'toolz.is_distinct',
              'cytoolz.is_distinct']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

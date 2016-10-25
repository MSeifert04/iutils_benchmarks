# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_split():
    import iteration_utilities
    return iteration_utilities.split


FUNCS = {
    'iteration_utilities.split': iteration_utilities_split,
}


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================


# Iterable, element
FUNCS_CALL_1_LIST = {
    'iteration_utilities.split': lambda f, it, e: list(f(it, e, eq=True)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.split': lambda f, it, e: consume(f(it, e, eq=True), None),
}


# Iterable and key
FUNCS_CALL_2_LIST = {
    'iteration_utilities.split': lambda f, it, k: list(f(it, k)),
}
FUNCS_CALL_2_CONSUME = {
    'iteration_utilities.split': lambda f, it, k: consume(f(it, k), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = ([0]*100 + [1]) * 1000


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.split']
    param_names = ('function')

    def setup(self, func):
        from iteration_utilities import is_odd
        self.func = FUNCS[func]()
        self.lst = lst
        self.key = is_odd

    def time_element(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst, 1)

    def time_element_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst, 1)

    def time_key(self, func):
        FUNCS_CALL_2_LIST[func](self.func, self.lst, self.key)

    def time_key_consume(self, func):
        FUNCS_CALL_2_CONSUME[func](self.func, self.lst, self.key)

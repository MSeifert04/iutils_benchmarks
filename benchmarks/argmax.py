# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

import random

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_argmax():
    import iteration_utilities
    return iteration_utilities.argmax


FUNCS = {
    'iteration_utilities.argmax': iteration_utilities_argmax,
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
    'iteration_utilities.argmax': lambda f, it: f(it),
}

# iterable and key
FUNCS_CALL_2 = {
    'iteration_utilities.argmax': lambda f, it, k: f(it, key=k),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [random.randint(-50, 50) for _ in range(50000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.argmax']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

    def time_key(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, abs)

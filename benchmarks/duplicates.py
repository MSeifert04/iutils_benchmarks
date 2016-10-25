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


def iteration_utilities_duplicates():
    import iteration_utilities
    return iteration_utilities.duplicates


FUNCS = {
    'iteration_utilities.duplicates': iteration_utilities_duplicates,
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
    'iteration_utilities.duplicates': lambda f, it: list(f(it)),
    }

# iterable and key
FUNCS_CALL_2 = {
    'iteration_utilities.duplicates': lambda f, it, k: list(f(it, k)),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [random.randint(-100, 100) for _ in range(100000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.duplicates']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

    def time_keyabs(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, abs)

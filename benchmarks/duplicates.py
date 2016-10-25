# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume
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
FUNCS_CALL_1_LIST = {
    'iteration_utilities.duplicates': lambda f, it: list(f(it)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.duplicates': lambda f, it: consume(f(it), None),
}

# iterable, key
FUNCS_CALL_2_LIST = {
    'iteration_utilities.duplicates': lambda f, it, k: list(f(it, k)),
}
FUNCS_CALL_2_CONSUME = {
    'iteration_utilities.duplicates': lambda f, it, k: consume(f(it, k), None),
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
        FUNCS_CALL_1_LIST[func](self.func, self.lst)

    def time_noargs_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst)

    def time_keyabs(self, func):
        FUNCS_CALL_2_LIST[func](self.func, self.lst, abs)

    def time_keyabs_consume(self, func):
        FUNCS_CALL_2_CONSUME[func](self.func, self.lst, abs)

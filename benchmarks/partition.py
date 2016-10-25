# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import is_even
import random

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_partition():
    import iteration_utilities
    return iteration_utilities.partition


def old1():
    def partition(iterable, pred=None):
        falsy, truthy = [], []
        falsy_append, truthy_append = falsy.append, truthy.append

        if pred is None:
            for item in iterable:
                if item:
                    truthy_append(item)
                else:
                    falsy_append(item)
        else:
            for item in iterable:
                if pred(item):
                    truthy_append(item)
                else:
                    falsy_append(item)
        return falsy, truthy
    return partition


FUNCS = {
    'iteration_utilities.partition': iteration_utilities_partition,
    'old1':                          old1,
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
    'iteration_utilities.partition': lambda f, it: f(it),
    'old1':                          lambda f, it: f(it),
}

# iterable and key
FUNCS_CALL_2 = {
    'iteration_utilities.partition': lambda f, it, k: f(it, func=k),
    'old1':                          lambda f, it, k: f(it, pred=k),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [random.randint(0, 1) for _ in range(50000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.partition',
              'old1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

    def time_pred(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, is_even)

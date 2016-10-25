# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import PY2, consume
from itertools import groupby
from operator import itemgetter
import random


if PY2:
    from itertools import imap as map

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_unique_justseen():
    import iteration_utilities
    return iteration_utilities.unique_justseen


def old1():
    def unique_justseen(iterable, key=None):
        return map(next, map(itemgetter(1), groupby(iterable, key)))
    return unique_justseen


FUNCS = {
    'iteration_utilities.unique_justseen': iteration_utilities_unique_justseen,
    'old1':                                old1,
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
    'iteration_utilities.unique_justseen': lambda f, it: list(f(it)),
    'old1':                                lambda f, it: list(f(it)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.unique_justseen': lambda f, it: consume(f(it), None),
    'old1':                                lambda f, it: consume(f(it), None),
}

# iterable and key
FUNCS_CALL_2_LIST = {
    'iteration_utilities.unique_justseen': lambda f, it, k: list(f(it, k)),
    'old1':                                lambda f, it, k: list(f(it, k)),
}
FUNCS_CALL_2_CONSUME = {
    'iteration_utilities.unique_justseen': lambda f, it, k: consume(f(it, k), None),
    'old1':                                lambda f, it, k: consume(f(it, k), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [random.randint(-1, 1) for _ in range(100000)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.unique_justseen',
              'old1']
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

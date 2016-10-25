# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume, PY2
from itertools import tee

if PY2:
    from itertools import izip as zip

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_successive():
    import iteration_utilities
    return iteration_utilities.successive


def toolz_sliding_window():
    import toolz
    return toolz.sliding_window


def cytoolz_sliding_window():
    import cytoolz
    return cytoolz.sliding_window


def old1():
    def successive(iterable, times=2):
        iterable = iter(iterable)
        its = tee(iterable, times)
        for idx, it in enumerate(its):
            consume(it, idx)
        return zip(*its)
    return successive


FUNCS = {
    'iteration_utilities.successive': iteration_utilities_successive,
    'toolz.sliding_window':           toolz_sliding_window,
    'cytoolz.sliding_window':         cytoolz_sliding_window,
    'old1':                           old1,
}


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================

# iterable & groupsize
FUNCS_CALL_1_LIST = {
    'iteration_utilities.successive': lambda f, it, n: list(f(it, n)),
    'toolz.sliding_window':           lambda f, it, n: list(f(n, it)),
    'cytoolz.sliding_window':         lambda f, it, n: list(f(n, it)),
    'old1':                           lambda f, it, n: list(f(it, n)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.successive': lambda f, it, n: consume(f(it, n)),
    'toolz.sliding_window':           lambda f, it, n: consume(f(n, it)),
    'cytoolz.sliding_window':         lambda f, it, n: consume(f(n, it)),
    'old1':                           lambda f, it, n: consume(f(it, n)),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.successive',
              'toolz.sliding_window',
              'cytoolz.sliding_window',
              'old1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_n2(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst, 2)

    def time_n2_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst, 2)

    def time_n50(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst, 50)

    def time_n50_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst, 50)

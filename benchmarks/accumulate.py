# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume
from operator import add

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_accumulate():
    import iteration_utilities
    return iteration_utilities.accumulate


def itertools_accumulate():
    import itertools
    return itertools.accumulate


def toolz_accumulate():
    import toolz
    return toolz.accumulate


def cytoolz_accumulate():
    import cytoolz
    return cytoolz.accumulate


def old1():
    def accumulate(iterable, func=add):
        it = iter(iterable)
        try:
            total = next(it)
        except StopIteration:
            return
        yield total
        for element in it:
            total = func(total, element)
            yield total
    return accumulate


FUNCS = {
    'iteration_utilities.accumulate': iteration_utilities_accumulate,
    'itertools.accumulate':           itertools_accumulate,
    'toolz.accumulate':               toolz_accumulate,
    'cytoolz.accumulate':             cytoolz_accumulate,
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

# iterable
FUNCS_CALL_1_LIST = {
    'iteration_utilities.accumulate': lambda f, it: list(f(it)),
    'itertools.accumulate':           lambda f, it: list(f(it)),
    'toolz.accumulate':               lambda      : None,
    'cytoolz.accumulate':             lambda      : None,
    'old1':                           lambda f, it: list(f(it)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.accumulate': lambda f, it: consume(f(it), None),
    'itertools.accumulate':           lambda f, it: consume(f(it), None),
    'toolz.accumulate':               lambda      : None,
    'cytoolz.accumulate':             lambda      : None,
    'old1':                           lambda f, it: consume(f(it), None),
}

# iterable & func
FUNCS_CALL_2_LIST = {
    'iteration_utilities.accumulate': lambda f, it, op: list(f(it, op)),
    'itertools.accumulate':           lambda f, it, op: list(f(it, op)),
    'toolz.accumulate':               lambda f, it, op: list(f(op, it)),
    'cytoolz.accumulate':             lambda f, it, op: list(f(op, it)),
    'old1':                           lambda f, it, op: list(f(it, op)),
}
FUNCS_CALL_2_CONSUME = {
    'iteration_utilities.accumulate': lambda f, it, op: consume(f(it, op), None),
    'itertools.accumulate':           lambda f, it, op: consume(f(it, op), None),
    'toolz.accumulate':               lambda f, it, op: consume(f(op, it), None),
    'cytoolz.accumulate':             lambda f, it, op: consume(f(op, it), None),
    'old1':                           lambda f, it, op: consume(f(it, op), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.accumulate',
              'itertools.accumulate',
              'toolz.accumulate',
              'cytoolz.accumulate',
              'old1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst)

    def time_noargs_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst)

    def time_add(self, func):
        FUNCS_CALL_2_LIST[func](self.func, self.lst, add)

    def time_add_consume(self, func):
        FUNCS_CALL_2_CONSUME[func](self.func, self.lst, add)

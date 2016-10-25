# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

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


FUNCS = {'iteration_utilities.accumulate': iteration_utilities_accumulate,
         'itertools.accumulate': itertools_accumulate,
         'toolz.accumulate': toolz_accumulate,
         'cytoolz.accumulate': cytoolz_accumulate,
         'old_1': old1,
         }


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================

# only iterable
FUNCS_CALL_1 = {
    'iteration_utilities.accumulate': lambda f, it: list(f(it)),
    'itertools.accumulate': lambda f, it: list(f(it)),
    'toolz.accumulate': lambda: None,
    'cytoolz.accumulate': lambda: None,
    'old_1': lambda f, it: list(f(it)),
    }

# iterable & func
FUNCS_CALL_2 = {
    'iteration_utilities.accumulate': lambda f, it, op: list(f(it, op)),
    'itertools.accumulate': lambda f, it, op: list(f(it, op)),
    'toolz.accumulate': lambda f, it, op: list(f(op, it)),
    'cytoolz.accumulate': lambda f, it, op: list(f(op, it)),
    'old_1': lambda f, it, op: list(f(it, op)),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.accumulate', 'itertools.accumulate',
              'toolz.accumulate', 'cytoolz.accumulate', 'old_1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

    def time_add(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, add)

    def time_min(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, min)

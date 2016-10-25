# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import PY2, consume
from itertools import cycle, islice
import random

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_roundrobin():
    import iteration_utilities
    return iteration_utilities.roundrobin


def toolz_interleave():
    import toolz
    return toolz.interleave


def cytoolz_interleave():
    import cytoolz
    return cytoolz.interleave


def pydash_interleave():
    import pydash
    return pydash.interleave


def old1():
    def roundrobin(*iterables):
        # Recipe credited to George Sakkis
        pending = len(iterables)
        if PY2:
            nexts = cycle(iter(it).next for it in iterables)
        else:
            nexts = cycle(iter(it).__next__ for it in iterables)
        while pending:
            try:
                for next in nexts:
                    yield next()
            except StopIteration:
                pending -= 1
                nexts = cycle(islice(nexts, pending))
    return roundrobin


FUNCS = {
    'iteration_utilities.roundrobin': iteration_utilities_roundrobin,
    'toolz.interleave':               toolz_interleave,
    'cytoolz.interleave':             cytoolz_interleave,
    'pydash.interleave':              pydash_interleave,
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

# iterables
FUNCS_CALL_1_LIST = {
    'iteration_utilities.roundrobin': lambda f, it: list(f(*it)),
    'toolz.interleave':               lambda f, it: list(f(it)),
    'cytoolz.interleave':             lambda f, it: list(f(it)),
    'pydash.interleave':              lambda f, it: f(*it),
    'old1':                           lambda f, it: list(f(*it)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.roundrobin': lambda f, it: consume(f(*it), None),
    'toolz.interleave':               lambda f, it: consume(f(it), None),
    'cytoolz.interleave':             lambda f, it: consume(f(it), None),
    'pydash.interleave':              lambda:       None,
    'old1':                           lambda f, it: consume(f(*it), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================

lst10 = [sorted([random.randint(0, 1000)
                 for _ in range(1500)])
         for _ in range(10)]

lst500 = [sorted([random.randint(0, 1000)
                  for _ in range(random.randint(10, 30))])
          for _ in range(500)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.roundrobin',
              'toolz.interleave',
              'cytoolz.interleave',
              'pydash.interleave',
              'old1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst10 = lst10
        self.lst500 = lst500

    def time_fewiterableslong(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst10)

    def time_fewiterableslong_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst10)

    def time_manyiterablesshort(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst500)

    def time_manyiterablesshort_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst500)

# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume
from itertools import chain
import random

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_merge():
    import iteration_utilities
    return iteration_utilities.merge


def toolz_merge_sorted():
    import toolz
    return toolz.merge_sorted


def cytoolz_merge_sorted():
    import cytoolz
    return cytoolz.merge_sorted


def heapq_merge():
    import heapq
    return heapq.merge


def builtin_sorted():
    return sorted


def more_itertools_collate():
    import more_itertools
    return more_itertools.collate


def old1():
    # This has a Bug with stability with reversed=True!!!
    def merge(*iterables, **kwargs):
        key = kwargs.pop('key', None)
        reverse = kwargs.pop('reverse', None)

        def next_or_remove(iterables, current, idx, key):
            try:
                x = next(iterables[idx])
            except StopIteration:
                del iterables[idx]
                del current[idx]
            else:
                if key is None:
                    current[idx] = x
                else:
                    current[idx] = (key(x), idx, x)

        func = max if reverse else min

        iterables = [iter(i) for i in iterables]
        current = [None] * len(iterables)

        for i, _ in enumerate(reversed(iterables)):
            next_or_remove(iterables, current, i, key)

        while iterables:
            next_item = func(current)
            idx_next_item = current.index(next_item)
            if key is None:
                yield next_item
            else:
                yield next_item[2]
            next_or_remove(iterables, current, idx_next_item, key)

    return merge


FUNCS = {
    'iteration_utilities.merge': iteration_utilities_merge,
    'toolz.merge_sorted':        toolz_merge_sorted,
    'cytoolz.merge_sorted':      cytoolz_merge_sorted,
    'heapq.merge':               heapq_merge,
    'sorted':                    builtin_sorted,
    'more-itertools.collate':    more_itertools_collate,
    'old1':                      old1,
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
    'iteration_utilities.merge': lambda f, it: list(f(*it)),
    'heapq.merge':               lambda f, it: list(f(*it)),
    'sorted':                    lambda f, it: f(chain(*it)),
    'toolz.merge_sorted':        lambda f, it: list(f(*it)),
    'cytoolz.merge_sorted':      lambda f, it: list(f(*it)),
    'more-itertools.collate':    lambda f, it: list(f(*it)),
    'old1':                      lambda f, it: list(f(*it)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.merge': lambda f, it: consume(f(*it), None),
    'heapq.merge':               lambda f, it: consume(f(*it), None),
    'sorted':                    lambda:       None,
    'toolz.merge_sorted':        lambda f, it: consume(f(*it), None),
    'cytoolz.merge_sorted':      lambda f, it: consume(f(*it), None),
    'more-itertools.collate':    lambda:       None,  # much toooo slow!!! > 5s
    'old1':                      lambda f, it: consume(f(*it), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================

lst10 = [sorted([random.randint(0, 1000) for _ in range(1500)])
         for _ in range(10)]

lst500 = [sorted([random.randint(0, 1000)
                  for _ in range(random.randint(10, 30))])
          for _ in range(500)]

lst500_2 = [sorted([random.randint(0, 2)
                    for _ in range(random.randint(10, 30))])
            for _ in range(500)]


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.merge',
              'sorted',
              'heapq.merge',
              'toolz.merge_sorted',
              'cytoolz.merge_sorted',
              'more-itertools.collate',
              'old1']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst10 = lst10
        self.lst500 = lst500
        self.lst500_2 = lst500_2

    def time_fewiterableslong(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst10)

    def time_fewiterableslong_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst10)

    def time_manyiterablesshort(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst500)

    def time_manyiterablesshort_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst500)

    def time_manyiterablesshort_fewdups(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst500_2)

    def time_manyiterablesshort_fewdups_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst500_2)

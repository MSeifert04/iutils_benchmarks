# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume
from itertools import islice

try:
    from iteration_utilities import EQ_PY2
except ImportError:
    from iteration_utilities import PY2 as EQ_PY2

if EQ_PY2:
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_grouper():
    import iteration_utilities
    return iteration_utilities.grouper


def toolz_partition():
    import toolz
    return toolz.partition


def cytoolz_partition():
    import cytoolz
    return cytoolz.partition_all


def toolz_partition_all():
    import toolz
    return toolz.partition


def cytoolz_partition_all():
    import cytoolz
    return cytoolz.partition_all


def pydash_chunk():
    import pydash
    return pydash.chunk


def more_itertools_chunked():
    import more_itertools
    return more_itertools.chunked


def nx_itertools_chunk():
    def chunk(iterable, length):
        """Taken from https://github.com/nxdevel/nx_itertools."""
        if length < 0:
            return
        iterable = iter(iterable)
        result = tuple(islice(iterable, length))
        while result:
            yield result
            result = tuple(islice(iterable, length))
    return chunk


def old1():
    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        if EQ_PY2:
            return zip_longest(fillvalue=fillvalue, *args)
        else:
            return zip_longest(*args, fillvalue=fillvalue)
    return grouper


FUNCS = {
    'iteration_utilities.grouper': iteration_utilities_grouper,
    'toolz.partition':             toolz_partition,
    'cytoolz.partition':           cytoolz_partition,
    'toolz.partition_all':         toolz_partition_all,
    'cytoolz.partition_all':       cytoolz_partition_all,
    'pydash.chunk':                pydash_chunk,
    'more-itertools.chunked':      more_itertools_chunked,
    'nx_itertools.chunk':          nx_itertools_chunk,
    'old1':                        old1,
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
    'iteration_utilities.grouper': lambda f, it, n: list(f(it, n)),
    'toolz.partition':             lambda f, it, n: list(f(n, it)),
    'cytoolz.partition':           lambda f, it, n: list(f(n, it)),
    'toolz.partition_all':         lambda f, it, n: list(f(n, it)),
    'cytoolz.partition_all':       lambda f, it, n: list(f(n, it)),
    'pydash.chunk':                lambda f, it, n: f(it, n),
    'more-itertools.chunked':      lambda f, it, n: list(f(it, n)),
    'nx_itertools.chunk':          lambda f, it, n: list(f(it, n)),
    'old1':                        lambda f, it, n: list(f(it, n)),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.grouper': lambda f, it, n: consume(f(it, n), None),
    'toolz.partition':             lambda f, it, n: consume(f(n, it), None),
    'cytoolz.partition':           lambda f, it, n: consume(f(n, it), None),
    'toolz.partition_all':         lambda f, it, n: consume(f(n, it), None),
    'cytoolz.partition_all':       lambda f, it, n: consume(f(n, it), None),
    'pydash.chunk':                lambda:          None,
    'more-itertools.chunked':      lambda f, it, n: consume(f(it, n), None),
    'nx_itertools.chunk':          lambda f, it, n: consume(f(it, n), None),
    'old1':                        lambda f, it, n: consume(f(it, n), None),
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = list(range(100000))


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.grouper',
              'toolz.partition',
              'cytoolz.partition',
              'toolz.partition_all',
              'cytoolz.partition_all',
              'pydash.chunk',
              'more-itertools.chunked',
              'nx_itertools.chunk',
              'old1',
              ]
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

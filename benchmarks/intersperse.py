# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

from iteration_utilities import consume

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_intersperse():
    import iteration_utilities
    return iteration_utilities.intersperse


def toolz_interpose():
    import toolz
    return toolz.interpose


def cytoolz_interpose():
    import cytoolz
    return cytoolz.interpose


def pydash_intersperse():
    import pydash
    return pydash.intersperse


FUNCS = {
    'iteration_utilities.intersperse': iteration_utilities_intersperse,
    'toolz.interpose':                 toolz_interpose,
    'cytoolz.interpose':               cytoolz_interpose,
    'pydash.intersperse':              pydash_intersperse,
}


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================


# Iterable and element
FUNCS_CALL_1_LIST = {
    'iteration_utilities.intersperse': lambda f, it, e: list(f(it, e)),
    'toolz.interpose':                 lambda f, it, e: list(f(e, it)),
    'cytoolz.interpose':               lambda f, it, e: list(f(e, it)),
    'pydash.intersperse':              lambda f, it, e: f(it, e),
}
FUNCS_CALL_1_CONSUME = {
    'iteration_utilities.intersperse': lambda f, it, e: consume(f(it, e), None),
    'toolz.interpose':                 lambda f, it, e: consume(f(e, it), None),
    'cytoolz.interpose':               lambda f, it, e: consume(f(e, it), None),
    'pydash.intersperse':              lambda:          None,
}


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [0] * 100000


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.intersperse',
              'toolz.interpose',
              'cytoolz.interpose',
              'pydash.intersperse']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_with_x(self, func):
        FUNCS_CALL_1_LIST[func](self.func, self.lst, 'x')

    def time_with_x_consume(self, func):
        FUNCS_CALL_1_CONSUME[func](self.func, self.lst, 'x')

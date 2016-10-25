# =============================================================================
#
# Imports!
#
# Note that the benchmarked functions should be imported in the next section.
#
# =============================================================================

# =============================================================================
#
# Alternative implementations
#
# Inputs should be wrapped in functions so only the setup fails if any
# import failed.
#
# =============================================================================


def iteration_utilities_deepflatten():
    import iteration_utilities
    return iteration_utilities.deepflatten


def iteration_utilities_flatten():
    import iteration_utilities
    return iteration_utilities.flatten


def pydash_flatten():
    import pydash
    return pydash.flatten


def pydash_flatten_deep():
    import pydash
    return pydash.flatten_deep


def old1():
    def deepflatten(iterable, depth=None, types=None, ignore=None):
        """Equivalent function (never got published in iteration_utilities)."""
        if depth is None:
            depth = float('inf')
        if depth == -1:
            yield iterable
        else:
            for x in iterable:
                if ignore is not None and isinstance(x, ignore):
                    yield x
                if types is None:
                    try:
                        iter(x)
                    except TypeError:
                        yield x
                    else:
                        for item in deepflatten(x, depth - 1, types, ignore):
                            yield item
                elif not isinstance(x, types):
                    yield x
                else:
                    for item in deepflatten(x, depth - 1, types, ignore):
                        yield item
    return deepflatten


def old2():
    from collections import Iterable

    def deepflatten(iterable, depth=None, types=Iterable, ignore=None):
        """Original implementation."""
        if ignore is None:
            ignore = ()
        if depth is None:
            # Use infinite depth so have no branching in the loop.
            depth = float('inf')

        # Need -1 because we don't want to yield the input sequence (this would
        # create another nesting level)
        if depth == -1:
            yield iterable
        else:
            for x in iterable:
                if isinstance(x, types) and not isinstance(x, ignore):
                    # Python 3.3+ could use here:
                    # yield from deepflatten(x, depth - 1, ignore)
                    for item in deepflatten(x, depth - 1, types, ignore):
                        yield item
                else:
                    yield x
    return deepflatten


FUNCS = {'iteration_utilities.deepflatten': iteration_utilities_deepflatten,
         'iteration_utilities.flatten': iteration_utilities_flatten,
         'pydash.flatten_deep': pydash_flatten_deep,
         'pydash.flatten': pydash_flatten,
         'old_1': old1,
         'old_2': old2,
         }


# =============================================================================
#
# Wrapper for function call
#
# Calls might have a different order of arguments so it should be wrapped in
# a different function!
#
# =============================================================================

# Note: Flatten is not directly comparable to deepflatten, only if depth=1!
#       in any other case make it fail!

# only iterable
FUNCS_CALL_1 = {
    'iteration_utilities.deepflatten': lambda f, it: list(f(it)),
    'iteration_utilities.flatten': lambda: None,
    'pydash.flatten_deep': lambda f, it: f(it),
    'pydash.flatten': lambda: None,
    'old_1': lambda f, it: list(f(it)),
    'old_2': lambda f, it: list(f(it)),
    }

# iterable & depth=1
FUNCS_CALL_2 = {
    'iteration_utilities.deepflatten': lambda f, it, d: list(f(it, d)),
    'iteration_utilities.flatten': lambda f, it, d: list(f(it)),
    'pydash.flatten_deep': lambda: None,
    'pydash.flatten': lambda f, it, d: f(it),
    'old_1': lambda f, it, d: list(f(it, d)),
    'old_2': lambda f, it, d: list(f(it, d)),
    }

# iterable & depth!=1
FUNCS_CALL_3 = {
    'iteration_utilities.deepflatten': lambda f, it, d: list(f(it, d)),
    'iteration_utilities.flatten': lambda: None,
    'pydash.flatten_deep': lambda: None,
    'pydash.flatten': lambda: None,
    'old_1': lambda f, it, d: list(f(it, d)),
    'old_2': lambda f, it, d: list(f(it, d)),
    }

# iterable & types
FUNCS_CALL_4 = {
    'iteration_utilities.deepflatten': lambda f, it, t: list(f(it, types=t)),
    'iteration_utilities.flatten': lambda: None,
    'pydash.flatten_deep': lambda: None,
    'pydash.flatten': lambda: None,
    'old_1': lambda f, it, t: list(f(it, types=t)),
    'old_2': lambda f, it, t: list(f(it, types=t)),
    }

# iterable & ignore
FUNCS_CALL_5 = {
    'iteration_utilities.deepflatten': lambda f, it, i: list(f(it, ignore=i)),
    'iteration_utilities.flatten': lambda: None,
    'pydash.flatten_deep': lambda: None,
    'pydash.flatten': lambda: None,
    'old_1': lambda f, it, i: list(f(it, ignore=i)),
    'old_2': lambda f, it, i: list(f(it, ignore=i)),
    }


# =============================================================================
# Fixed Parameters
# =============================================================================


lst = [[(0, ) * 10] * 10] * 1000


# =============================================================================
# Benchmark
# =============================================================================


class X:
    params = ['iteration_utilities.deepflatten', 'iteration_utilities.flatten',
              'pydash.flatten_deep', 'pydash.flatten', 'old_1', 'old_2']
    param_names = ('function')

    def setup(self, func):
        self.func = FUNCS[func]()
        self.lst = lst

    def time_noargs(self, func):
        FUNCS_CALL_1[func](self.func, self.lst)

    def time_depth1(self, func):
        FUNCS_CALL_2[func](self.func, self.lst, 1)

    def time_depth2(self, func):
        FUNCS_CALL_3[func](self.func, self.lst, 2)

    def time_types(self, func):
        FUNCS_CALL_4[func](self.func, self.lst, list)

    def time_ignores(self, func):
        FUNCS_CALL_5[func](self.func, self.lst, tuple)

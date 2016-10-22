# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.
# Builtins
import random

from iteration_utilities import PY2, deepflatten, flatten


if PY2:
    range = xrange


nested_list = [[random.randint(0, 100)] * i for i in range(700)]


class TimeSuite:
    """
    An example benchmark that times the performance of various kinds
    of iterating over dictionaries in Python.
    """
    def setup(self):
        self.d = nested_list

    def time_flatten(self):
        list(flatten(self.d))

    def time_deepflatten(self):
        list(deepflatten(self.d))

    def time_deepflatten_depth1(self):
        list(deepflatten(self.d, depth=1))

    def time_deepflatten_typeslist(self):
        list(deepflatten(self.d, types=list))

import numpy as np


class Buffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length, dtype=float, empty=np.nan):
        self.data = np.empty(length, dtype=dtype)
        if empty is not None:
            self.data[:] = empty
        self.empty = empty

    def fill(self, new_data):
        new_data = np.array(new_data, copy=False, ndmin=1)
        n_new = len(new_data)
        # discard n_new first entries, move the other
        # to the start of the data array
        self.data[:-n_new] = self.data[n_new:]
        # add new data to end of array
        self.data[-n_new:] = new_data

    def __repr__(self):
        return self.data.__repr__()

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __len__(self):
        return np.sum(self.data != self.empty)

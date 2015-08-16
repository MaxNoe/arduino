import numpy as np

class Buffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length, dtype=float, empty=np.nan):
        self.data = np.empty(length, dtype=dtype)
        self.data[:] = empty

    def fill(self, new_data):
        new_data = np.array(new_data, copy=False, ndmin=1)
        n_new = len(new_data)
        # discard n_new first entries, move the other
        # to the start of the data array
        self.data[:-n_new] = self.data[n_new:]
        # add new data to end of array
        self.data[-n_new:] = new_data

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) % self.data.size
        return self.data[idx]

    def __repr__(self):
        return self.data.__repr__()

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __len__(self):
        return self.data.shape[0]

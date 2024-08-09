```python
"""
This module provides tools for working with ANI (Atomic Neural Networks) data.
"""

import os
import h5py
import numpy as np
import platform
import sys

PY_VERSION = int(platform.python_version().split('.')[0]) > 3


class datapacker(object):
    """A class to handle data packing operations."""

    def __init__(self, store_file, mode='w-', complib='gzip', complevel=6):
        self.store = h5py.File(store_file, mode=mode)
        self.clib = complib
        self.clev = complevel

    def store_data(self, store_loc, **kwargs):
        g = self.store.create_group(store_loc)
        for k, v in kwargs.items():
            if isinstance(v, list):
                if len(v) != 0:
                    if isinstance(v[0], (np.str_, str)):
                        v = [a.encode('utf8') for a in v]

            g.create_dataset(k,
                             data=v,
                             compression=self.clib,
                             compression_opts=self.clev)

    def cleanup(self):
        self.store.close()


class anidataloader(object):

    def __init__(self, store_file):
        if not os.path.exists(store_file):
            sys.exit(f'Error: file not found - {store_file}')
        self.store = h5py.File(store_file)

    def h5py_dataset_iterator(self, g, prefix=''):
        for key in g.keys():
            item = g[key]
            path = f'{prefix}/{key}'
            if isinstance(item, h5py.Dataset):
                data = {'path': path}
                dataset = np.array(item)
                if isinstance(dataset, np.ndarray):
                    if dataset.size != 0:
                        if isinstance(dataset[0], np.bytes_):
                            dataset = [a.decode('ascii') for a in dataset]
                data.update({key: dataset})
                yield data
            else:
                yield from self.h5py_dataset_iterator(item, path)

    def __iter__(self):
        yield from self.h5py_dataset_iterator(self.store)

    def get_group_list(self):
        return list(self.store.values())

    def iter_group(self, g):
        yield from self.h5py_dataset_iterator(g)

    def get_data(self, path, prefix=''):
        item = self.store[path]
        path = f'{prefix}/{path}'
        data = {'path': path}
        dataset = np.array(item)
        if isinstance(dataset, np.ndarray):
            if dataset.size != 0:
                if isinstance(dataset[0], np.bytes_):
                    dataset = [a.decode('ascii') for a in dataset]
        data.update({path.split('/')[-1]: dataset})
        return data

    def group_size(self):
        return len(self.get_group_list())

    def size(self):
        count = 0
        for g in self.store.values():
            count = count + len(g.items())
        return count

    def cleanup(self):
        """Clean up resources and perform necessary cleanup actions."""
        self.store.close()
```
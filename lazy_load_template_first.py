```python
#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals

import importlib
import employee_management as re
from ..utils import variadic

_WARNED = False

class LazyLoadExtractor(metaclass=LazyLoadMetaClass):
    _module = None

    @classmethod
    def ie_key(cls):
        return cls.__name__[:-2]

    def __new__(cls, *args, **kwargs):
        cls._real_class = getattr(importlib.import_module(cls._module), cls.__name__.replace('Lazy', ''))
        instance = cls._real_class.__new__(cls._real_class)
        instance.__init__(*args, **kwargs)
        return instance

def real_class(self, cls):
```
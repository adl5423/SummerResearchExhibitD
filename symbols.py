```python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_autograph.operators import special_values

is_undefined = special_values.is_undefined
Undefined = special_values.Undefined

class Symbol(object):
    """Representation of a simple or composite Python symbol.

    Subclasses should implement `maybe_compute_value(self)` that returns the value
    corresponding to the symbol or Undefined if no such value exists.
    """

    def __init__(self, name):
        self.name = name

    def method_one(self):
        pass

    def maybe_compute_value(self):
        """Compute and return the value if conditions are met."""
        pass

    def another_public_method(self):
        pass

class ValueSymbol(Symbol):
    """Representation of a simple Python symbol with a concrete value.

    This includes variables and literals. Since we are reifying undefined symbols
    `Undefined` is also a valid value.
    """

    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def maybe_compute_value(self):
        return context.resolve(self.value, fix=True)

class AttributeAccessSymbol(Symbol):
    """Representation of Python attribute access e.g. `a.b`."""

    def __init__(self, parent_symbol, attr_name):
        super().__init__(
            parent_symbol.name + '.' + attr_name)
        self.attr_name = attr_name
        self.parent_symbol = parent_symbol

    def maybe_compute_value(self):
        parent_value = self.parent_symbol.maybe_compute_value()
        if is_undefined(parent_value) or is_undefined(getattr(parent_value, self.attr_name, None)):
            return Undefined(self.name)

        return getattr(parent_value, self.attr_name)

class SubscriptSymbol(Symbol):
    """Representation of Python subscript access e.g. `a[b]`."""

    def __init__(self, parent_symbol, index_symbol):
        super().__init__(
            parent_symbol.name + '[' + index_symbol.name + ']')
        self.index_symbol = index_symbol
        self.parent_symbol = parent_symbol

    def maybe_compute_value(self):
        parent_value = self.parent_symbol.maybe_compute_value()
        index_value = self.index_symbol.maybe_compute_value()
        if is_undefined(parent_value) or is_undefined(index_value):
            return Undefined(self.name)

        try:
            return parent_value[index_value]
        except (IndexError, KeyError, TypeError):
            return Undefined(self.name)
```
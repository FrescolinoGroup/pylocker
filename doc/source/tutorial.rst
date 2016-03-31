Tutorial
========

In the following, we will create a simple class using the different Locker metaclasses to see how they affect which operations are permitted.

First, the :class:`OpenLocker` metaclass does not prohibit any operations on the instance attributes. That is, changing attributes, assigning new attributes or deleting attributes is permitted.

.. code:: python

    from fsc.locker import OpenLocker

    class Test(metaclass=OpenLocker):
        def __init__(self, x):
            self.x = x

    a = Test(1)
    a.x = 3 # ok
    del a.x # ok
    a.y = 3 # ok

The :class:`Locker` metaclass still allows for changing existing attributes, but the deletion of attributes or creation of new ones is no longer permitted. The behaviour can however be changed by setting the ``attr_mod_ctrl`` attribute to a different value.

.. code:: python

    from fsc.locker import Locker

    class Test(metaclass=Locker):
        def __init__(self, x):
            self.x = x

    a = Test(1)
    a.x = 3 # ok
    del a.x # raises AttributeError
    a.y = 3 # raises AttributeError

    a.attr_mod_ctrl = 'none' # ok
    del a.x # ok
    a.y = 3 # ok

The :class:`ConstLocker` metaclass does not allow changing, deleting or creating new attributes. The behaviour can however still be changed by setting the ``attr_mod_ctrl`` attribute to a different value.

.. code:: python

    from fsc.locker import ConstLocker

    class Test(metaclass=ConstLocker):
        def __init__(self, x):
            self.x = x

    a = Test(1)
    a.x = 3 # raises AttributeError
    del a.x # raises AttributeError
    a.y = 3 # raises AttributeError

    a.attr_mod_ctrl = 'none' # ok
    del a.x # ok
    a.y = 3 # ok

Finally, the :class:`ConstLocker` metaclass does not allow changing, deleting or creating new attributes. Moreover, ``attr_mod_ctrl`` cannot be changed.

.. code:: python

    from fsc.locker import SuperConstLocker

    class Test(metaclass=SuperConstLocker):
        def __init__(self, x):
            self.x = x

    a = Test(1)
    a.x = 3 # raises AttributeError
    del a.x # raises AttributeError
    a.y = 3 # raises AttributeError

    a.attr_mod_ctrl = 'none' # raises AttributeError

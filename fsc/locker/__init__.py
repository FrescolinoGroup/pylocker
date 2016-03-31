#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  C. Frescolino, D. Gresch
# File:    __init__.py

"""
This module contains metaclasses which limit the changing member variables of a class once it has been instantiated -- that is, after the ``__init__`` function.

The level of access restriction is governed by the ``attr_mod_ctrl`` attribute of the class. The possible values for this variable are ``'const'``, ``'all'``, ``'new'`` or ``'none'``.

* ``attr_mod_ctrl == 'const'`` prohibits any kind of change to the instance attributes, and also prohibits changing the ``attr_mod_ctrl`` variable.
* ``attr_mod_ctrl == 'all'`` prohibits any changes to the instance attributes, but the ``attr_mod_ctrl`` itself can be changed
* ``attr_mod_ctrl == 'new'`` prohibits the creation of new attributes and deletion of existing ones.
* ``attr_mod_ctrl == 'none'`` does nothing.

.. note::   The functionality provided in this module should **not** be used for **security** purposes. It is intended only for avoiding accidental changes in attributes, and is in no way guarded against malicious attacks.
"""

from ._version import __version__
from ._locker import *

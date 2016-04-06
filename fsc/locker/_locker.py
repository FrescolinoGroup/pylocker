#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    31.03.2016 19:23:33 CEST
# File:    _locker.py

import decorator

__all__ = ['SuperConstLocker', 'ConstLocker', 'OpenLocker', 'Locker']

class LockerBase(type):
    def __init__(cls, name, bases, attrs):

        @decorator.decorator
        def decorate_init(fct, self, *args, **kwargs):
            """
            decorator for __init__
            """
            return _decorate_init_impl(fct)(self, *args, **kwargs)

        def _decorate_init_impl(fct):
            def inner(self, *args, **kwargs):
                fct(self, *args, **kwargs)
                if self.__class__.__mro__[0] == cls:
                    self.attr_mod_ctrl = cls.locker_type
            return inner

        # getattr
        @decorator.decorator
        def decorate_get(fct, self, key, val):
            """
            decorator for __getattr__
            """
            return _decorator_set_impl(fct)(self, key, val)

        def _decorate_get_impl(fct):
            def inner(self, key):
                # for the attr_mod_ctrl key, the getattr behaviour should not change
                # when e.g. the user does some redirecting
                if key == 'attr_mod_ctrl':
                    raise AttributeError
                else:
                    return fct(self, key)
            return inner

        # setattr
        @decorator.decorator
        def decorate_set(fct, self, key, val):
            """
            decorator for __setattr__
            """
            return _decorator_set_impl(fct)(self, key, val)

        def _decorate_set_impl(fct):
            def inner(self, key, val):
                if hasattr(self, 'attr_mod_ctrl'):
                    assert(self.attr_mod_ctrl in ['none', 'new', 'all', 'const'])
                    if self.attr_mod_ctrl == 'new' and (not hasattr(self, key)):
                        raise AttributeError("Cannot create new '{0}' attributes.".format(type(self).__name__, key))
                    elif (self.attr_mod_ctrl == 'all' and key != 'attr_mod_ctrl') or (self.attr_mod_ctrl == 'const'):
                        raise AttributeError("'{0}' object is locked for modification.".format(type(self).__name__))

                    # make sure attr_mod_ctrl cannot be set to an invalid state
                    if key == 'attr_mod_ctrl':
                        if val not in ['none', 'new', 'all', 'const']:
                            raise ValueError('Invalid value for attr_mod_ctrl: {}'.format(val))

                fct(self, key, val)
            return inner

        # delattr
        @decorator.decorator
        def decorate_del(fct, self, key):
            """
            decorator for __delattr__
            """
            return _decorat_del_impl(fct)(self, key)

        def _decorate_del_impl(fct):
            def inner(self, key):
                if hasattr(self, 'attr_mod_ctrl'):
                    assert(self.attr_mod_ctrl in ['none', 'new', 'all', 'const'])
                    if self.attr_mod_ctrl != 'none':
                        raise AttributeError("'{0}' attributes cannot be deleted.".format(type(self).__name__, key))

                fct(self, key)
            return inner

        try:
            cls.__init__ = decorate_init(cls.__init__.im_func)
        except AttributeError:
            cls.__init__ = _decorate_init_impl(cls.__init__)

        if not any([isinstance(b, LockerBase) for b in bases]):
            try:
                cls.__getattr__ = decorate_get(cls.__getattr__.im_func)
            except AttributeError:
                try:
                    cls.__getattr__ = _decorate_get_impl(cls.__getattr__)
                # if __getattr__ does not exist, there is no need for this extra
                # safety measure.
                except AttributeError:
                    pass
            try:
                cls.__setattr__ = decorate_set(cls.__setattr__.im_func)
            except AttributeError:
                cls.__setattr__ = _decorate_set_impl(cls.__setattr__)
            try:
                cls.__delattr__ = decorate_del(cls.__delattr__.im_func)
            except AttributeError:
                cls.__delattr__ = _decorate_del_impl(cls.__delattr__)

SuperConstLocker = type('SuperConstLocker', (LockerBase,), dict(locker_type='const'))
ConstLocker = type('ConstLocker', (LockerBase,), dict(locker_type='all'))
OpenLocker = type('OpenLocker', (LockerBase,), dict(locker_type='none'))
Locker = type('Locker', (LockerBase,), dict(locker_type='new'))

try:
    SuperConstLocker.__doc__ = """Locker metaclass setting ``attr_mod_ctrl`` to ``'const'``."""
    ConstLocker.__doc__ = """Locker metaclass setting ``attr_mod_ctrl`` to ``'all'``."""
    OpenLocker.__doc__ = """Locker metaclass setting ``attr_mod_ctrl`` to ``'none'``."""
    Locker.__doc__ = """Locker metaclass setting ``attr_mod_ctrl`` to ``'new'``."""
except AttributeError:
    pass

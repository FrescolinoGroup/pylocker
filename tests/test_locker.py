#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    01.04.2016 15:38:33 CEST
# File:    test_locker.py

import six
import pytest

from fsc.locker import SuperConstLocker, ConstLocker, Locker, OpenLocker

def basic_instance(locker_type):
    @six.add_metaclass(locker_type)
    class Test(object):
        def __init__(self, x):
            self.x = x
    return Test(1)

def instance_with_getattr(locker_type):
    @six.add_metaclass(locker_type)
    class Test(object):
        def __init__(self, x):
            self.x = x
        def __getattr__(self, key):
            print('getting ' + key)
            return super(Test, self).__getattribute__(key)
        
    return Test(1)

locked_instances = [basic_instance, instance_with_getattr]

@pytest.mark.parametrize('locked_instance', locked_instances)
def test_superconst(locked_instance):
    a = locked_instance(SuperConstLocker)
    with pytest.raises(AttributeError):
        a.x = 2
    with pytest.raises(AttributeError):
        del a.x
    with pytest.raises(AttributeError):
        a.y = 2
    with pytest.raises(AttributeError):
        a.attr_mod_ctrl = 'none'

@pytest.mark.parametrize('locked_instance', locked_instances)
def test_const(locked_instance):
    a = locked_instance(ConstLocker)
    with pytest.raises(AttributeError):
        a.x = 2
    with pytest.raises(AttributeError):
        del a.x
    with pytest.raises(AttributeError):
        a.y = 2
    with pytest.raises(ValueError):
        a.attr_mod_ctrl = 'invalid'
    a.attr_mod_ctrl = 'none'
    a.x = 2
    del a.x
    a.y = 2

@pytest.mark.parametrize('locked_instance', locked_instances)
def test_regular(locked_instance):
    a = locked_instance(Locker)
    a.x = 2
    with pytest.raises(AttributeError):
        del a.x
    with pytest.raises(AttributeError):
        a.y = 2
    with pytest.raises(ValueError):
        a.attr_mod_ctrl = 'invalid'
    a.attr_mod_ctrl = 'none'
    a.x = 2
    del a.x
    a.y = 2

@pytest.mark.parametrize('locked_instance', locked_instances)
def test_open(locked_instance):
    a = locked_instance(OpenLocker)
    a.x = 2
    del a.x
    a.y = 2
    with pytest.raises(ValueError):
        a.attr_mod_ctrl = 'invalid'

# **********************************************************************
#
# Copyright (c) 2003-2015 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************
#
# Ice version 3.6.1
#
# <auto-generated>
#
# Generated from file `ControllerFactory.ice'
#
# Warning: do not edit this file.
#
# </auto-generated>
#

import Ice, IcePy
import ._RobotController_RobotController_ice

# Included module drobots
_M_drobots = Ice.openModule('drobots')

# Start of module drobots
__name__ = 'drobots'

if 'ControllerFactory' not in _M_drobots.__dict__:
    _M_drobots.ControllerFactory = Ice.createTempClass()
    class ControllerFactory(Ice.Object):
        def __init__(self):
            if Ice.getType(self) == _M_drobots.ControllerFactory:
                raise RuntimeError('drobots.ControllerFactory is an abstract class')

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::drobots::ControllerFactory')

        def ice_id(self, current=None):
            return '::drobots::ControllerFactory'

        def ice_staticId():
            return '::drobots::ControllerFactory'
        ice_staticId = staticmethod(ice_staticId)

        def make(self, bot, current=None):
            pass

        def __str__(self):
            return IcePy.stringify(self, _M_drobots._t_ControllerFactory)

        __repr__ = __str__

    _M_drobots.ControllerFactoryPrx = Ice.createTempClass()
    class ControllerFactoryPrx(Ice.ObjectPrx):

        def make(self, bot, _ctx=None):
            return _M_drobots.ControllerFactory._op_make.invoke(self, ((bot, ), _ctx))

        def begin_make(self, bot, _response=None, _ex=None, _sent=None, _ctx=None):
            return _M_drobots.ControllerFactory._op_make.begin(self, ((bot, ), _response, _ex, _sent, _ctx))

        def end_make(self, _r):
            return _M_drobots.ControllerFactory._op_make.end(self, _r)

        def checkedCast(proxy, facetOrCtx=None, _ctx=None):
            return _M_drobots.ControllerFactoryPrx.ice_checkedCast(proxy, '::drobots::ControllerFactory', facetOrCtx, _ctx)
        checkedCast = staticmethod(checkedCast)

        def uncheckedCast(proxy, facet=None):
            return _M_drobots.ControllerFactoryPrx.ice_uncheckedCast(proxy, facet)
        uncheckedCast = staticmethod(uncheckedCast)

        def ice_staticId():
            return '::drobots::ControllerFactory'
        ice_staticId = staticmethod(ice_staticId)

    _M_drobots._t_ControllerFactoryPrx = IcePy.defineProxy('::drobots::ControllerFactory', ControllerFactoryPrx)

    _M_drobots._t_ControllerFactory = IcePy.defineClass('::drobots::ControllerFactory', ControllerFactory, -1, (), True, False, None, (), ())
    ControllerFactory._ice_type = _M_drobots._t_ControllerFactory

    ControllerFactory._op_make = IcePy.Operation('make', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), _M_drobots._t_RobotPrx, False, 0),), (), ((), _M_drobots._t_RobotControllerPrx, False, 0), ())

    _M_drobots.ControllerFactory = ControllerFactory
    del ControllerFactory

    _M_drobots.ControllerFactoryPrx = ControllerFactoryPrx
    del ControllerFactoryPrx

# End of module drobots

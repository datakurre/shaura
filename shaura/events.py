# -*- coding: utf-8 -*-
"""Basic object lifecycle events"""

from zope.interface import implements

from shaura_core.interfaces import\
    IObjectCreatedEvent, IObjectModifiedEvent, IObjectObsoletedEvent


class ObjectCreatedEvent(object):
    """Object created lifecycle event"""
    implements(IObjectCreatedEvent)

    def __init__(self, target):
        self.target = target


class ObjectModifiedEvent(object):
    """Object modified lifecycle event"""
    implements(IObjectModifiedEvent)

    def __init__(self, target):
        self.target = target


class ObjectObsoletedEvent(object):
    """Object obsoleted lifecycle event"""
    implements(IObjectObsoletedEvent)

    def __init__(self, target):
        self.target = target

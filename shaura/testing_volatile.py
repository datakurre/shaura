# -*- coding: utf-8 -*-
"""Dummy volatile storage for testing purposes"""

from zope.interface import implements

from pyramid.threadlocal import get_current_registry

from shaura_core.interfaces import IObjectManager
from shaura_core.events import\
    ObjectCreatedEvent, ObjectModifiedEvent, ObjectObsoletedEvent
from shaura.interfaces import IUnique

DATASTORE = {}


class ObjectManager(object):
    """Database access utility"""
    implements(IObjectManager)

    def __call__(self, **kwargs):
        klass = None
        try:
            klass = kwargs.pop("object_type")
        except KeyError:
            pass

        for result in DATASTORE.get(klass, {}).values():
            yield result

    def add(self, obj):
        """Add object to datastore"""
        registry = get_current_registry()
        event = ObjectCreatedEvent(obj)
        registry.notify(event)

    def update(self, obj):
        """Update object on datastore"""
        registry = get_current_registry()
        event = ObjectModifiedEvent(obj)
        registry.notify(event)

    def delete(self, obj):
        """Delete object from datastore"""
        registry = get_current_registry()
        event = ObjectObsoletedEvent(obj)
        registry.notify(event)


def putCreatedObject(event):
    """Object created lifecycle event"""
    klass = event.target.__class__.__name__
    uuid = IUnique(event.target).uuid
    if not klass in DATASTORE:
        DATASTORE[klass] = {}
    DATASTORE[klass][uuid] = event.target


def deleteObsoletedObject(event):
    """Object obsoleted lifecycle event"""
    klass = event.target.__class__.__name__
    uuid = IUnique(event.target).uuid
    del DATASTORE[klass][uuid]

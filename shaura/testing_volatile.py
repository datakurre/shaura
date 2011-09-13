# -*- coding: utf-8 -*-
"""Dummy volatile storage for testing purposes"""

from zope.interface import implements

from shaura_core.interfaces import IObjectManager
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

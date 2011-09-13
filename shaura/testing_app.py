# -*- coding: utf-8 -*-
"""Dummy app for testing purposes"""

from zope import schema
from zope.interface import Interface, implements

from shaura_core.interfaces import IObject

from shaura.interfaces import IUnique, ICollection
from shaura.collections import Collection


class IApplication(Interface):
    """Root object factory"""

    def __init__(request):
        pass

    def __getitem__(key):
        pass


class Application(object):
    """Root object factory"""
    implements(IApplication)

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        """Looks up for named collection multiadapters to find
        some children for this non-persistent root object"""
        registry = self.request.registry
        try:
            return registry.getAdapter(self, ICollection, name=key)
        except:
            raise KeyError(key)


class ITask(Interface):
    """Simple task"""

    title = schema.TextLine(
        title=u"Title",
        required=True
        )

    due_date = schema.Datetime(
        title=u"Due date",
        required=False
        )


class Task(object):
    """Simple task"""
    implements(IObject, IUnique, ITask)

    def __init__(self, uuid=None, title=None, due_date=None):
        self.uuid = uuid
        self.title = title
        self.due_date = due_date


class Tasks(Collection):
    """Collection multi adapter for tasks"""
    object_class = Task

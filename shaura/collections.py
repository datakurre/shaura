# -*- coding: utf-8 -*-
"""Generic collection views and actions"""

from uuid import uuid4 as uuid

from zope.interface import implements

# See: http://docs.pylonsproject.org/projects/pyramid/dev/api/httpexceptions.html
from pyramid import httpexceptions
from pyramid.threadlocal import get_current_registry

from shaura.interfaces import ICollection, IUnique
from shaura_core.interfaces import IObjectManager
from shaura.response import Created

from shaura_json import utils as json


class Collection(object):
    """Collection adapter base for a content type"""
    implements(ICollection)

    object_class = None

    def __init__(self, context):
        self.context = context

    def __iter__(self):
        registry = get_current_registry()
        manager = registry.getUtility(IObjectManager)
        object_type = self.object_class.__name__
        for item in manager(object_type=object_type):
            yield item

    def __getitem__(self, uuid):
        registry = get_current_registry()
        manager = registry.getUtility(IObjectManager)
        object_type = self.object_class.__name__
        results = manager(object_type=object_type, uuid=uuid)
        try:
            return results.next()
        except StopIteration:
            raise KeyError


def add(context, request):
    # parse JSON data from the request and create object
    try:
        values = json.decode(request.params.get("data", None),
                             target_class=context.object_class)
        obj = context.object_class(**values)
    except:
        raise httpexceptions.HTTPBadRequest()

    manager = request.registry.getUtility(IObjectManager)
    manager.add(obj)

    return Created("%s/%s" % (request.url, IUnique(obj).uuid))


def list(context, request):
    return [IUnique(obj).uuid for obj in context]


def get(context, request):
    return json.values(context)


def setUniqueId(event):
    if IUnique.providedBy(event.target):
        # genrate UUID for new object
        IUnique(event.target).uuid = unicode(uuid())
        # update object on datastore to save UUID
        registry = get_current_registry()
        manager = registry.getUtility(IObjectManager)
        manager.update(event.target)

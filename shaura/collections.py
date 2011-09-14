# -*- coding: utf-8 -*-
"""Generic collection views and actions"""

from uuid import uuid4 as uuid

from zope.interface import implements
from zope.schema import getFieldNamesInOrder

# See: http://docs.pylonsproject.org/projects/pyramid/dev/api/httpexceptions.html
from pyramid import httpexceptions
from pyramid.threadlocal import get_current_registry

from shaura.interfaces import ICollection, ICollectable
from shaura_core.interfaces import IObjectManager
from shaura.response import Ok, Created

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


def list(context, request):
    return [ICollectable(obj).uuid for obj in context]


def create(context, request):
    # parse JSON data from the request and create object
    try:
        values = json.decode(request.params.get("data", None),
                             target_class=context.object_class)
        obj = context.object_class(**values)
    except:
        raise httpexceptions.HTTPBadRequest()

    manager = request.registry.getUtility(IObjectManager)
    manager.add(obj)

    return Created("%s/%s" % (request.url, ICollectable(obj).uuid))


def read(context, request):
    return json.values(context)


def update(context, request):
    # parse JSON data from the request
    try:
        values = json.decode(request.params.get("data", None), context)
    except:
        raise httpexceptions.HTTPBadRequest()

    # drop uuid from values
    if "uuid" in values:
        values.pop("uuid")

    # iterate through schema and update fields
    for interface in context.__provides__.interfaces():
        for name in getFieldNamesInOrder(interface):
            if name in values:
                field = interface[name].bind(context)
                field.validate(values[name])
                field.set(context, values[name])

    manager = request.registry.getUtility(IObjectManager)
    manager.update(context)

    return json.values(context)


def delete(context, request):
    manager = request.registry.getUtility(IObjectManager)
    manager.delete(context)

    return Ok()


def setUniqueId(event):
    if ICollectable.providedBy(event.target):
        # generate UUID for the (created) target object
        ICollectable(event.target).uuid = unicode(uuid())

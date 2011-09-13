# -*- coding: utf-8 -*-
"""Base interfaces and schemas"""

from zope import schema
from zope.interface import Interface

from shaura_core.interfaces import IObject

from zope.i18nmessageid import MessageFactory as ZopeMessageFactory
_ = ZopeMessageFactory("shaura")


class IUnique(Interface):
    """Universally unique identifier for an object"""

    uuid = schema.ASCIILine(
        title=_("generic_uuid",
                default="Unique identifier"),
        readonly=True,
        required=False  # should be set by an event
        )


class ICollection(Interface):
    """Collections support RESTful GET (list) and POST (create)"""

    object_class = schema.Object(
        title=_("object_class",
                default="Collection's content objects' class"),
        schema=IObject,
        required=True
        )

    def __iter__():
        """Returns iterator for the collection"""
        pass

    def __getitem__(key):
        """Return the item with requested key from the collection"""
        pass

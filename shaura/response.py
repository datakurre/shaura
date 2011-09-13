# -*- coding: utf-8 -*-
"""Basic responses"""

from zope.interface import implements

from pyramid.interfaces import IResponse


class Response(object):
    """May be faster than webob.Response"""
    implements(IResponse)

    status = "200 OK"

    def __init__(self, body, content_type="text/html"):
        self.app_iter = [body]
        self.headerlist = [("Content-Type", content_type),
                           ("Content-Length", str(len(body)))]

    def __call__(self, environ, start_response):
        """WSGI application interface"""
        start_response(self.status, self.headerlist)
        if environ["REQUEST_METHOD"] == "HEAD":
            return []
        else:
            return self.app_iter


class Created(Response):
    status = "201 CREATED"

    def __init__(self, location):
        super(Created, self).__init__(str(), content_type="text/html")
        self.headerlist.append(("Location", location))

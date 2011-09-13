# -*- coding: utf-8 -*-
"""zope.testrunner layers"""

from pyramid import testing


class PyramidLayer(object):

    @classmethod
    def setUp(cls):
        cls.config = testing.setUp()

        import pyramid_zcml
        cls.config.include(pyramid_zcml)
        cls.config.load_zcml("shaura:configure.zcml")

    @classmethod
    def tearDown(cls):
        testing.tearDown()

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


from shaura import testing_volatile


class VolatileLayer(PyramidLayer):

    @classmethod
    def setUp(cls):
        cls.config.load_zcml("shaura:testing_volatile.zcml")

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        testing_volatile.DATASTORE.clear()

    @classmethod
    def testTearDown(cls):
        pass


from shaura import testing_app


class VolatileAppLayer(VolatileLayer):

    @classmethod
    def setUp(cls):
        cls.config.load_zcml("shaura:testing_app.zcml")
        cls.config._set_root_factory(testing_app.Application)

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass

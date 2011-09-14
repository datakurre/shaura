# -*- coding: utf-8 -*-
"""Integration tests"""

import unittest2 as unittest
from corejet.core import Scenario, story, scenario, given, when, then

from zope.testbrowser import wsgi
from shaura.testing import VolatileAppLayer


@story(id="18123073", title=u"As user I want to store tasks")
class As_user_I_want_to_store_tasks(unittest.TestCase):

    layer = VolatileAppLayer

    def redo(self, name):
        index = [s.name for s in self.scenarios].index(name)
        scenario = self.scenarios[index]
        for clause in scenario.givens + scenario.whens + scenario.thens:
            clause(self)

    def setUp(self):
        self.browser = wsgi.Browser(wsgi_app=self.layer.config.make_wsgi_app())

    @scenario(u"POST a new task")
    class POST_a_new_task(Scenario):

        @given(u"There's a collection for tasks defined at '/task'")
        def Theres_a_collection_for_tasks_defined_at_task(self):
            import simplejson
            self.browser.open("http://localhost/tasks")
            self.assertEquals(simplejson.loads(self.browser.contents), [])

        @given(u"I've got a new task described in JSON")
        def Ive_got_a_new_task_described_in_JSON(self):
            import simplejson
            self.task = {
                "title": u"Do something",
                "due_date": u"2011-12-24T00:00:00Z"
            }
            self.task_json = simplejson.dumps(self.task)

        @when(u"I POST that task to '/tasks'")
        def I_POST_that_task_to_tasks(self):
            from urllib2 import quote
            self.browser.post("http://localhost/tasks",
                              "data=%s" % quote(self.task_json))

        @then(u"I get a response with location for the posted task")
        def I_get_a_response_with_location_for_the_posted_task(self):
            self.assertEquals(self.browser.headers["Status"], "201 CREATED")
            self.assertIn("location", self.browser.headers)

    @scenario(u"GET a list of all tasks")
    class GET_a_list_of_all_tasks(Scenario):

        @given(u"I've posted a new task onto the collection at '/tasks'")
        def Ive_posted_a_new_task_onto_the_collection_at_tasks(self):
            self.redo(u"POST a new task")
            self.task_uri = self.browser.headers["location"]
            self.task_uuid = self.task_uri.split("/")[-1]

        @when(u"I GET '/tasks'")
        def I_GET_tasks(self):
            self.browser.open("http://localhost/tasks")

        @then(u"The results include the UUID of my task")
        def The_results_include_the_UUID_of_my_task(self):
            import simplejson
            self.assertIn(
                self.task_uuid, simplejson.loads(self.browser.contents))

    @scenario(u"GET a posted task")
    class GET_a_posted_task(Scenario):

        @given(u"I've POSTed a new task onto the collection at '/tasks'")
        def Ive_POSTed_a_new_task_onto_the_collection_at_tasks(self):
            self.redo(u"POST a new task")
            self.task["uuid"] =\
                self.browser.headers["location"].split("/")[-1]

        @when(u"I GET the URI of my task")
        def I_GET_the_URI_of_my_task(self):
            self.browser.open(self.browser.headers["location"])

        @then(u"I get a JSON dump of my task")
        def I_get_a_JSON_dump_of_my_task(self):
            import simplejson
            self.assertEquals(
                self.task, simplejson.loads(self.browser.contents))

    @scenario(u"PUT a new version of task")
    class PUT_a_new_version_of_task(Scenario):

        @given(u"I've got a JSON dump of my task")
        def Ive_got_a_JSON_dump_of_my_task(self):
            self.redo(u"GET a posted task")
            self.task_json = self.browser.contents

        @when(u"I modify that JSON")
        def I_modify_that_JSON(self):
            import simplejson
            self.task = simplejson.loads(self.task_json)
            self.task.update({
                "title": u"Do something else",
                "due_date": u"2012-12-24T00:00:00Z"
            })
            self.task_json = simplejson.dumps(self.task)

        @when(u"I PUT that JSON back to its URI")
        def I_PUT_that_JSON_back_to_its_URI(self):
            from urllib2 import quote
            self.browser.post(
                "http://localhost/tasks/%s/put" % self.task["uuid"],
                "data=%s" % quote(self.task_json))

        @when(u"I GET that URI again")
        def I_GET_that_URI_again(self):
            self.browser.open("http://localhost/tasks/%s" % self.task["uuid"])

        @then(u"I get an updated JSON dump of my task")
        def I_get_an_updated_JSON_dump_of_my_task(self):
            import simplejson
            self.assertEquals(
                self.task, simplejson.loads(self.browser.contents))

    @scenario(u"DELETE a task")
    class DELETE_a_task(Scenario):

        @given(u"I've POSTed a new task onto the collection at '/tasks'")
        def Ive_POSTed_a_new_task_onto_the_collection_at_tasks(self):
            self.redo(u"POST a new task")

        @when(u"I GET the URI of my task")
        def I_GET_the_URI_of_my_task(self):
            self.uri = self.browser.headers["location"]

        @when(u"I DELETE that URI")
        def I_DELETE_that_URI(self):
            self.browser.post("%s/delete" % self.uri, "")

        @when(u"I GET '/tasks'")
        def I_GET_tasks(self):
            self.browser.open("http://localhost/tasks")

        @then(u"The results don't include the UUID of my task")
        def The_results_dont_include_the_UUID_of_my_task(self):
            import simplejson
            self.assertEquals(simplejson.loads(self.browser.contents), [])

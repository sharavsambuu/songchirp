#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2, os
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	path = os.path.join(os.path.dirname(__file__), '../views' ,'index.html')
    	template_values = {
    	}
    	self.response.write(
        	template.render(path, template_values)
        	)

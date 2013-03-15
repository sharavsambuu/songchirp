# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Music(db.Model):
	sourceType = db.StringProperty(required=True, choices=set(["youtube", "soundcloud", "vimeo", "mp3"]))
	name   = db.StringProperty(required=True)
	source = db.TextProperty(required=True)
	play_count = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)



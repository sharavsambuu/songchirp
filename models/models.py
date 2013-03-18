# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Music(db.Model):
	sourceType = db.StringProperty(required=True, choices=set(["youtube", "soundcloud", "vimeo", "mp3"]))
	name   = db.StringProperty(required=True)
	source = db.TextProperty(required=True)
	broken_report_count = db.IntegerProperty()
	play_count = db.IntegerProperty()
	date = db.DateTimeProperty(auto_now_add=True)

class MusicQueue(db.Model):
	music_list = db.ListProperty(long)
	date = db.DateTimeProperty(auto_now_add=True)



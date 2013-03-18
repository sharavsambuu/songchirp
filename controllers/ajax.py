#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2, json, logging
from models.models import *
import random
#from google.appengine.api import memcache

class AddMusicHandler(webapp2.RequestHandler):
    def post(self):
    	sourceType = str(self.request.get('type'))
    	name = str(self.request.get('name'))
    	source = str(self.request.get('source'))
        logging.warning("type : %s", sourceType)
        logging.warning("name : %s", name)
        logging.warning("source : %s", source)
    	dat = Music(
            sourceType = str(self.request.get('type')),
            name = str(self.request.get('name')),
            source = str(self.request.get('source')),
            play_count = 0
            )
    	dat.put()
        #memcache.set(str(dat.key().id()), dat)
        result = []
        result.append({
                'id': str(dat.key().id())
            });
        json_string = json.dumps(result)
        self.response.write(json_string)

class SearchMusicHandler(webapp2.RequestHandler):
    def post(self):
        searchValue = str(self.request.get('searchValue'))
        q = Music.all().filter('name >=', searchValue).filter('name <', searchValue+u'\uFFFD')
        #q.filter('name =', searchValue)
        #q.order("-date")
        fetched = q.fetch(10)
        result = []
        for p in fetched:
            result.append({
                'id':str(p.key().id()),
                'type':p.sourceType,
                'name':p.name,
                'source':p.source,
                'play_count':p.play_count,
                'report_count':p.broken_report_count,
                'date':str(p.date)
                })
        json_string = json.dumps(result)
        self.response.write(json_string)
        pass

class GetMusicListHandler(webapp2.RequestHandler):
    def get(self):
        q = Music.all()
        q.order("-date")
        fetched = q.fetch(10)
        result = []
        for p in fetched:
            result.append({
                'id':str(p.key().id()),
                'type':p.sourceType,
                'name':p.name,
                'source':p.source,
                'play_count':p.play_count,
                'date':str(p.date)
                })
        json_string = json.dumps(result)
        self.response.write(json_string)

class GetMusicHandler(webapp2.RequestHandler):
    def post(self):
        entity_id= str(self.request.get('id'))
        #p = memcache.get(entity_id)
        #if p is None:
        #    p = Music.get_by_id(int(entity_id))
        p = Music.get_by_id(int(entity_id))
        p.play_count += 1
        p.put()
        #memcache.set(str(p.key().id()), p)
        result = []
        result.append({
                'id':str(p.key().id()),
                'type':p.sourceType,
                'name':p.name,
                'source':p.source,
                'play_count':p.play_count,
                'date':str(p.date)
                })
        json_string = json.dumps(result)
        self.response.write(json_string)

class DeleteMusicHandler(webapp2.RequestHandler):
    def post(self):
        entity_id= str(self.request.get('id'))
        p = Music.get_by_id(int(entity_id))
        p.delete()
        result = []
        json_string = json.dumps(result)
        self.response.write(json_string)

class NextMusicHandler(webapp2.RequestHandler):
    def get(self):
        query = Music.all(keys_only=True)
        selected_key = None
        n = 0
        for key in query:
            if random.randint(0, n)==0:
                selected_key = key
            n += 1

        p = None
        if selected_key is None:
            local_query = Music.all()
            results = local_query.fetch(1)
            for result in results:
                p = result
        else:
            p = Music.get(selected_key)

        result = []
        result.append({
                'id':str(p.key().id())
                })
        json_string = json.dumps(result)
        self.response.write(json_string)

class BrokenMusicHandler(webapp2.RequestHandler):
    def post(self):
        entity_id= str(self.request.get('id'))
        p = Music.get_by_id(int(entity_id))
        if p.broken_report_count is None:
            p.broken_report_count = 0
            p.put()    
        p.broken_report_count += 1
        p.put()
        #logging.warning("ID : %s, Count : %s", entity_id, str(p.broken_report_count))
        result = []
        result.append({
                'report_count':p.broken_report_count,
                })
        json_string = json.dumps(result)
        self.response.write(json_string)
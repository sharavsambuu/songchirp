#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2, json, logging
from models.models import *
import random

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
        result = []
        result.append({
                'id': str(dat.key().id())
            });
        json_string = json.dumps(result)
        self.response.write(json_string)

class GetMusicListHandler(webapp2.RequestHandler):
    def get(self):
        q = Music.all()
        q.order("-date")
        fetched = q.fetch(20)
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
        logging.warning("incoming ID : %s", entity_id)
        p = Music.get_by_id(int(entity_id))
        p.play_count += 1
        p.put()
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
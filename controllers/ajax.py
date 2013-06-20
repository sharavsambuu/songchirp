#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2, json, logging
from models.models import *
import random
import gdata.youtube
import gdata.youtube.service
from pyechonest import config
config.ECHO_NEST_API_KEY=""
from pyechonest import playlist
from pyechonest import artist
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

class TotalNumberofSongsHandler(webapp2.RequestHandler):
    def get(self):
        count = Music.all(keys_only=True).count()
        self.response.write(str(count))

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


class GenerateQueueHandler(webapp2.RequestHandler):
    def get(self):
        query = Music.all(keys_only=True)
        music_list = []
        for i in range(0,20):
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
            music_list.append(p.key().id())
        queue = MusicQueue(music_list = music_list)
        queue.put()
        pass
    def post(self):
        query = Music.all(keys_only=True)
        music_list = []
        for i in range(0,20):
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
            music_list.append(p.key().id())
        queue = MusicQueue(music_list = music_list)
        queue.put()
        pass

class GetRandomQueueHandler(webapp2.RequestHandler):
    def get(self):
        query = MusicQueue.all(keys_only=True)
        selected_key = None
        n = 0
        for key in query:
            if random.randint(0, n)==0:
                selected_key = key
            n += 1
        p = None
        if selected_key is None:
            local_query = MusicQueue.all()
            results = local_query.fetch(1)
            for result in results:
                p = result
        else:
            p = MusicQueue.get(selected_key)
        temp_music_list = []
        for i in p.music_list:
            temp_music_list.append(str(i))
        result = []
        result.append({
                'music_list': temp_music_list
            });
        json_string = json.dumps(result)
        self.response.write(json_string)
        pass
    pass
        
class SearchYoutubeHandler(webapp2.RequestHandler):
    def post(self):
        search_value= str(self.request.get('searchValue'))
        #query.vq = search_value
        #query.max_results = 1
        #query.start_index = 1
        #query.racy = "exclude"
        #query.format = "5"
        #query.orderby = "relevance"
        #feed = client.YouTubeQuery(query)
        #for entry in feed.entry:
        #    logging.warning(entry.GetSwfUrl())
        #logging.warning(search_value)
    
        #p = playlist.Playlist(type='artist-radio', artist=search_value)
        #if p is None:
        #    logging.warning("Cannot create playlist")        
        #sid = p.session_id
        #song = p.get_next_songs()
        #youtube_search_string = str(song.artist_name)+" - "+str(song.title)
        #youtube_search_string = search_value
        
        yt_service = gdata.youtube.service.YouTubeService()
        yt_service.ssl = False
        #query = gdata.youtube.service.YouTubeVideoQuery()
        #query.vq = youtube_search_string
        #query.orderby = 'relevance' # might want to change this
        #query.racy = 'include' # feelin' racy
        #feed = yt_service.YouTubeQuery(query)
        
        #result = feed.entry[0]
        #embed_url = result.split("&")[0].replace("watch?v=","v/")
        #embed_url = result.GetSwfUrl()
        
        p = playlist.static(type="artist-radio", artist=search_value)
        songs = []
        for song in p:
            #query = gdata.youtube.service.YouTubeVideoQuery()
            #query.vq = song.artist_name+" - "+song.title
            #query.orderby = 'relevance'
            #query.racy = 'include'
            #feed = yt_service.YouTubeQuery(query)
            #result = feed.entry[0]
            #embed_url = result.GetSwfUrl()
            songs.append({"artist":song.artist_name,"title":song.title})

        ajaxresult = []
        ajaxresult.append({
                'songs' : songs
            });
        json_string = json.dumps(ajaxresult)
        self.response.write(json_string)

class TestCronHandler(webapp2.RequestHandler):
    def get(self):
        logging.warning("Test CRON is WORKING from get")
        pass
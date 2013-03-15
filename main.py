#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from controllers import mainhandle, ajax

app = webapp2.WSGIApplication([
    ('/', mainhandle.MainHandler),
    ('/addMusic', ajax.AddMusicHandler),
    ('/getMusicList', ajax.GetMusicListHandler),
    ('/getMusic', ajax.GetMusicHandler),
    ('/deleteMusic', ajax.DeleteMusicHandler),
    ('/nextMusic', ajax.NextMusicHandler)
], debug=True)


# http://tutorialzine.com/2011/01/google-appengine-series/
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# API for D&B TV
# Version 1.0.0
#------------------------------------------------------------

import os
import sys
import urlparse
import plugintools
import jsontools
import urllib
from item import Item

def get_base_url():
    return "http://www.dandbtv.co.uk/dandb/api/"

# ---------------------------------------------------------------------------------------------------------
#  Core
# ---------------------------------------------------------------------------------------------------------
def get_json_response(service,parameters):
    plugintools.log("dandb.api.get_json_response service="+service+", parameters="+repr(parameters))

    # Service call
    s = plugintools.get_setting("token")
    parameters["s"] = s
    service_url = urlparse.urljoin(get_base_url(),service)
    plugintools.log("dandb.api.get_json_response service_url="+service_url)
    service_parameters = urllib.urlencode(parameters)
    plugintools.log("dandb.api.get_json_response parameters="+service_parameters)
    try:
        body , response_headers = plugintools.read_body_and_headers( service_url , post=service_parameters )
    except:
        import traceback
        plugintools.log("dandb.api.get_json_response "+traceback.format_exc())

    json_response = jsontools.load_json(body)

    return json_response

def get_itemlist_response(service,parameters,is_folder=True):
    plugintools.log("dandb.api.get_itemlist_response service="+service+", parameters="+repr(parameters))

    json_response = get_json_response(service,parameters)

    itemlist = []
    if not json_response['error']:
        for entry in json_response['body']:
            item = Item( title=entry['title'] )

            if 'plot' in entry:
                item.plot = entry['plot']
            else:
                item.plot = ""

            if 'thumbnail' in entry and entry['thumbnail'] is not None and entry['thumbnail']<>"":
                item.thumbnail = entry['thumbnail']

            else:
                item.thumbnail = os.path.join( plugintools.get_runtime_path() , "icon.png" )

            if 'fanart' in entry and entry['fanart'] is not None and entry['fanart']<>"":
                item.fanart = entry['fanart']
            else:
                item.fanart = ""

            if 'action' in entry:
                item.action = entry['action']
            else:
                item.action = "play"

            if 'url' in entry:
                item.url = entry['url']
            elif 'id' in entry:
                item.url = entry['id']
            else:
                item.url = entry['title']

            item.folder = is_folder

            itemlist.append( item )

    return itemlist

# ---------------------------------------------------------------------------------------------------------
#  Users
# ---------------------------------------------------------------------------------------------------------

def users_login(username,password):
    json_response = get_json_response("users/login.php",{'u':username,'p':password})

    if not json_response['error']:
        return json_response['body']['s']
    else:
        return ""

# ---------------------------------------------------------------------------------------------------------
#  Navigation
# ---------------------------------------------------------------------------------------------------------

def navigation_get_all(action,num_page,per_page):
    json_response = get_json_response("navigation/get_all.php",{'action':action,'num_page':num_page,'per_page':per_page})

    itemlist = []
    if not json_response['error']:
        for entry in json_response['body']:
            item = Item( title=entry['title'] )

            item.plot = entry['plot']
            item.thumbnail = entry['thumbnail']
            item.fanart = entry['fanart']
            item.command_type = entry['command_type']
            item.command = entry['command']
            item.file_url = entry['file_url']

            if item.command=="" and item.file_url!="":
                plugintools.log("dandb.api.navigation_get_all Detected an action_download")
                item.action = "action_download"
                item.folder = False
            elif item.command!="" and item.file_url=="":
                plugintools.log("dandb.api.navigation_get_all Detected an action_execute")
                item.action = "action_execute"
                item.folder = False
            elif item.command!="" and item.file_url!="":
                plugintools.log("dandb.api.navigation_get_all Detected an action_download_and_execute")
                item.action = "action_download_and_execute"
                item.folder = False
            else:
                item.folder = True

                import navigation
                if hasattr(navigation, entry['action']):
                    plugintools.log("dandb.api.navigation_get_all Found function "+entry['action']+" on navigation")
                    item.action = entry['action']
                    item.url = entry['url']
                else:
                    plugintools.log("dandb.api.navigation_get_all Function "+entry['action']+" not found on navigation, default navigation assumed")
                    item.action = 'get_navigation'
                    item.url = entry['action']


            itemlist.append( item )

    return itemlist

# ---------------------------------------------------------------------------------------------------------
#  Movies
# ---------------------------------------------------------------------------------------------------------

def movies_get_releases(num_page,per_page):
    return get_itemlist_response("movies/get_releases.php",{'num_page':num_page,'per_page':per_page},is_folder=False)

def movies_get_latest(num_page,per_page):
    return get_itemlist_response("movies/get_latest.php",{'num_page':num_page,'per_page':per_page},is_folder=False)

def movies_get_genres():

    itemlist = get_itemlist_response("movies/get_genres.php",{})
    
    for item in itemlist:
        item.action = "movies_get_by_genre"

    return itemlist

def movies_get_by_genre(num_page,per_page,genre):
    return get_itemlist_response("movies/get_by_genre.php",{'genre':genre,'num_page':num_page,'per_page':per_page},is_folder=False)

def movies_get_letters():
    itemlist = get_itemlist_response("movies/get_letters.php",{})

    for item in itemlist:
        item.action = "movies_get_by_letter"

    return itemlist

def movies_get_by_letter(num_page,per_page,letter):
    return get_itemlist_response("movies/get_by_letter.php",{'letter':letter,'num_page':num_page,'per_page':per_page},is_folder=False)

def movies_search(num_page,per_page,q):
    return get_itemlist_response("movies/search.php",{'q':q,'num_page':num_page,'per_page':per_page},is_folder=False)

# ---------------------------------------------------------------------------------------------------------
#  Series
# ---------------------------------------------------------------------------------------------------------

def series_get_releases(num_page,per_page):
    itemlist = get_itemlist_response("series/get_releases.php",{'num_page':num_page,'per_page':per_page})
    
    for item in itemlist:
        item.action = "series_get_episodes"

    return itemlist

def series_get_latest(num_page,per_page):
    itemlist = get_itemlist_response("series/get_latest.php",{'num_page':num_page,'per_page':per_page})
    
    for item in itemlist:
        item.action = "series_get_episodes"

    return itemlist

def series_get_updated(num_page,per_page):
    itemlist = get_itemlist_response("series/get_updated.php",{'num_page':num_page,'per_page':per_page})
    
    for item in itemlist:
        item.action = "series_get_episodes"

    return itemlist

def series_get_genres():

    itemlist = get_itemlist_response("series/get_genres.php",{})
    
    for item in itemlist:
        item.action = "series_get_by_genre"

    return itemlist

def series_get_by_genre(num_page,per_page,genre):
    itemlist = get_itemlist_response("series/get_by_genre.php",{'genre':genre,'num_page':num_page,'per_page':per_page})
    
    for item in itemlist:
        item.action = "series_get_episodes"

    return itemlist

def series_get_letters():
    itemlist = get_itemlist_response("series/get_letters.php",{})

    for item in itemlist:
        item.action = "series_get_by_letter"

    return itemlist

def series_get_by_letter(num_page,per_page,letter):
    itemlist = get_itemlist_response("series/get_by_letter.php",{'letter':letter,'num_page':num_page,'per_page':per_page})
    
    for item in itemlist:
        item.action = "series_get_episodes"

    return itemlist

def series_search(num_page,per_page,q):
    itemlist = get_itemlist_response("series/search.php",{'q':q,'num_page':num_page,'per_page':per_page})
    
    for item in itemlist:
        item.action = "series_get_episodes"

    return itemlist

def series_get_episodes(num_page,per_page,id_serie,id_season):
    return get_itemlist_response("series/get_episodes.php",{'id_serie':id_serie,'id_season':id_season,'num_page':num_page,'per_page':per_page},is_folder=False)

# ---------------------------------------------------------------------------------------------------------
#  Live
# ---------------------------------------------------------------------------------------------------------

def live_get_all(num_page,per_page):
    return get_itemlist_response("live/get_all.php",{'num_page':num_page,'per_page':per_page},is_folder=False)

def live_get_genres():

    itemlist = get_itemlist_response("live/get_genres.php",{})
    
    for item in itemlist:
        item.action = "live_get_by_genre"

    return itemlist

def live_get_by_genre(num_page,per_page,genre):
    return get_itemlist_response("live/get_by_genre.php",{'genre':genre,'num_page':num_page,'per_page':per_page},is_folder=False)

# ---------------------------------------------------------------------------------------------------------
#  Content
# ---------------------------------------------------------------------------------------------------------

def content_get_all(content_type,num_page,per_page):
    return get_itemlist_response("content/get_all.php",{'type':content_type,'num_page':num_page,'per_page':per_page},is_folder=False)

def content_get_genres(content_type):

    itemlist = get_itemlist_response("content/get_genres.php",{'type':content_type})
    
    for item in itemlist:
        item.action = content_type+"_get_by_genre"

    return itemlist

def content_get_by_genre(content_type,num_page,per_page,genre):
    return get_itemlist_response("content/get_by_genre.php",{'type':content_type,'genre':genre,'num_page':num_page,'per_page':per_page},is_folder=False)

# --------------------------------------------------------------------------------------------------------
#  Stream
# ---------------------------------------------------------------------------------------------------------
def stream_get(content_type,content_id,stream_version=""):
    json_body = get_json_response("stream/get.php",{'type':content_type,'id':content_id,'version':stream_version,'device_type':'xbmc'})

    itemlist = []
    if not json_body['error']:
        itemlist.append( Item( url=json_body['body']['url'] ) )

    return itemlist

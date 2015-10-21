# -*- coding: utf-8 -*-
#------------------------------------------------------------
# D&B TV
# Version 1.0.0
#------------------------------------------------------------

import os
import sys

import plugintools
import api
import urllib2 

# Main menu
def main_list(params):
    plugintools.log("dandb.main_list "+repr(params))

    if plugintools.get_setting("user")=="":
        settings(params)

    token = api.users_login( plugintools.get_setting("user") , plugintools.get_setting("password") )

    if token!="":
        plugintools.set_setting("token",token)
        import os
        itemlist = api.navigation_get_all("mainlist",0,1000)
        add_items_to_xbmc(params,itemlist)
    else:
        plugintools.message("D&B TV","Invalid login, check your account in add-on settings")

    import os
    plugintools.add_item( action="settings", title="Settings..." , folder=False )

    if token!="" and plugintools.get_setting("check_for_updates")=="true":
        import updater
        updater.check_for_updates()

    plugintools.set_view( plugintools.LIST )

# Settings dialog
def settings(params):
    plugintools.log("dandb.settings "+repr(params))
    plugintools.open_settings_dialog()

# Main menu
def get_navigation(params):
    plugintools.log("dandb.get_navigation "+repr(params))

    itemlist = api.navigation_get_all(params.get("url"),0,1000)
    add_items_to_xbmc(params,itemlist)

    plugintools.set_view( plugintools.LIST )

def action_download(params):
    plugintools.log("dandb.action_download "+repr(params))

    icon = os.path.join( plugintools.get_runtime_path() , "icon.png" )
    filename = plugintools.get_filename_from_url(params.get("file_url"))
    full_path_filename = os.path.join( plugintools.get_data_path() , filename )
    plugintools.download(params.get("file_url"),full_path_filename)

    plugintools.show_notification("D&B TV","File "+filename+"downloaded",icon)

def action_execute(params):
    plugintools.log("dandb.action_execute "+repr(params))

    icon = os.path.join( plugintools.get_runtime_path() , "icon.png" )

    if params.get("command_type")=="system":
        os.system(params.get("command"))
        plugintools.show_notification("D&B TV","Command executed",icon)

    elif params.get("command_type")=="xbmc":
        import xbmc
        xbmc.executebuiltin(params.get("command"))
        plugintools.show_notification("D&B TV","Command executed",icon)
    else:
        plugintools.show_notification("D&B TV","Command *NOT* executed",icon)

def action_download_and_execute(params):
    plugintools.log("dandb.action_download_and_execute "+repr(params))

    icon = os.path.join( plugintools.get_runtime_path() , "icon.png" )

    # Download file
    filename = plugintools.get_filename_from_url(params.get("file_url"))
    full_path_filename = os.path.join( plugintools.get_data_path() , filename )
    plugintools.download(params.get("file_url"),full_path_filename)
    plugintools.show_notification("D&B TV","File "+filename+"downloaded",icon)

    # Replace filename
    command = params.get("command")
    plugintools.log("dandb.action_download_and_execute command="+command)
    command = command.replace("$1",full_path_filename)
    plugintools.log("dandb.action_download_and_execute command="+command)

    # Execute command
    params["command"] = command
    action_execute(params)

# Live TV
def live_get_all(params):
    itemlist = api.live_get_all(0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def live_get_genres(params):
    itemlist = api.live_get_genres()
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def live_get_by_genre(params):
    itemlist = api.live_get_by_genre(0,1000,params.get("title"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)


# Music
def music_get_all(params):
    itemlist = api.content_get_all("music",0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def music_get_genres(params):
    itemlist = api.content_get_genres("music")
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def music_get_by_genre(params):
    itemlist = api.content_get_by_genre("music",0,1000,params.get("title"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)


# Radios
def radio_get_all(params):
    itemlist = api.content_get_all("radio",0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def radio_get_genres(params):
    itemlist = api.content_get_genres("radio")
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def radio_get_by_genre(params):
    itemlist = api.content_get_by_genre("radio",0,1000,params.get("title"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)


# Music videos
def musicvideo_get_all(params):
    itemlist = api.content_get_all("musicvideo",0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def musicvideo_get_genres(params):
    itemlist = api.content_get_genres("musicvideo")
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def musicvideo_get_by_genre(params):
    itemlist = api.content_get_by_genre("musicvideo",0,1000,params.get("title"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)




# Movies
def movies_get_latest(params):
    itemlist = api.movies_get_latest(0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.MOVIES)

def movies_get_releases(params):
    itemlist = api.movies_get_releases(0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.MOVIES)

def movies_get_genres(params):
    itemlist = api.movies_get_genres()
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def movies_get_by_genre(params):
    itemlist = api.movies_get_by_genre(0,1000,params.get("title"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.MOVIES)

def movies_get_letters(params):
    itemlist = api.movies_get_letters()
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def movies_get_by_letter(params):
    itemlist = api.movies_get_by_letter(0,1000,params.get("url"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.MOVIES)

def movies_search(params):
    q = plugintools.keyboard_input("", title="Text to search")
    itemlist = api.movies_search(0,1000,q)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.MOVIES)



# Series
def series_get_latest(params):
    itemlist = api.series_get_latest(0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.TV_SHOWS)

def series_get_releases(params):
    itemlist = api.series_get_releases(0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.TV_SHOWS)

def series_get_updated(params):
    itemlist = api.series_get_updated(0,1000)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.TV_SHOWS)

def series_get_genres(params):
    itemlist = api.series_get_genres()
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def series_get_by_genre(params):
    itemlist = api.series_get_by_genre(0,1000,params.get("title"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.TV_SHOWS)

def series_get_letters(params):
    itemlist = api.series_get_letters()
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.LIST)

def series_get_by_letter(params):
    itemlist = api.series_get_by_letter(0,1000,params.get("url"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.TV_SHOWS)

def series_search(params):
    q = plugintools.keyboard_input("", title="Text to search")
    itemlist = api.series_search(0,1000,q)
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.TV_SHOWS)

def series_get_episodes(params):
    itemlist = api.series_get_episodes(0,1000,params.get("url"),params.get("title"))
    add_items_to_xbmc(params,itemlist)
    plugintools.set_view(plugintools.TV_SHOWS)

# Resolve hoster links
def play(params):
    plugintools.log("dandb.play "+repr(params))

    #plugintools.set_view(plugintools.LIST)

    try:
        url = params.get("url")
        plugintools.log("dandb.play url="+repr(url))

        if url=="":
            return

        from urlresolver.types import HostedMediaFile
        hosted_media_file = HostedMediaFile(url=url)
        plugintools.log("dandb.play hosted_media_file="+repr(hosted_media_file))

        try:
            media_url = hosted_media_file.resolve()
            plugintools.log("dandb.play media_url="+repr(media_url))

            if media_url:
                #plugintools.add_item( action="playable", title="Play this video from "+hosted_media_file.get_host()+"", url=media_url, isPlayable=True, folder=False )
                plugintools.play_resolved_url( media_url )    
            else:
                plugintools.play_resolved_url( url )    
        except:
            import traceback
            plugintools.log(traceback.format_exc())
            #plugintools.add_item( action="play", title="Error while getting access to video", isPlayable=True, folder=False )
            plugintools.message("D&B TV","Error while getting access to video")

    except urllib2.URLError,e:
        #plugintools.add_item( action="play", title="Error reading data, please try again", isPlayable=True, folder=False )
        plugintools.message("D&B TV","Connection error while getting access to video")
        body = ""



def add_items_to_xbmc(params,itemlist):

    for item in itemlist:
        plugintools.log("item="+item.tostring())
        fanart = item.fanart
        if fanart=="":
            fanart = params.get("fanart")
        if fanart=="" or fanart is None:
            fanart = os.path.join( plugintools.get_runtime_path() , "fanart.jpg" )

        if item.folder:
            plugintools.add_item( title=item.title, plot=item.plot, url=item.url, action=item.action, thumbnail=item.thumbnail , fanart=fanart, folder=True )
        elif item.command!="" or item.file_url!="":
            plugintools.add_item( title=item.title, plot=item.plot, url=item.url, action=item.action, thumbnail=item.thumbnail , fanart=fanart, command_type=item.command_type, command=item.command, file_url=item.file_url, folder=False )
        else:
            plugintools.add_item( title=item.title, plot=item.plot, url=item.url, action=item.action, thumbnail=item.thumbnail , fanart=fanart, folder=False, isPlayable=True )

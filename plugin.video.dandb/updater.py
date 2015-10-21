# -*- coding: utf-8 -*-
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import plugintools
import xbmc

REMOTE_VERSION_FILE = "http://88.198.92.46/dandb/api/version.txt"
LOCAL_VERSION_FILE = os.path.join( plugintools.get_runtime_path() , "version.txt")

def check_for_updates():
    plugintools.log("dandb.updater checkforupdates")

    # Descarga el fichero con la versión en la web
    try:
        plugintools.log("dandb.updater remote_version_file="+REMOTE_VERSION_FILE)
        data = plugintools.read( REMOTE_VERSION_FILE )

        versiondescargada = data.splitlines()[0]
        urldescarga = data.splitlines()[1]
        plugintools.log("dandb.updater remote_version="+versiondescargada)
        
        # Lee el fichero con la versión instalada
        plugintools.log("dandb.updater local_version_file="+LOCAL_VERSION_FILE)
        infile = open( LOCAL_VERSION_FILE )
        data = infile.read()
        infile.close();

        versionlocal = data.splitlines()[0]
        plugintools.log("dandb.updater local_version="+versionlocal)

        if int(versiondescargada)>int(versionlocal):
            plugintools.log("dandb.updater update found")
            
            yes_pressed = plugintools.message_yes_no("D&B","There is an update available!","Do you want to install it?")

            if yes_pressed:
                try:
                    plugintools.log("dandb.updater Download file...")
                    local_file_name = os.path.join( plugintools.get_data_path() , "update.zip" )
                    urllib.urlretrieve(urldescarga, local_file_name )
            
                    # Lo descomprime
                    plugintools.log("dandb.updater Unzip file...")

                    import ziptools
                    unzipper = ziptools.ziptools()
                    destpathname = xbmc.translatePath( "special://home/addons")
                    plugintools.log("dandb.updater destpathname=%s" % destpathname)
                    unzipper.extract( local_file_name , destpathname )
                    
                    # Borra el zip descargado
                    plugintools.log("dandb.updater remove file...")
                    os.remove(local_file_name)
                    plugintools.log("dandb.updater ...file deleted")

                    xbmc.executebuiltin((u'XBMC.Notification("Updated", "D&B has been updated", 2000)'))
                    xbmc.executebuiltin( "Container.Refresh" )
                except:
                    xbmc.executebuiltin((u'XBMC.Notification("Not updated", "Update failed due to an error", 2000)'))

    except:
        import traceback
        plugintools.log(traceback.format_exc())

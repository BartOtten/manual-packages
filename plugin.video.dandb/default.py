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
import navigation

plugintools.application_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.module_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.http_debug_log_enabled = (plugintools.get_setting("debug")=="true")

# Entry point
def run():
    plugintools.log("dandb.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        navigation.main_list(params)
    else:
        action = params.get("action")
        plugintools.log("dandb."+action+" "+repr(params))
        exec "navigation."+action+"(params)"

    plugintools.close_item_list()

run()

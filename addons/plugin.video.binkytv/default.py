# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Binky TV special thanks to original authors of the code
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: Dandymedia
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.binkytv'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCbt63GNsB5wet6NO3dmhssA"
YOUTUBE_CHANNEL_ID_2 = "UCRXXQgZZsMIxXpFncK019DA"
YOUTUBE_CHANNEL_ID_3 = "UCLsooMJoIpl_7ux2jvdPB-Q"
YOUTUBE_CHANNEL_ID_4 = "UCIX0Z-09kLkf-96-StW3hAw"
YOUTUBE_CHANNEL_ID_5 = "UCbCmjCuTUZos6Inko4u57UQ"
YOUTUBE_CHANNEL_ID_6 = "UCZzfOkvfLKdKYEWAZ_Vc0zg"
YOUTUBE_CHANNEL_ID_7 = "UCMU_RNU6KR49ZE8KmOcpdnA"
YOUTUBE_CHANNEL_ID_8 = "UCn--vKxbXBYt_b0lKJ0JEnw"
YOUTUBE_CHANNEL_ID_9 = "UCcvkRvee98FqqUmXN_dwOUw"
YOUTUBE_CHANNEL_ID_10 = "UCBnZ16ahKA2DZ_T5W0FPUXg"
YOUTUBE_CHANNEL_ID_11 = "UCJkWoS4RsldA1coEIot5yDA"
YOUTUBE_CHANNEL_ID_12 = "UCwynFfAvCF2kiRSMWiozQHg"
YOUTUBE_CHANNEL_ID_13 = "UCU_If3OQp9FPHoP1BteFNlA"
YOUTUBE_CHANNEL_ID_14 = "UCbmw4dLid589QTC7xRi0DdA"
YOUTUBE_CHANNEL_ID_15 = "UCwOS0K6uKOqoAWU7MUEtxaQ"


# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="Busy Beavers",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-gB_SFlcGzDc/AAAAAAAAAAI/AAAAAAAAAAA/KwtbUnJTQTQ/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nursery Rhyme Street",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-iALq_ddya5I/AAAAAAAAAAI/AAAAAAAAAAA/xZ3XR3PkxuE/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Super Simple Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://cdn.shopify.com/s/files/1/0177/6170/products/sss1-cd_1_large.jpg?v=1357867121",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="TinySchool TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-GKF9gp5kPTA/AAAAAAAAAAI/AAAAAAAAAAA/RTTvkaJ4UyE/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ABCkidTV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51V8MrZu5TL._SY300_.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Toddler Fun Learning",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-CszZY89JGBA/AAAAAAAAAAI/AAAAAAAAAAA/1k3MQc5znAU/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="HooplaKidz Shows",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-R4Yt7fFk6A4/AAAAAAAAAAI/AAAAAAAAAAA/2tqwFduNGjw/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ShopkinsWorld",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-jPfU68yA4yo/AAAAAAAAAAI/AAAAAAAAAAA/BKo01shIosI/s500-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Binkie.TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-WhVgRo5IyXc/AAAAAAAAAAI/AAAAAAAAAAA/ZWaVblU-sdk/s500-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ChuChu TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-QHPC9emY_8c/AAAAAAAAAAI/AAAAAAAAAAA/03fPGkHcBbk/s500-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Mother Goose Club",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-CjtfMnhAf90/AAAAAAAAAAI/AAAAAAAAAAA/9x0cv1cw3-8/s500-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Kids Learning Videos",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-xy6rXhNqql0/AAAAAAAAAAI/AAAAAAAAAAA/YQB3DbpRdZ0/s500-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Kids Tv Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-co8gqPEZ4wg/AAAAAAAAAAI/AAAAAAAAAAA/ns5vMzc8vzM/s500-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Kids Live Shows",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-eqqPmAIvb7o/AAAAAAAAAAI/AAAAAAAAAAA/j9XSYw35IxY/s500-c-k-no/photo.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="Cartoon Candy",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-eDshGeqRoVg/AAAAAAAAAAI/AAAAAAAAAAA/ijrVpSZsWRk/s500-c-k-no/photo.jpg",
        folder=True )
				
run()		

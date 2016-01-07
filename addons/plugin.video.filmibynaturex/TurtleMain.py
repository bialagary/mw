'''
Created on Nov 20, 2012

@author: ajju
'''


try:
    import TurtlePlugin
except:
    import xbmcgui  # @UnresolvedImport
    dialog = xbmcgui.Dialog()
    dialog.ok('[B][COLOR red]ALERT: [/COLOR][/B] RESTART XBMC', 'A new update has recently installed or add-on reconfigured.', 'Please restart XBMC to reflect the changes.', 'You will not be able to access until restart.')

TurtlePlugin.start('plugin.video.filmibynaturex')

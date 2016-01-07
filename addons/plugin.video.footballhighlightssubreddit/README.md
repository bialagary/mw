/r/footballhighlights
=====================

An XBMC plugin that plays videos from reddit.com/r/footballhighlights

It supports videos hosted on Google Drive, Dailymotion, YouTube, and CloudyVideos



Installation
------------
1.  Download the the repo zip file from [here](https://bitbucket.org/surmac/surmac-xbmc-repo/raw/master/repo/repository.surmac/repository.surmac-1.0.0.zip)
2.  Navigate to System > Settings > Add-ons > Install from zip file > Navigate to the zip file on your system
3.  Navigate to System > Settings > Add-ons > Get Add-ons > surmac's repo > Video Add-ons > /r/footballhighlights > Install

Settings
--------
There are two ways to access this add-on's settings

1.  System > Settings > Add-ons > Enabled Add-ons > Video Add-ons > /r/footballhighlights > Configure
2.  Videos > Add-ons > Right click on /r/footballhighlights (or press "c" with it highlighted) > Add-on settings

### Maximum playback quality ###
This setting does not apply to CloudyVideos, as they are only available in the original upload format (usually 720p).

### Saved searches ###
Add custom searches for easy access. For example, "Sevilla, Europa League, World Cup" in saved searches would add each of those items to the add-on's startup screen. Search results are sorted by date.

### Enable DASH videos ###
Off by default, this tells the add-on whether to play [MPEG-DASH videos](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP), which cannot be played with audio. As YouTube currently uses DASH as its only 1080p format, with this setting turned off the add-on will prefer 720p with audio, over silent 1080p DASH video.
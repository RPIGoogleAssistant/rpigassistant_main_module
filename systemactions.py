import os
import time
import re

from rpitts import say
from mpvplayer import (
     mpvplayeradjustvolume, mpvplayerrestorevolume,
     mpvplayergetvolume, mpvplayersetvolume,
     mpvplayerstop, mpvplayercycle, mpvplayermute, mpvplayerunmute,
     mpvplayerskip
)
from gmusicplayer import stopgmusicplayer, updategmusiclibrary, updategmusicplaylistlibrary

#System power controls
#Shutdown reboot controls
def Action(phrase):
    if 'shut down' in phrase:
        say('Shutting down in 5 seconds')
        time.sleep(5)
        say('Shut down initiated')
        os.system("sudo shutdown -h now")
    elif ('reboot' in phrase) or ('restart' in phrase):
        say('Rebooting in 5 seconds')
        time.sleep(5)
        say('Reboot initiated')
        os.system("sudo reboot")
    else:
        say('Sorry I did not understand')

#System updates
#Update music library etc.
def systemupdateprocess():
    gmusiclibrayupdated=updategmusiclibrary()
    gmusicplaylistlibraryupdated=updategmusicplaylistlibrary()

#Playback volume controls
#Temporary adjustment for playback volume
#restore to previous value using restorevolume()
def adjustvolume(volumelevel):
    mpvplayeradjustvolume(volumelevel)

#Set volume permanently in mpvplayer.json
def setvolume(volumelevel):
    mpvplayersetvolume(volumelevel)

#Decrease volume permanently by value volumechange
def decreasevolume(volumechange):
    volumelevel=int(mpvplayergetvolume()) - int(volumechange)
    mpvplayersetvolume(str(volumelevel))

#Increase volume permanently by value volumechange
def increasevolume(volumechange):
    volumelevel=int(mpvplayergetvolume()) + int(volumechange)
    mpvplayersetvolume(str(volumelevel))

#restores volume from mpvplayer.json after being changed by adjustvolume()
def restorevolume():
    volumelevel=mpvplayergetvolume()
    mpvplayerrestorevolume(volumelevel)

#Parsing volume control query string
def getsystemvolumecontrolstring(querystring):
    volregexobj = re.match( r"{'text': '(increase|decrease|set) playback volume (to|by)?\s*((\d+)|maximum)?(.*)?'}", 
                  querystring, re.I|re.I|re.I)
    if volregexobj:
       return volregexobj.group(1),volregexobj.group(2),volregexobj.group(3)
    else:
       return None

#Calculating and setting volume from voice command string
def systemvolumecontrol(querystring):
    volumectrls=getsystemvolumecontrolstring(querystring)
    if volumectrls is not None:
       operation=volumectrls[0]
       operator=str(volumectrls[1])
       value=volumectrls[2]
       if value == 'None':
          value = '10'
       if value == 'maximum':
          value = '100'
       if (operator == 'to') or (operator == 'None'):
          setvolume(value)
       elif operator == 'by':
          if operation == 'set':
             setvolume(value)
          elif operation == 'increase':
             increasevolume(value)
          else:
             decreasevolume(value)
    else:
      say('Sorry you did not say the correct keywords')

#Playback play controls
def stopplayback():
    stopgmusicplayer()

def pauseplayback():
    mpvplayercycle()

def resumeplayback():
    mpvplayercycle()

def muteplayback():
    mpvplayermute()

def unmuteplayback():
    mpvplayerunmute()

#Track skipping
def skipplayback(skipby):
    mpvplayerskip(int(skipby))

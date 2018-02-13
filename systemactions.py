import os
import time
import re

from rpitts import say
from mpvplayer import (
     mpvplayeradjustvolume, mpvplayerrestorevolume,
     mpvplayergetvolume, mpvplayersetvolume,
     mpvplayerstop, mpvplayercycle, mpvplayermute, mpvplayerunmute
)
from gmusicplayer import stopgmusicplayer

#System actions Control
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

def adjustvolume(volumelevel):
    mpvplayeradjustvolume(volumelevel)

def setvolume(volumelevel):
    mpvplayersetvolume(volumelevel)

def decreasevolume(volumechange):
    volumelevel=int(mpvplayergetvolume()) - int(volumechange)
    mpvplayersetvolume(str(volumelevel))

def increasevolume(volumechange):
    volumelevel=int(mpvplayergetvolume()) + int(volumechange)
    mpvplayersetvolume(str(volumelevel))

def restorevolume():
    volumelevel=mpvplayergetvolume()
    mpvplayerrestorevolume(volumelevel)

def getsystemvolumecontrolstring(querystring):
    volregexobj = re.match( r"{'text': '(increase|decrease|set) playback volume (to|by)?\s*((\d+)|maximum)(.*)?'}", 
                  querystring, re.I|re.I|re.I)
    if volregexobj:
       return volregexobj.group(1),volregexobj.group(2),volregexobj.group(3)
    else:
       return None

def systemvolumecontrol(querystring):
    volumectrls=getsystemvolumecontrolstring(querystring)
    if volumectrls is not None:
       operation=volumectrls[0]
       operator=str(volumectrls[1])
       value=volumectrls[2]
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

#systemvolumecontrol("{'text': 'increase volume by 70 percent'}")
#systemvolumecontrol("{'text': 'decrease volume to 10 percent'}")
#systemvolumecontrol("{'text': 'decrease volume by 10 percent'}")
#systemvolumecontrol("{'text': 'set volume 10'}")
#systemvolumecontrol("{'text': 'decrease volume to 10'}")
#systemvolumecontrol("{'text': 'set volume to 10 percent'}")
#systemvolumecontrol("{'text': 'set volume to 10'}")

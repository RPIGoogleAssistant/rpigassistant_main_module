import os
import json
import re
import string

from threading import Thread

from rpitts import say
from gmusicplayer import playgmusicplaylist, updategmusiclibrary, stopgmusicplayer, creategmusicplaylist, generategmusicplaylist, searchgmusic

#Find loop playback or not
def getloopstatus(querystring):
   regexobj = (re.match( r"^((loop|shuffle)?\s*(and)?\s*(loop|shuffle))\s*(.*)", querystring, re.I))
   if regexobj:
      if (regexobj.group(2) == 'loop' or regexobj.group(4) == 'loop'):
          return True
      else:
          return False
   else:
      return False

#Find shuffle playback or not
def getshufflestatus(querystring):
   regexobj = (re.match( r"^((loop|shuffle)?\s*(and)?\s*(loop|shuffle)?)", querystring, re.I))
   if regexobj:
      if (regexobj.group(2) == 'shuffle' or regexobj.group(4) == 'shuffle'):
          return True
      else:
          return False
   else:
      return False

#Parse music query string and identify song, artist etc.
def parse_music_query(querystring):
    if (re.search( r"(.*)\s*play all (songs)$", querystring, re.I)):
       return 'PLAYALLSONGS',None,None,None
    elif (re.search( r"(.*)\s*play\s*(song|songs)?\s*(.*)?\s*(from)?\s*playlist (.*)$", querystring, re.I)):
          regexobj=re.search( r"(.*)\s*play\s*(song|songs)?\s*(.*)?\s*(from)?\s*playlist (.*)$", querystring, re.I)
          return regexobj.group(3),None,None,regexobj.group(5),None,None
    elif (re.search( r"(.*)\s*play\s*(songs)?\s*(from)?\s*station (.*)$", querystring, re.I)):
          regexobj=re.search( r"(.*)\s*play\s*(songs)?\s*(from)?\s*station (.*)$", querystring, re.I)
          return None,None,None,None,regexobj.group(4),None
    elif (re.search( r"(.*)\s*play\s*(from)?\s*podcast (.*)$", querystring, re.I)):
          regexobj=re.search( r"(.*)\s*play\s*(from)?\s*podcast (.*)$", querystring, re.I)
          return None,None,None,None,None,regexobj.group(3)
    elif (re.search(r"play\s*(song|songs)?\s*(.*)?\s*(by|of)\s*(artist)\s*(.*)\s*(from|in)\s*(album)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(song|songs)?\s*(.*)?\s*(by|of)\s*(artist)\s*(.*)\s*(from|in)\s*(album)\s*(.*)", querystring, re.I)
          return regexobj.group(2),regexobj.group(5),regexobj.group(8),None,None,None
    elif (re.search(r"play\s*(song|songs)?\s*(.*)?\s*(from|in)\s*(album)\s*(.*)\s*(by|of)\s*(artist)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(song|songs)?\s*(.*)?\s*(from|in)\s*(album)\s*(.*)\s*(by|of)\s*(artist)\s*(.*)", querystring, re.I)
          return regexobj.group(2),regexobj.group(8),regexobj.group(5),None,None,None
    elif (re.search(r"play\s*(song(s)?)\s*(.*)?\s*(from|in)\s*(album)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(song(s)?)\s*(.*)?\s*(from|in)\s*(album)\s*(.*)", querystring, re.I)
          return regexobj.group(3),None,regexobj.group(6),None,None,None
    elif (re.search(r"play\s*(song(s)?)\s*(.*)?\s*(by|of)\s*(artist)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(song(s)?)\s*(.*)?\s*(by|of)\s*(artist)\s*(.*)", querystring, re.I)
          return regexobj.group(3),regexobj.group(6),None,None,None,None
    elif (re.search(r"play\s*(album)\s*(.*)\s*(of|by)\s*(artist)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(album)?\s*(.*)\s*(of|by)\s*(artist)?\s*(.*)", querystring, re.I)
          return None,regexobj.group(5),regexobj.group(2),None,None,None
    elif (re.search(r"play\s*(artist)\s*(.*)\s*(from|in)\s*(album)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(artist)?\s*(.*)\s*(from|in)\s*(album)?\s*(.*)", querystring, re.I)
          return None,regexobj.group(2),regexobj.group(3),None,None,None
    elif (re.search(r"play\s*(album)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(album)\s*(.*)", querystring, re.I)
          return None,None,regexobj.group(2),None,None,None
    elif (re.search(r"play\s*(artist)\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(artist)\s*(.*)", querystring, re.I)
          return None,regexobj.group(2),None,None,None,None
    elif (re.search(r"play\s*(song(s)?)?\s*(.*)", querystring, re.I)):
          regexobj=re.search(r"play\s*(song(s)?)?\s*(.*)", querystring, re.I)
          return regexobj.group(3),None,None,None,None,None
    else:
          return None,None,None,None,None,None

#Update music library in database
def updatemedialibraries():
    medialibraryupdated=updategmusiclibrary()
    return medialibraryupdated

def playmedia(**kwargs):
    player = kwargs.get('player', 'gmusic')
    loop = kwargs.get('loop', False)
    shuffle = kwargs.get('shuffle', False)
    playgmusicplaylist(loop=loop,shuffle=shuffle)

#Stop media players
def stopmediaplayer(*args):
    stopgmusicplayer()

#Create media playlist from query
def createmediaplaylist(**kwargs):
    myquery = kwargs.get('query', None)
    player = kwargs.get('player', 'gmusic')
    song,artist,album,playlist,station,podcast=parse_music_query(myquery)
    if not song:
       song = None
    if not artist:
       artist = None
    if not album:
       album = None
    if not playlist:
       playlist = None
    if not station:
       station = None
    if not podcast:
       podcast = None
    response = "Looking for"
    if song is not None:
       response = response + " song "+song
    if artist is not None:
       response = response + " by artist "+artist
    if album is not None:
       response = response + " from album "+album
    if playlist is not None:
       response = response + " playlist "+playlist
    if station is not None:
       response = response + " station "+station
    if podcast is not None:
       response = response + " podcast "+podcast
    say(response)
    if (player == 'gmusic'):
        if (station is not None):
            generategmusicplaylist(station=station)
        elif (podcast is not None):
            generategmusicplaylist(podcast=podcast)
        else:
            creategmusicplaylist(song=song,artist=artist,album=album,playlist=playlist)
        if not os.path.isfile("gmusicplaylist.json"):
           searchgmusic(song=song,artist=artist,album=album,playlist=playlist)

def mediaplayer(query):
    createmediaplaylist(query=query,player='gmusic')
    loopstatus=getloopstatus(query)
    shufflestatus=getshufflestatus(query)
    gmusicplayerthread = Thread(target=playmedia, kwargs={'player':'gmusic','shuffle':shufflestatus,'loop':loopstatus})
    gmusicplayerthread.start()


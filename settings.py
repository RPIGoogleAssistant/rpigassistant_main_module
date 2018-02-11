import os
import os.path
import json

def readsettings(settingsfile,element):
    if os.path.isfile(settingsfile + '.json'):
        with open(settingsfile + '.json', 'r') as settings:
            settingsdata = json.load(settings)
            return settingsdata[element]

def writesettings(settingsfile,element,value):
    if os.path.isfile(settingsfile+'.json'):
        with open(settingsfile+'.json', 'r+') as settings:
            settingsdata = json.load(settings)
            settingsdata[element] = value
            settings.seek(0)
            json.dump(settingsdata, settings, indent=4)
            settings.truncate()

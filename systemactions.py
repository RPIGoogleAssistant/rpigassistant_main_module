import os
import time

from rpitts import say

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

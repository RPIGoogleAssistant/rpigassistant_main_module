import os

from googletrans import Translator
from gtts import gTTS
from settings import readsettings

#Speech and translator declarations
ttsfilename="/tmp/say.mp3"
translator = Translator()
language=readsettings('rpitts','language')
ttslanguage=readsettings('rpitts','ttslanguage')

#Text to speech converter with translation
def say(words):
    words= translator.translate(words, dest=language)
    words=words.text
    words=words.replace("Text, ",'',1)
    words=words.strip()
    print('Saying ' + words)
    tts = gTTS(text=words, lang=ttslanguage, slow=False)
    tts.save(ttsfilename)
    os.system("mpg123 "+ttsfilename)
    os.remove(ttsfilename)


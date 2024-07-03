from UniversalAdMute.models.mobileclipS2 import mobileclip_s2
from UniversalAdMute.modules.ScreenCapture import simpleScreenshot
from UniversalAdMute.modules.AudioController import AudioController

from time import sleep

audioCont = AudioController()
model = mobileclip_s2()

while True:
    probs = model.infer(simpleScreenshot())
    if probs[1] > 51 and audioCont.isUnmuted == False:
        audioCont.unmute()
        
    elif probs[0] > 50:
        audioCont.mute()

    sleep(1)
from UniversalAdMute.models.mobileclipS2 import mobileclip_s2
from UniversalAdMute.modules.ScreenCapture import simpleScreenshot
from UniversalAdMute.modules.AudioController import AudioController

from time import sleep

audioCont = AudioController()
model = mobileclip_s2()
text_prompts = ["Television tv advertisement break",
                "football soccer fifa uefa match tv sports broadcast"] # Set second description to the content you intend to watch.

while True:
    probs = model.infer(simpleScreenshot(), text_prompts)
    if probs[1] > 51 and audioCont.isUnmuted == False:
        audioCont.unmute()

    elif probs[0] > 50:
        audioCont.mute()

    sleep(1)

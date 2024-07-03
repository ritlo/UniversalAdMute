from UniversalAdMute.models.mobileclipS2 import mobileclip_s2
from UniversalAdMute.modules.ScreenCapture import simpleScreenshot
from UniversalAdMute.modules.AudioController import AudioController
from PIL import Image
import torch
from time import sleep

audioCont = AudioController()
model = mobileclip_s2()

while True:
    model.infer(simpleScreenshot())
    sleep(1)
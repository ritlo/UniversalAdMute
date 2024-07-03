from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class AudioController:

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        self.muteVolume=self.volume.GetMute()
        self.currentVolume=self.volume.GetMasterVolumeLevelScalar()
        if self.currentVolume > 0:
            self.isUnmuted = True
        else:
            self.isUnmuted = False

    def setVolume(self, volumeArg):
        self.volume.SetMasterVolumeLevelScaler(volumeArg/100)

    def mute(self):
        self.volume.SetMasterVolumeLevelScaler(0.0)

    def unmute(self):
        self.volume.SetMasterVolumeLevelScaler(self.currentVolume)
    


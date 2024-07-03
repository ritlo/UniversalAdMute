from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class AudioController:

    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        self.muteVolume = self.volume.GetMute()
        self.currentVolume = self.volume.GetMasterVolumeLevelScalar()
        if self.currentVolume > 0:
            self.isUnmuted = True
        else:
            self.isUnmuted = False

    def setVolume(self, volumeArg):
        if volumeArg > 1.0:
            self.volume.SetMasterVolumeLevelScalar(volumeArg/100, None)
        else:
            self.volume.SetMasterVolumeLevelScalar(volumeArg, None)

    def mute(self):
        self.volume.SetMasterVolumeLevelScalar(0.0, None)
        self.isUnmuted = False
        print("Muting")

    def unmute(self):
        self.setVolume(self.currentVolume)
        self.isUnmuted = True
        print("Unmuting")

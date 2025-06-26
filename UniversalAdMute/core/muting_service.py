<<<<<<< HEAD
=======
# Converting UniversalAdMute.py to threads
import threading
import logging
import pythoncom

from UniversalAdMute.models.mobileclipS2 import mobileclip_s2
from UniversalAdMute.modules.ScreenCapture import simpleScreenshot
from UniversalAdMute.modules.AudioController import AudioController

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MutingService:
    def __init__(self):
        pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
        self._muting_active = False
        self._muting_thread = None
        self._thread_stop_event = threading.Event()

        logger.info("MutingService: Initializing AudioController...")
        self.audio_controller = AudioController()
        logger.info("MutingService: AudioController initialized.")

        logger.info(
            "MutingService: Initializing mobileclip_s2 model (this might take time)..."
        )
        self.model = mobileclip_s2()
        logger.info("MutingService: mobileclip_s2 model initialized.")

        self.text_prompts = [
            "Television tv advertisement break",
            "football soccer fifa uefa match tv sports broadcast",
        ]
        self.ad_threshold = 50
        self.content_threshold = 51

        logger.info("MutingService: All components initialized.")

    def _mute_service(self):  # Main Logic Thread
        logger.info("Muting logic thread started.")
        while not self._thread_stop_event.is_set():
            try:
                probs = self.model.infer(simpleScreenshot(), self.text_prompts)
                if (
                    probs[1] > self.content_threshold
                    and not self.audio_controller.isUnmuted
                ):
                    self.audio_controller.unmute()
                    logger.info(f"Unmuted audio. Content similarity: {probs[1]:.2f}%")
                elif probs[0] > self.ad_threshold and self.audio_controller.isUnmuted:
                    self.audio_controller.mute()
                    logger.info(f"Muted audio. Ad similarity: {probs[0]:.2f}%")
            except Exception as e:
                logger.error(f"Error in muting logic: {e}", exc_info=True)

            self._thread_stop_event.wait(1)
        logger.info("Muting logic thread stopped.")

    def start_service(self):
        """Starts the muting process."""
        if not self._muting_active:
            self._muting_active = True
            self._thread_stop_event.clear()
            self._muting_thread = threading.Thread(target=self._mute_service)
            self._muting_thread.daemon = True
            self._muting_thread.start()
            logger.info("Muting process initiated.")
            return True
        logger.info("Muting process already active.")
        return False

    def stop_service(self):
        """Stops the muting process."""
        if self._muting_active:
            self._muting_active = False
            self._thread_stop_event.set()
            if self._muting_thread and self._muting_thread.is_alive():
                self._muting_thread.join(timeout=5)
                if self._muting_thread.is_alive():
                    logger.warning("Muting thread did not terminate gracefully.")
            logger.info("Muting process stopped.")
            return True
        logger.info("Muting process not active.")
        return False

    def get_status(self):  # Status for front end
        return {
            "muting_active": self._muting_active,
            "is_unmuted": self.audio_controller.isUnmuted,
            "current_volume": self.audio_controller.currentVolume,
            "text_prompts": self.text_prompts,
            "ad_threshold": self.ad_threshold,
            "content_threshold": self.content_threshold,
        }

    def update_settings(self, new_settings: dict):  # Update variables using extension
        updated = False
        if (
            "text_prompts" in new_settings
            and isinstance(new_settings["text_prompts"], list)
            and len(new_settings["text_prompts"]) == 2
        ):
            self.text_prompts = new_settings["text_prompts"]
            updated = True
            logger.info(f"Updated text prompts to: {self.text_prompts}")
        if "ad_threshold" in new_settings and isinstance(
            new_settings["ad_threshold"], (int, float)
        ):
            self.ad_threshold = new_settings["ad_threshold"]
            updated = True
            logger.info(f"Updated ad threshold to: {self.ad_threshold}")
        if "content_threshold" in new_settings and isinstance(
            new_settings["content_threshold"], (int, float)
        ):
            self.content_threshold = new_settings["content_threshold"]
            updated = True
            logger.info(f"Updated content threshold to: {self.content_threshold}")
        return updated
>>>>>>> dcfe49a (Created Chrome extension support with FastAPI backend controlling UniversalAdMute thread.)

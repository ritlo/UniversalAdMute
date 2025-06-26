from UniversalAdMute.core.muting_service import MutingService
import logging
import json
import os
import time


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

CONFIG_FILE = "config.json"


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "text_prompts": [
            "Television tv advertisement break",
            "football soccer fifa uefa match tv sports broadcast",
        ],
        "ad_threshold": 50,
        "content_threshold": 51,
    }


def main():
    config = load_config()
    muting_service = MutingService()
    muting_service.text_prompts = config.get(
        "text_prompts", muting_service.text_prompts
    )
    muting_service.ad_threshold = config.get(
        "ad_threshold", muting_service.ad_threshold
    )
    muting_service.content_threshold = config.get(
        "content_threshold", muting_service.content_threshold
    )

    logger.info("Starting UniversalAdMute standalone script...")
    muting_service.start_service()

    try:

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Ctrl+C detected. Stopping muting service...")
        muting_service.stop_service()
        logger.info("UniversalAdMute script terminated.")


if __name__ == "__main__":
    main()

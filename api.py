from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
import logging

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from UniversalAdMute.core.muting_service import MutingService

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

CONFIG_FILE = "config.json"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        logger.info(f"'{CONFIG_FILE}' not found, creating with default values.")
        default_config = {
            "text_prompts": [
                "Television tv advertisement break",
                "football soccer fifa uefa match tv sports broadcast",
            ],
            "ad_threshold": 50,
            "content_threshold": 51,
            "api_host": "127.0.0.1",
            "api_port": 32542,
        }
        save_config(default_config)
        return default_config
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)


config = load_config()

origins = [
    f"http://{config['api_host']}:{config['api_port']}",
    "chrome-extension://*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # For development, allow all origins. In production, restrict to your extension ID.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


muting_service_instance: MutingService = None


def get_muting_service() -> MutingService:
    global muting_service_instance
    if muting_service_instance is None:
        try:
            muting_service_instance = MutingService()

            muting_service_instance.text_prompts = config.get(
                "text_prompts", muting_service_instance.text_prompts
            )
            muting_service_instance.ad_threshold = config.get(
                "ad_threshold", muting_service_instance.ad_threshold
            )
            muting_service_instance.content_threshold = config.get(
                "content_threshold", muting_service_instance.content_threshold
            )
            logger.info("MutingService instance created and initialized with config.")
        except Exception as e:
            logger.error(f"Failed to initialize MutingService: {e}", exc_info=True)

            raise HTTPException(
                status_code=500, detail=f"Server initialization failed: {e}"
            )
    return muting_service_instance


@app.get("/start")
async def start_muting(service: MutingService = Depends(get_muting_service)):
    if service.start_service():
        return {"status": "Muting started"}
    raise HTTPException(status_code=400, detail="Muting already active")


@app.get("/stop")
async def stop_muting(service: MutingService = Depends(get_muting_service)):
    if service.stop_service():
        return {"status": "Muting stopped"}
    raise HTTPException(status_code=400, detail="Muting not active")


@app.get("/status")
async def get_status(service: MutingService = Depends(get_muting_service)):
    return service.get_status()


@app.post("/settings")
async def update_settings(
    new_settings: dict, service: MutingService = Depends(get_muting_service)
):
    if service.update_settings(new_settings):

        current_settings = service.get_status()
        config["text_prompts"] = current_settings["text_prompts"]
        config["ad_threshold"] = current_settings["ad_threshold"]
        config["content_threshold"] = current_settings["content_threshold"]
        save_config(config)
        return {"status": "Settings updated", "new_config": current_settings}
    raise HTTPException(
        status_code=400, detail="Failed to update settings. Check payload."
    )


@app.get("/config")
async def get_config():
    return config


if __name__ == "__main__":
    uvicorn.run(app, host=config["api_host"], port=config["api_port"])

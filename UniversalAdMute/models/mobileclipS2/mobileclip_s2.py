import os
import torch
import open_clip
import logging
from huggingface_hub import logging as hf_logging

logger = logging.getLogger(__name__)
if not logging.root.handlers:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

hf_logging.set_verbosity_info()


class mobileclip_s2:
    def __init__(self):
        self.load_model()
        self.last_probs = [0.0, 0.0]

    def load_model(self):
        logger.info("Attempting to load MobileCLIP-S2-OpenCLIP model...")
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "downloads"
        )

        try:
            self.model, self.preprocess_train, self.preprocess_val = (
                open_clip.create_model_and_transforms(
                    "hf-hub:apple/MobileCLIP-S2-OpenCLIP", cache_dir=model_path
                )
            )
            self.tokenizer = open_clip.get_tokenizer(
                "hf-hub:apple/MobileCLIP-S2-OpenCLIP"
            )

            if torch.cuda.is_available():
                self.device = torch.device("cuda")
                logger.info("Using CUDA")
            else:
                self.device = torch.device("cpu")
                logger.info("Using CUDA")

            self.model.to(self.device)
            self.model.eval()
            logger.info("MobileCLIP-S2-OpenCLIP Model Loaded successfully.")
        except Exception as e:
            logger.error(
                f"Failed to load MobileCLIP-S2-OpenCLIP model: {e}", exc_info=True
            )
            raise

    def infer(self, screenshotArg, text_prompts):
        probs = []
        image_files = [screenshotArg]
        for image_path in image_files:
            try:
                img = image_path.convert("RGB")
                img_tensor = self.preprocess_val(img).unsqueeze(0).to(self.device)

                with torch.no_grad(), torch.amp.autocast("cuda"):
                    image_features = self.model.encode_image(img_tensor)
                    text_features = self.model.encode_text(
                        self.tokenizer(text_prompts).to(self.device)
                    )

                    image_features = image_features / image_features.norm(
                        dim=-1, keepdim=True
                    )
                    text_features = text_features / text_features.norm(
                        dim=-1, keepdim=True
                    )

                    similarity_scores = image_features @ text_features.T
                    text_probs = (100.0 * similarity_scores.softmax(dim=-1)).squeeze(0)

                for i, text_prompt in enumerate(text_prompts):
                    logger.debug(
                        f"Similarity to '{text_prompt}': {text_probs[i].item():.2f}%"
                    )
                    probs.append(float(f"{text_probs[i].item()}"))
                logger.debug("Inference complete.\n")
                self.last_probs = probs
            except Exception as e:  # Return last probs in an error
                logger.error(f"Error during model inference: {e}", exc_info=True)
                return self.last_probs
        return probs

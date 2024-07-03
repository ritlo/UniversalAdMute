from UniversalAdMute.models.mobileclipS2 import mobileclip_s2
from UniversalAdMute.modules.ScreenCapture import simpleScreenshot
from PIL import Image
import torch
from time import sleep

model = mobileclip_s2()


def infer2():
    
    image = simpleScreenshot()
    image
    image_files = [image]

    text_prompts = ["Television tv advertisement break", "football soccer fifa uefa match tv sports broadcast"]

    for image_path in image_files:

        img = image_path.convert('RGB')
        img_tensor = model.preprocess_val(img).unsqueeze(0).to(model.device)

        with torch.no_grad(), torch.amp.autocast('cuda'):

            image_features = model.model.encode_image(img_tensor)
            text_features = model.model.encode_text(
                model.tokenizer(text_prompts).to(model.device))

            image_features = image_features / \
                image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / \
                text_features.norm(dim=-1, keepdim=True)

            similarity_scores = image_features @ text_features.T
            text_probs = (
                100.0 * similarity_scores.softmax(dim=-1)).squeeze(0)

        print(f"Image Path: {image_path}")
        for i, text_prompt in enumerate(text_prompts):
            print(
                f"Similarity to '{text_prompt}': {text_probs[i].item():.2f}%")
        print("\n")

while True:
    infer2()
    sleep(1)
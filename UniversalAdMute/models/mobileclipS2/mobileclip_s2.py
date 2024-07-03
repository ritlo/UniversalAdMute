import os
import requests
import torch
from PIL import Image
import matplotlib.pyplot as plt
import datetime
import open_clip


class mobileclip_s2:
    def __init__(self):
        self.load_model()

    def load_model(self):

        model_path = os.path.join(os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))), 'downloads')
        self.model, self.preprocess_train, self.preprocess_val = open_clip.create_model_and_transforms(
            'hf-hub:apple/MobileCLIP-S2-OpenCLIP', cache_dir=model_path)
        self.tokenizer = open_clip.get_tokenizer(
            'hf-hub:apple/MobileCLIP-S2-OpenCLIP')
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("Using CUDA")
        else: 
            self.device = torch.device("cpu")
            print("Using CPU")
        self.model.to(self.device)
        self.model.eval()

        print("model loaded")

    def infer(self,screenshotArg):

        image_files = [screenshotArg]

        text_prompts = ["Television tv advertisement break", "football soccer fifa uefa match tv sports broadcast"]

        for image_path in image_files:

            img = image_path.convert('RGB')
            img_tensor = self.preprocess_val(img).unsqueeze(0).to(self.device)

            with torch.no_grad(), torch.amp.autocast('cuda'):

                image_features = self.model.encode_image(img_tensor)
                text_features = self.model.encode_text(
                    self.tokenizer(text_prompts).to(self.device))

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

    def infer2(self):

        image_folder = 'test_imgs/input'
        image_files = [os.path.join(image_folder, f) for f in os.listdir(
            image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

        text_prompts = ["advertisement", "football match tv broadcast"]

        for image_path in image_files:

            img = Image.open(image_path).convert('RGB')
            img_tensor = self.preprocess_val(img).unsqueeze(0).to(self.device)

            with torch.no_grad(), torch.amp.autocast('cuda'):

                image_features = self.model.encode_image(img_tensor)
                text_features = self.model.encode_text(
                    self.tokenizer(text_prompts).to(self.device))

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

import open_clip
import requests
import os
import torch
from PIL import Image
import matplotlib.pyplot as plt
import datetime

class mobileclip_s2:
    loaded = ""
    
    def load_model():
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'downloads')
        model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms('hf-hub:apple/MobileCLIP-S2-OpenCLIP',cache_dir=model_path)
        tokenizer = open_clip.get_tokenizer('hf-hub:apple/MobileCLIP-S2-OpenCLIP')
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.eval()
        loaded = "hello,world"
        print(loaded)
        

    def infer():
        

        # Example image URIs
        uris = [
            'http://images.cocodataset.org/test-stuff2017/000000024309.jpg',
            'http://images.cocodataset.org/test-stuff2017/000000028117.jpg',
            'http://images.cocodataset.org/test-stuff2017/000000006149.jpg',
            'http://images.cocodataset.org/test-stuff2017/000000004954.jpg',
            "https://ultralytics.com/images/zidane.jpg",
            "https://i0.wp.com/becleverwithyourcash.com/wp-content/uploads/2021/08/watch_football_on_TV.jpeg",
        ]

        # Text prompts for classification
        text_prompts = [
            "football match",
            "soccer match",
            "fifa",
            "uefa",
            "advertisement",
        ]

        # Create the output directory if it doesn't exist
        if not os.path.exists("output_images"):
            os.makedirs("output_images")
            
        # Process each image
        for i, uri in enumerate(uris):
            img = Image.open(requests.get(uri, stream=True).raw).convert("RGB")
            img_tensor = imapreprocess(img).unsqueeze(0).to(device)  # Preprocess and move to device

            with torch.no_grad():
                # Calculate image features
                image_features = model.encode_image(img_tensor)
                image_features /= image_features.norm(dim=1, keepdim=True)

                # Process each text prompt separately
                for text_prompt in text_prompts:
                    text_tensor = tokenizer([text_prompt]).to(device)
                    text_features = model.encode_text(text_tensor)
                    text_features /= text_features.norm(dim=1, keepdim=True)

                    # Calculate cosine similarity (similarity score)
                    similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    filename = f"output_images/image_{timestamp}_{i}_{text_prompt.replace(' ', '_')}.png"
                    plt.imshow(img)
                    plt.title(f"{text_prompt} Similarity: {similarity[0][0]:.2f}%")
                    plt.axis('off')
                    plt.savefig(filename)
                    plt.close()

                    # Print results to the terminal
                    print(f"URI: {uri}")
                    print(f"Text Prompt: {text_prompt}")
                    print(f"Similarity Score: {similarity[0][0]:.2f}%")
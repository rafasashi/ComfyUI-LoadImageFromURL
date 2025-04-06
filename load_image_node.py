import os
import requests
from PIL import Image
from io import BytesIO
import hashlib

from comfy.model_management import get_torch_device
from nodes import ImageToLatents
import folder_paths

class LoadImageFromURL:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"multiline": False}),
            },
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "load"

    CATEGORY = "image"

    def load(self, url):
        print(f"Downloading image from URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")

            # Optional: save image to input folder with a hash name
            filename = hashlib.md5(url.encode()).hexdigest() + ".png"
            input_folder = folder_paths.get_input_directory()
            save_path = os.path.join(input_folder, filename)
            img.save(save_path)

            print(f"Image saved to {save_path}")

            # Convert image to latent using existing node
            latents = ImageToLatents().convert(image=img)
            return (latents,)
        except Exception as e:
            raise Exception(f"Failed to download or process image: {e}")

NODE_CLASS_MAPPINGS = {
    "LoadImageFromURL": LoadImageFromURL
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageFromURL": "🖼️ Load Image From URL"
}
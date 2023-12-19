from getpass import getpass
import requests
import os
from get_prompt import get_prompt
import replicate

#REPLICATE_API_TOKEN = getpass()
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


def get_image():
    prompts = get_prompt()
    file_paths = []  # List to store file paths of generated images
    count = 0

    for prompt in prompts:
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "width": 1024,
                "height": 1024,
                "prompt": prompt,
                "refine": "expert_ensemble_refiner",
                "scheduler": "KarrasDPM",
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "high_noise_frac": 0.8,
                "prompt_strength": 0.8,
                "num_inference_steps": 50
            }
        )
        image_url = output[0]
        response = requests.get(image_url)

        if response.status_code == 200:
            file_path = f'image_{count}.png'  # Filename for the image
            with open(file_path, 'wb') as file:
                file.write(response.content)
            file_paths.append(file_path)  # Add the file path to the list
            count += 1
        else:
            raise Exception(f"Failed to download image from {image_url}")

    return file_paths  # Return the list of file paths after all prompts are processed

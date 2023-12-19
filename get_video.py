import replicate
import requests


def get_video():
    filenames = ["image_0.png", "image_1.png", "image_2.png", "image_3.png", "image_4.png"]
    videos = []  # List to store paths of downloaded videos

    for idx, file in enumerate(filenames):
        output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
            input={"input_image": open(file, "rb"),
                   "video_length": "25_frames_with_svd_xt",
                   "sizing_strategy": "maintain_aspect_ratio",
                   "frames_per_second": 6}
        )

        video_url = output  # Assuming the output is a URL
        response = requests.get(video_url)
        if response.status_code == 200:
            video_path = f'video_{idx}.mp4'  # Save the video with a unique filename
            with open(video_path, 'wb') as video_file:
                video_file.write(response.content)
            videos.append(video_path)
        else:
            raise Exception(f"Failed to download video from {video_url}")

    return videos  # Return list of downloaded video paths




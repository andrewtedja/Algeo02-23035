import json
import re
import os

DIR = "backend/app/data/"
DATASET_DIR = DIR + "dataset/"
AUDIO_DIR = DATASET_DIR + "audio/"
IMAGE_DIR = DATASET_DIR + "image/"


def generate_mapper() -> None:
    num_pattern = re.compile(r'(\d+)')
    mapping = []
    audio_files = [file for file in os.listdir(AUDIO_DIR)]
    image_files = [file for file in os.listdir(IMAGE_DIR)]
    audio_files.sort()
    image_files.sort()

    image_map = {}
    for image in os.listdir(IMAGE_DIR):
        if image.endswith('.png'):
            match = num_pattern.search(image)
            if match:
                image_number = match.group(1)
                image_map[image_number] = image

    mapping = []
    for audio in os.listdir(AUDIO_DIR):
        match = num_pattern.search(audio)
        if match:
            audio_number = match.group(1)
            # Check if the number exists in the image hashmap
            if audio_number in image_map:
                mapping.append({
                    "audio_name": audio,
                    "pic_name": image_map[audio_number]
                })

    with open(DIR + "mapper.json", 'w') as json_file:
        json.dump(mapping, json_file, indent=4)

    print("Mapping file saved to mapper.json")


def load_mapper(directory: str) -> dict:
    with open(directory + "mapper.json", 'r') as f:
        json_raw = json.load(f)

    audio_to_pic = {entry["audio_name"]: entry["pic_name"] for entry in json_raw}
    pic_to_audio = {entry["pic_name"]: entry["audio_name"] for entry in json_raw}
    return audio_to_pic, pic_to_audio


def create_test_files(directory: str, files_amount: int, file_name: str, file_extension: str) -> None:
    for i in range(1, files_amount + 1):
        filename = os.path.join(directory, f"{file_name}_{i}.{file_extension}")
        with open(filename, 'w') as file:
            file.write(f"This is test file number {i}\n")


# generate_mapper()
print(load_mapper(DIR))

import json
import re
import os

DIR = "src/backend/app/data/"
DATASET_DIR = "src/datasets/"


def generate_mapper(json_or_txt: str) -> None:
    num_pattern = re.compile(r'_([0-9]+)\.[^\.]+$')
    mapping = []

    image_map = {}
    for image in os.listdir(DATASET_DIR):
        if image.endswith((".png", ".jpg", ".jpeg")):
            match = num_pattern.search(image)
            if match:
                image_number = match.group(1)
                image_map[image_number] = image

    mapping = []
    for audio in os.listdir(DATASET_DIR):
        if audio.endswith((".mid", ".wav", ".midi")):
            match = num_pattern.search(audio)
            if match:
                audio_number = match.group(1)
                # Check if the number exists in the image hashmap
                if audio_number in image_map:
                    mapping.append({
                        "audio_name": audio,
                        "pic_name": image_map[audio_number]
                    })
    if (json_or_txt == "json"):
        with open(DIR + "mapper.json", 'w') as json_file:
            json.dump(mapping, json_file, indent=4)

        print("Mapping file saved to mapper.json")

    elif json_or_txt == "txt":
        with open(DIR + "mapper.txt", 'w') as txt_file:
            txt_file.write("audio_name pic_name\n")
            for entry in mapping:
                txt_file.write(f"{entry['audio_name']} {entry['pic_name']}\n")
        print("Mapping file saved to mapper.txt")


def load_mapper_json(directory: str) -> dict:
    with open(directory + "mapper.json", 'r') as f:
        json_raw = json.load(f)

    audio_to_pic = {entry["audio_name"]: entry["pic_name"] for entry in json_raw}
    pic_to_audio = {entry["pic_name"]: entry["audio_name"] for entry in json_raw}
    return audio_to_pic, pic_to_audio


def load_mapper_txt(directory: str) -> dict:
    audio_to_pic = {}
    pic_to_audio = {}

    with open(directory + "mapper.txt", 'r') as file:
        next(file)
        for line in file:
            audio_name, pic_name = line.strip().split()
            audio_to_pic[audio_name] = pic_name
            pic_to_audio[pic_name] = audio_name
    return audio_to_pic, pic_to_audio


def load_mapper(directory: str) -> dict:
    if (os.path.isfile(directory + "mapper.json")):
        return load_mapper_json(directory)
    elif (os.path.isfile(directory + "mapper.txt")):
        return load_mapper_txt(directory)
    else:
        return [], []


def create_test_files(directory: str, files_amount: int, file_name: str, file_extension: str) -> None:
    for i in range(1, files_amount + 1):
        filename = os.path.join(directory, f"{file_name}_{i}.{file_extension}")
        with open(filename, 'w') as file:
            file.write(f"This is test file number {i}\n")


if __name__ == "__main__":
    generate_mapper("json")
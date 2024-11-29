from album_finder import *

##################### DEBUGGING/TESTING ######################
# Mengubah image menjadi grayscale  
def test_convert_img_to_grayscale(file_path : str) -> None:
    grayscale = extract_grayscale(file_path)
    gray_img = PIL.fromarray(grayscale)

    test_directory_assert()

    gray_img.save("results/dinogra.png")    # Save into img
    print("Saved succesfully")

def test_resize_img_to_64(file_path):
    img = PIL.open(file_path).convert("RGB")
    resized_img = img.resize((64,64), PIL.Resampling.BILINEAR) # Resizing
    
    test_directory_assert()
    
    resized_img.save("results/dinogra.png")    # Save into img
    print("Saved succesfully")

def test_dataset_processing(dataset: list[ImageData]):
    directory = "results"
    for image in dataset:
        pixels = np.array(image.pixels).reshape((image.size,image.size))

        img = PIL.fromarray(pixels.astype('uint8'), mode='L')
        output_path = f"{directory}/{image.filename}"
        img.save(output_path)
        print(f"Saved {output_path}")


################# UTILITY #################
def test_directory_assert():
    output_dir = "result"                   # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

# test_convert_img_to_grayscale("images/dino.png")
# test_resize_img_to_64("images/dino.png")

# test = matrix_to_1d(image_normalization(extract_grayscale("images/dino.png")))

dataset = load_dataset()
# standardize_images(dataset)
test_dataset_processing(dataset)
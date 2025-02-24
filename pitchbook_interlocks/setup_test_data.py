import gdown
import zipfile
import os
import shutil


def setup_test_data():
    print("Downloading anonymized input data...")
    file_id = "1_brAIQP5gJ08xNMuUl3mhiYJwEk3Fjlo"
    url = f"https://drive.google.com/uc?id={file_id}"
    zip_path = "./input_data/anonymized_input_data.zip"
    gdown.download(url, zip_path, quiet=False)

    extract_dir = os.path.dirname(os.path.abspath(zip_path))

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    extracted_folder = os.path.join(extract_dir, "anonymized_input_data")

    for item in os.listdir(extracted_folder):
        source = os.path.join(extracted_folder, item)
        destination = os.path.join(extract_dir, item)
        shutil.move(source, destination)

    shutil.rmtree(extracted_folder)
    os.remove(zip_path)

    print("Done! You can now run the analysis.")

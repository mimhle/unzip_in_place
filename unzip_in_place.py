"""A simple python script for extracting all zip files in a folder and delete the zips after unzip
Usage:
    python unzip_in_place.py <path to folder>
Limitations:
    Currently only support ".zip" files (".rar" not support yet)
    No progress bar
    Very slow compare to 7zip or winrar
"""

import os
import argparse
import zipfile
import tqdm


def unzip_files(
        zip_file_path: str,
        destination_dir: str,
        save_to_subfolder: bool = False,
        encoding: str = "utf-8",
        decoding: str = "utf-8",
        include_ext: list = None,
) -> list:
    zipdata = zipfile.ZipFile(zip_file_path)
    zipinfos = zipdata.infolist()

    extracted_files = []
    subfolder_name = ""

    if save_to_subfolder:
        zip_basename = os.path.basename(zip_file_path)
        subfolder_name = os.path.splitext(zip_basename)[0]
        destination_dir = os.path.join(destination_dir, subfolder_name)
        os.makedirs(destination_dir, exist_ok=True)

    for zipinfo in zipinfos:
        zipinfo.filename = ' '.join(zipinfo.filename.encode(encoding).decode(decoding).split())
        extension = os.path.splitext(zipinfo.filename)[-1].lower()
        if include_ext is None or extension in include_ext:
            zipdata.extract(zipinfo, path=destination_dir)
            extracted_file_path = os.path.join(zipinfo.filename)
            if save_to_subfolder:
                extracted_file_path = os.path.join(subfolder_name, zipinfo.filename)
            extracted_files.append(extracted_file_path)

    return extracted_files


def extract_all_zips(path: str, save_to_subfolder: bool = True) -> None:

    file_to_extract = []

    # find all zip files
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".zip"):
                zip_file_path = os.path.join(root, file)
                file_to_extract.append((zip_file_path, root, save_to_subfolder))

    # unzip and delete  all files
    for zip_file_path, root, save_to_subfolder in tqdm.tqdm(file_to_extract):
        unzip_files(zip_file_path, root, save_to_subfolder=save_to_subfolder)
        os.remove(zip_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract all zip files in a folder and delete the zips after unzip")
    parser.add_argument("path_to_folder", type=str, help="path to folder")
    parser.add_argument("-s", "--save_to_subfolder", action="store_true", help="save extracted files to subfolder")
    args = parser.parse_args()

    extract_all_zips(
        args.path_to_folder,
        save_to_subfolder=args.save_to_subfolder
    )

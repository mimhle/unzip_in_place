"""A simple python script for extracting all zip files in a folder and delete the zips after unzip
Usage:
    python unzip_in_place.py <path to folder>
Limitations:
    Currently only support ".zip" files (".rar" not support yet) 
    No progress bar
"""

import os
import sys
import zipfile


def unzip_files(
        zip_file_path: str,
        destination_dir: str,
        encoding: str = "utf-8",
        decoding: str = "utf-8",
        include_ext: list = None,
        save_to_subfolder: bool = False
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
        zipinfo.filename = '_'.join(zipinfo.filename.encode(encoding).decode(decoding).split())
        extension = os.path.splitext(zipinfo.filename)[-1].lower()
        if include_ext is None or extension in include_ext:
            zipdata.extract(zipinfo, path=destination_dir)
            extracted_file_path = os.path.join(zipinfo.filename)
            if save_to_subfolder:
                extracted_file_path = os.path.join(subfolder_name, zipinfo.filename)
            extracted_files.append(extracted_file_path)

    return extracted_files


def extract_all_zips(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".zip"):
                zip_file_path = os.path.join(root, file)
                print("Extracting:", zip_file_path)
                unzip_files(zip_file_path, root, save_to_subfolder=True)
                os.remove(zip_file_path)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        path_to_folder = sys.argv[1]
        extract_all_zips(path_to_folder)
    else:
        print('Usage: python unzip_in_place.py <path_to_folder>')

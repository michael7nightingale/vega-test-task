from fastapi import UploadFile


image_extensions = {"png", "jpg", "jpeg", "img"}


def get_filename_extension(filename: str) -> str:
    split_filename = filename.split('.')
    if not split_filename:
        return ""
    else:
        return split_filename[-1]


def filter_image_files(files: list[UploadFile]) -> list[UploadFile]:
    return [
        file for file in files
        if get_filename_extension(file.filename.strip()) in image_extensions
    ]

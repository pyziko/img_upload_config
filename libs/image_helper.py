import os.path
import re
from typing import Union

from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES


#   todo info  name(images) used here must match dump folder set in default_config UPLOADED_IMAGES_DEST
IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Takes  FileStorage and saves it to a folder,  # root folder configured in default_config"""
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """Takes images name and folder and return full path"""
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """Takes a filename and returns an image on any of the accepted formats."""
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Take FileStorage and returns the file name
    Allows our fns to call this with both file names and FileStorages and always get back file name."""
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check our regex and return whether the string matches or not"""
    filename = _retrieve_filename(file)

    allowed_format = "|".join(IMAGES)   # png|svg|jpe|jpg"jpeg
    # first char must be a-zA-Z0-9 :: oher chars a-zA-Z0-9_()-\.  :: * other char 1 or more :: .jpg
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """
    Return full name of image in the path
    get_basename('some/folder/image.jpg) returns 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]):
    """Return file extension
    get_extension('image.jpg') returns '.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]


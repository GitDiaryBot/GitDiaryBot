import os
from contextlib import contextmanager
from typing import Iterator, BinaryIO


_PHOTO_DIR = 'photo'


class PhotoTransformer:

    _FILE_NAME_PTRN = '{}.jpeg'

    def __init__(self,
                 base_dir: str,
                 rel_dir: str = _PHOTO_DIR) -> None:
        self._base_dir = base_dir
        self._rel_dir = rel_dir
        self._target_dir = os.path.join(base_dir, rel_dir)

    @contextmanager
    def file_writer(self, file_id: str) -> Iterator[BinaryIO]:
        if not os.path.exists(self._target_dir):
            os.makedirs(self._target_dir)
        abs_path = os.path.join(self._target_dir, self._FILE_NAME_PTRN.format(file_id))
        with open(abs_path, "wb") as fobj:
            yield fobj

    def handle_file_id(self, file_id: str) -> str:
        rel_path = os.path.join(self._rel_dir, self._FILE_NAME_PTRN.format(file_id))
        message = f"Photo: {rel_path}"
        return message

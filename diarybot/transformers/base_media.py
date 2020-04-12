import abc
import os
from typing import Iterator, BinaryIO
from contextlib import contextmanager


class BaseMediaTransformer(abc.ABC):

    _FILE_NAME_PTRN = '{}'

    def __init__(self,
                 base_dir: str,
                 rel_dir: str) -> None:
        self._base_dir = base_dir
        self._rel_dir = rel_dir
        self._target_dir = os.path.join(base_dir, rel_dir)

    @abc.abstractmethod
    def handle_file_id(self, file_id: str) -> str:
        """Generate text message for saved file_id."""

    @contextmanager
    def file_writer(self, file_id: str) -> Iterator[BinaryIO]:
        if not os.path.exists(self._target_dir):
            os.makedirs(self._target_dir)
        abs_path = os.path.join(self._target_dir, self._FILE_NAME_PTRN.format(file_id))
        with open(abs_path, "wb") as fobj:
            yield fobj

    def _rel_path(self, file_id: str) -> str:
        return os.path.join(self._rel_dir, self._FILE_NAME_PTRN.format(file_id))

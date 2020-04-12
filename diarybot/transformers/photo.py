from .base_media import BaseMediaTransformer


_PHOTO_DIR = 'photo'


class PhotoTransformer(BaseMediaTransformer):

    _FILE_NAME_PTRN = '{}.jpeg'

    def __init__(self,
                 base_dir: str,
                 rel_dir: str = _PHOTO_DIR) -> None:
        super().__init__(base_dir, rel_dir)

    def handle_file_id(self, file_id: str) -> str:
        return "Photo: {}".format(self._rel_path(file_id))

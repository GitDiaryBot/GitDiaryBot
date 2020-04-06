from typing import Iterator, List
from io import BytesIO

from telegram import Message, PhotoSize

from diarybot.events import PhotoReceived
from .interface import EventExtractorInterface


class PhotoEventExtractor(EventExtractorInterface):
    def extract_events(self, message: Message) -> Iterator[PhotoReceived]:
        if message.photo:
            photo = self._largest_photo(message.photo)
            tg_file = photo.get_file()
            fobj = BytesIO()
            tg_file.download(out=fobj)
            yield PhotoReceived(tg_file.file_id, fobj.getvalue())

    @staticmethod
    def _largest_photo(photo_sizes: List[PhotoSize]) -> PhotoSize:
        return max([
            (size.width * size.height, size)
            for size in photo_sizes
        ])[1]

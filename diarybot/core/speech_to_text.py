import base64
import logging

import requests


_SPEECH_TO_TEXT_URL = "https://speech.googleapis.com/v1/speech:recognize"


logger = logging.getLogger(__name__)


class SpeechToTextClient:

    def __init__(self, google_api_key: str) -> None:
        self._google_api_key = google_api_key

    def transcript(self, language_code, audio):
        payload = {
            "config": {
                "encoding": 'OGG_OPUS',
                "sampleRateHertz": 48000,
                "languageCode": language_code,
                "maxAlternatives": 1,
                "profanityFilter": False,
                "speechContexts": [],
                "enableWordTimeOffsets": False,
                "enableAutomaticPunctuation": True,
                "model": "phone_call",
                "useEnhanced": True,
            },
            "audio": {
                "content": base64.b64encode(audio).decode(),
            }
        }
        response = requests.post(
            _SPEECH_TO_TEXT_URL,
            params={'key': self._google_api_key},
            json=payload,
        )
        logger.debug("Text to speech response: %s", response.text)
        response.raise_for_status()
        results = response.json().get('results', [])
        if results:
            alternatives = results[0]['alternatives']
            return alternatives[0]['transcript']
        return ""

    __call__ = transcript

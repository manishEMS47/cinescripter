import base64
import os

import requests

from utils.common import SettingsLoader
from utils.logs import logger

FOLDER_PREFIX = "audio/"
MAX_TEXT_LENGTH = 5000


class SixtyDB:
    """60db Text-To-Speech provider.

    Mirrors the interface of the other audio providers: ``generate`` takes a
    section and an output folder, writes a narration file to disk, records the
    resulting path in ``section["media"]["audio_path"]`` and returns the section.
    """

    APP_NAME = "SIXTYDB"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )

    async def generate(self, section: dict, output_folder: str) -> str:
        logger.info('Generating audio for %s', section)
        os.makedirs(os.path.join(output_folder, FOLDER_PREFIX), exist_ok=True)

        text = section['sentence'][:MAX_TEXT_LENGTH]
        headers = {
            "Authorization": f"Bearer {self.options.get('api_key')}",
        }
        payload = {
            "text": text,
            "voice_id": self.options.get("voice_id"),
            "speed": self.options.get("speed"),
            "stability": self.options.get("stability"),
            "similarity": self.options.get("similarity"),
            "enhance": self.options.get("enhance"),
            "output_format": self.options.get("output_format"),
        }

        response = requests.post(
            f"{self.options.get('api')}/tts-synthesize",
            json=payload,
            headers=headers,
            timeout=self.options.get("timeout"),
        )
        response.raise_for_status()

        parsed_response = response.json()
        if not parsed_response.get("success"):
            raise RuntimeError(
                f"60db TTS failed: {parsed_response.get('message')}"
            )

        audio = base64.b64decode(parsed_response["audio_base64"])
        extension = parsed_response.get("output_format") or self.options.get("output_format")
        file_name = f"{section['index']}-{section['topic_slug']}.{extension}"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        with open(file_path, "wb") as fl:
            fl.write(audio)

        logger.info('Downloaded %s', file_path)
        section["media"]["audio_path"] = file_path
        return section

    def list_voices(self) -> list:
        """Fetch the voices available to the configured API key.

        Helper to discover ``voice_id`` values to put in ``SIXTYDB_VOICE_ID``.
        """
        headers = {
            "Authorization": f"Bearer {self.options.get('api_key')}",
        }
        response = requests.get(
            f"{self.options.get('api')}/myvoices",
            headers=headers,
            timeout=self.options.get("timeout"),
        )
        response.raise_for_status()
        return response.json().get("data", [])

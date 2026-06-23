import os

from elevenlabs import generate, save

from generation.sixtydb import SixtyDB
from utils.common import SettingsLoader
from utils.logs import logger

FOLDER_PREFIX = "audio/"


class ElevenLabsAudio:
    """ElevenLabs Text-To-Speech provider."""

    APP_NAME = "ELEVENLABS"

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )

    async def generate(self, section: dict, output_folder: str) -> str:
        logger.info('Generating audio for %s', section)
        os.makedirs(os.path.join(output_folder, FOLDER_PREFIX), exist_ok=True)
        audio = generate(
            text=section['sentence'],
            voice=self.options.get("voice"),
            model=self.options.get("model"),
        )
        file_name = f"{section['index']}-{section['topic_slug']}.wav"
        file_path = os.path.join(output_folder, FOLDER_PREFIX, file_name)
        save(audio, file_path)
        logger.info('Downloaded %s', file_path)
        section["media"]["audio_path"] = file_path
        return section


class Audio:
    """Audio entrypoint that dispatches to the configured TTS provider.

    The active provider is selected via the ``TTS`` settings (``TTS_PROVIDER``
    environment variable). Every provider exposes the same
    ``async generate(section, output_folder)`` signature so the rest of the
    generation pipeline is provider-agnostic.
    """

    APP_NAME = "TTS"

    PROVIDERS = {
        "elevenlabs": ElevenLabsAudio,
        "60db": SixtyDB,
        "sixtydb": SixtyDB,
    }

    def __init__(self, **kwargs):
        self.options = SettingsLoader.load(
            self.APP_NAME,
            kwargs
        )
        provider = self.options.get("provider")
        provider_cls = self.PROVIDERS.get(provider)
        if provider_cls is None:
            raise ValueError(
                f"Unknown TTS provider '{provider}'. "
                f"Available providers: {list(self.PROVIDERS)}"
            )
        logger.info("Using TTS provider: %s", provider)
        self.provider = provider_cls()

    async def generate(self, section: dict, output_folder: str) -> str:
        return await self.provider.generate(section, output_folder)

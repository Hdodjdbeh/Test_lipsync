from pathlib import Path
import logging

logger = logging.getLogger(__name__)
import soundfile as sf
from silero import silero_tts


class SileroTTS:
    def __init__(self):
        self.model, _ = silero_tts(
            language="ru",
            speaker="v4_ru",
        )
        logger.info("Silero TTS model loaded")

    def generate(self, text: str, output_path: Path) -> Path:
        logger.info("Generating speech")
        audio = self.model.apply_tts(
            text=text,
            speaker="baya",
            sample_rate=48000,
        )

        sf.write(
            output_path,
            audio,
            48000,
        )
        logger.info(
            "Audio saved: %s",
            output_path,
        )
        return output_path
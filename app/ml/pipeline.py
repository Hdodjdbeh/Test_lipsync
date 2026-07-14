from pathlib import Path

from app.ml.lipsync import Wav2Lip
from app.ml.tts import SileroTTS

import logging

logger = logging.getLogger(__name__)

class GenerationPipeline:
    def __init__(self):
        self.tts = SileroTTS()
        self.lipsync = Wav2Lip()

    def generate(
        self,
        task_id: str,
        text: str,
        avatar_path: Path = Path("avatars/avatar.jpg"),
    ) -> Path:
        logger.info(
            "Pipeline started for task %s",
            task_id,
        )
        audio_path = Path("temp/audio") / f"{task_id}.wav"
        video_path = Path("results") / f"{task_id}.mp4"

        if not avatar_path.exists():
            raise FileNotFoundError(avatar_path)

        audio_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        video_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.tts.generate(
            text=text,
            output_path=audio_path,
        )
        logger.info(
            "Audio generated: %s",
            audio_path,
        )
        self.lipsync.generate(
            avatar_path=avatar_path,
            audio_path=audio_path,
            output_path=video_path,
        )
        audio_path.unlink(missing_ok=True)
        logger.info(
            "Video generated: %s",
            video_path,
        )
        return video_path


_pipeline: GenerationPipeline | None = None


def get_pipeline() -> GenerationPipeline:
    global _pipeline

    if _pipeline is None:
        _pipeline = GenerationPipeline()

    return _pipeline
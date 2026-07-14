from pathlib import Path
import subprocess

import logging

logger = logging.getLogger(__name__)

class Wav2Lip:
    def __init__(self):
        logger.info("Starting Wav2Lip")
        self.project_dir = Path("third_party/Wav2Lip")
        self.checkpoint = self.project_dir / "checkpoints" / "wav2lip_gan.pth"

    def generate(
        self,
        avatar_path: Path,
        audio_path: Path,
        output_path: Path,
    ) -> Path:
        logger.info(
            "Generating video: %s",
            output_path.name,
        )
        if not avatar_path.exists():
            raise FileNotFoundError(avatar_path)

        if not audio_path.exists():
            raise FileNotFoundError(audio_path)

        if not self.checkpoint.exists():
            raise FileNotFoundError(self.checkpoint)
        command = [
            "python",
            "inference.py",
            "--checkpoint_path",
            str(self.checkpoint.resolve()),
            "--face",
            str(avatar_path.resolve()),
            "--audio",
            str(audio_path.resolve()),
            "--outfile",
            str(output_path.resolve()),
        ]

        result = subprocess.run(
            command,
            cwd=self.project_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            logger.error(result.stderr)
            raise RuntimeError(
                f"Wav2Lip failed:\n{result.stderr}"
            )

        return output_path
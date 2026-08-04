import os
import subprocess
from typing import Dict, List, Optional

from ..config import LOCAL_OUTPUT_DIR


def crop_clip_ffmpeg(
    source_path: str,
    start_time: float,
    end_time: float,
    aspect_ratio: str,
    out_path: str,
) -> str:
    """
    Create one vertical short using only FFmpeg.
    """

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if aspect_ratio == "9:16":
        vf = (
            "scale=720:1280:force_original_aspect_ratio=increase,"
            "crop=720:1280"
        )
    elif aspect_ratio == "1:1":
        vf = (
            "scale=720:720:force_original_aspect_ratio=increase,"
            "crop=720:720"
        )
    else:
        raise ValueError(f"Unsupported aspect ratio: {aspect_ratio}")

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start_time),
        "-to",
        str(end_time),
        "-i",
        source_path,
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "20",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        out_path,
    ]

    subprocess.run(cmd, check=True)

    return out_path


def crop_highlights_ffmpeg(
    source_path: str,
    highlights: List[Dict],
    aspect_ratio: str = "9:16",
    out_dir: Optional[str] = None,
) -> List[Dict]:

    out_dir = out_dir or LOCAL_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)

    results = []

    for i, h in enumerate(highlights, 1):

        out_path = os.path.join(
            out_dir,
            f"short_{i:02d}.mp4",
        )

        print(
            f"[ffmpeg] Rendering {i}/{len(highlights)}",
            flush=True,
        )

        try:

            crop_clip_ffmpeg(
                source_path,
                float(h["start_time"]),
                float(h["end_time"]),
                aspect_ratio,
                out_path,
            )

            results.append(
                {
                    **h,
                    "clip_url": out_path,
                }
            )

        except Exception as e:

            results.append(
                {
                    **h,
                    "clip_url": None,
                    "error": str(e),
                }
            )

    return results

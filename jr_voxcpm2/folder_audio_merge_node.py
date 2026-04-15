import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Tuple


SUPPORTED_AUDIO_EXTS = {".wav", ".mp3", ".flac"}


def _natural_sort_key(path: Path):
    parts = re.split(r"(\d+)", path.name.lower())
    return [int(p) if p.isdigit() else p for p in parts]


def _resolve_ffmpeg(ffmpeg_path: str) -> str:
    candidates = []

    if ffmpeg_path and ffmpeg_path.strip():
        candidates.append(ffmpeg_path.strip())

    if os.name == "nt":
        candidates.extend(["ffmpeg.exe", "ffmpeg"])
    else:
        candidates.extend(["ffmpeg", "ffmpeg.exe"])

    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            return str(p.resolve())

        found = shutil.which(candidate)
        if found:
            return found

    raise FileNotFoundError(
        "ffmpeg not found. Please install ffmpeg or provide ffmpeg_path."
    )


def _collect_audio_files(source_folder: Path) -> List[Path]:
    files = []
    for item in source_folder.iterdir():
        if item.is_file() and item.suffix.lower() in SUPPORTED_AUDIO_EXTS:
            files.append(item)

    files.sort(key=_natural_sort_key)
    return files


def _ensure_single_extension(files: List[Path]) -> str:
    exts = {f.suffix.lower() for f in files}
    if len(exts) != 1:
        raise ValueError(
            f"Mixed audio formats found in source folder: {sorted(exts)}. "
            "This node requires all source files in one folder to use the same format."
        )
    return files[0].suffix.lower()


def _run_cmd(cmd: List[str]) -> Tuple[int, str, str]:
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,
    )
    return result.returncode, result.stdout, result.stderr


def _build_output_codec_args(ext: str) -> List[str]:
    ext = ext.lower()
    if ext == ".wav":
        return ["-c:a", "pcm_s16le"]
    if ext == ".flac":
        return ["-c:a", "flac"]
    if ext == ".mp3":
        return ["-c:a", "libmp3lame", "-q:a", "2"]
    return []


def _merge_with_concat_filter(
    ffmpeg_bin: str,
    files: List[Path],
    output_file: Path,
    overwrite: bool,
    output_ext: str,
) -> Tuple[int, str, str]:
    """
    使用 ffmpeg concat filter 进行真正的音频拼接。
    这比 concat demuxer + copy 更稳，尤其适合 TTS 切片。
    """
    with tempfile.TemporaryDirectory(prefix="jr_voxcpm2_concat_filter_") as tmpdir:
        filter_script = Path(tmpdir) / "filter_complex.txt"

        input_cmd = []
        filter_inputs = []

        for idx, f in enumerate(files):
            input_cmd.extend(["-i", str(f.resolve())])
            filter_inputs.append(f"[{idx}:a]")

        # 例如: [0:a][1:a][2:a]concat=n=3:v=0:a=1[outa]
        filter_text = "".join(filter_inputs) + f"concat=n={len(files)}:v=0:a=1[outa]"
        filter_script.write_text(filter_text, encoding="utf-8")

        cmd = [
            ffmpeg_bin,
            "-y" if overwrite else "-n",
            "-hide_banner",
            "-loglevel",
            "error",
            *input_cmd,
            "-filter_complex_script",
            str(filter_script),
            "-map",
            "[outa]",
            *_build_output_codec_args(output_ext),
            str(output_file),
        ]

        return _run_cmd(cmd)


class JR_VoxCPM2_FolderAudioMerge:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_folder": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "placeholder": r"D:\ComfyUI\output\audio\book01 or /data/ComfyUI/output/audio/book01",
                    },
                ),
                "output_folder": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "placeholder": r"D:\ComfyUI\output\audio\merged or /data/ComfyUI/output/audio/merged",
                    },
                ),
                "output_basename": (
                    "STRING",
                    {
                        "default": "merged_audio",
                        "multiline": False,
                    },
                ),
                "overwrite": ("BOOLEAN", {"default": True}),
                "ffmpeg_path": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "placeholder": r"optional: C:\ffmpeg\bin\ffmpeg.exe or /usr/bin/ffmpeg",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("output_file", "file_count", "log")
    FUNCTION = "merge_audio_folder"
    CATEGORY = "JR/VoxCPM2/Utils"

    def merge_audio_folder(
        self,
        source_folder: str,
        output_folder: str,
        output_basename: str,
        overwrite: bool,
        ffmpeg_path: str,
    ):
        source_dir = Path(source_folder.strip()).expanduser()
        output_dir = Path(output_folder.strip()).expanduser()

        if not source_dir.exists() or not source_dir.is_dir():
            raise ValueError(f"source_folder does not exist or is not a folder: {source_dir}")

        output_dir.mkdir(parents=True, exist_ok=True)

        files = _collect_audio_files(source_dir)
        if not files:
            raise ValueError(
                f"No supported audio files found in: {source_dir} "
                f"(supported: {sorted(SUPPORTED_AUDIO_EXTS)})"
            )

        ext = _ensure_single_extension(files)

        if not output_basename or not output_basename.strip():
            output_basename = f"{source_dir.name}_merged"

        output_file = output_dir / f"{output_basename}{ext}"

        if output_file.exists() and not overwrite:
            raise ValueError(f"Output file already exists and overwrite=False: {output_file}")

        if len(files) == 1:
            shutil.copy2(files[0], output_file)
            log = (
                "Only one audio file found. Copied directly.\n"
                f"Source: {files[0]}\n"
                f"Output: {output_file}"
            )
            return (str(output_file), 1, log)

        ffmpeg_bin = _resolve_ffmpeg(ffmpeg_path)

        code, _, err = _merge_with_concat_filter(
            ffmpeg_bin=ffmpeg_bin,
            files=files,
            output_file=output_file,
            overwrite=overwrite,
            output_ext=ext,
        )

        if code == 0 and output_file.exists():
            file_list_preview = "\n".join([f.name for f in files[:20]])
            if len(files) > 20:
                file_list_preview += f"\n... ({len(files) - 20} more files)"

            log = (
                "Merged successfully with concat filter.\n"
                f"ffmpeg: {ffmpeg_bin}\n"
                f"Source folder: {source_dir}\n"
                f"Detected format: {ext}\n"
                f"Files merged: {len(files)}\n"
                f"Output: {output_file}\n\n"
                "[First files]\n"
                f"{file_list_preview}"
            )
            return (str(output_file), len(files), log)

        raise RuntimeError(
            "Audio merge failed.\n\n"
            "[ffmpeg stderr]\n"
            f"{err.strip()}"
        )


NODE_CLASS_MAPPINGS = {
    "JR_VoxCPM2_FolderAudioMerge": JR_VoxCPM2_FolderAudioMerge,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JR_VoxCPM2_FolderAudioMerge": "JR VoxCPM2 Folder Audio Merge",
}
from pathlib import Path

from . import steps


def _need(path: Path, resume: bool) -> bool:
    """返回 True 表示该步骤需要执行"""
    if resume and path.is_file():
        print(f"[跳过] 已存在: {path}")
        return False
    return True


def run_pipeline(cfg: dict) -> Path:
    video = Path(cfg["input_video"])
    resume = cfg["resume"]
    work = Path(cfg["output_dir"]) / video.stem
    work.mkdir(parents=True, exist_ok=True)

    raw = work / "01_audio.wav"
    if _need(raw, resume):
        print("[1/5] 提取音频")
        steps.extract_audio(cfg, video, raw)

    stem_dir = work / "demucs" / cfg["separation"].get("model", "htdemucs") / raw.stem
    vocals, accomp = stem_dir / "vocals.wav", stem_dir / "no_vocals.wav"
    if _need(vocals, resume) or not accomp.is_file():
        print("[2/5] 人声/伴奏分离")
        vocals, accomp = steps.separate(cfg, raw, work)

    converted = work / "03_vocals_converted.wav"
    if _need(converted, resume):
        print("[3/5] 人声克隆 (RVC)")
        steps.convert_voice(cfg, vocals, converted)

    mixed = work / "04_mix.wav"
    if _need(mixed, resume):
        print("[4/5] 混音")
        steps.mix_audio(cfg, converted, accomp, mixed)

    name = cfg["output"].get("filename") or f"{video.stem}_cover.mp4"
    final = work / name
    print("[5/5] 合成视频")
    steps.mux_video(cfg, video, mixed, final)

    print(f"完成: {final}")
    return final

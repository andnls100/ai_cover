import sys
from pathlib import Path

from .utils import run


def extract_audio(cfg: dict, video: Path, out_wav: Path) -> None:
    """1. 从视频提取音频 -> 44.1k 立体声 wav"""
    sr = cfg["mix"].get("sample_rate", 44100)
    run([cfg["ffmpeg"], "-y", "-i", str(video), "-vn", "-ac", "2",
         "-ar", str(sr), "-c:a", "pcm_s16le", str(out_wav)])


def separate(cfg: dict, audio: Path, work: Path) -> tuple[Path, Path]:
    """2. 人声 / 伴奏分离 (Demucs two-stems)，返回 (vocals, accompaniment)"""
    sep = cfg["separation"]
    model = sep.get("model", "htdemucs")
    out_root = work / "demucs"
    run([sys.executable, "-m", "demucs", "-n", model, "--two-stems=vocals",
         "-d", sep.get("device", "cuda"), "-o", str(out_root), str(audio)])
    stem_dir = out_root / model / audio.stem
    vocals, accomp = stem_dir / "vocals.wav", stem_dir / "no_vocals.wav"
    if not vocals.is_file() or not accomp.is_file():
        raise FileNotFoundError(f"Demucs 未产出预期文件: {stem_dir}")
    return vocals, accomp


def convert_voice(cfg: dict, vocals: Path, out_wav: Path) -> None:
    """3. RVC 人声克隆：把人声转成目标模型音色"""
    from rvc_python.infer import RVCInference  # 延迟导入，避免没用到时加载 torch

    r = cfg["rvc"]
    rvc = RVCInference(device=r.get("device", "cuda:0"))
    rvc.load_model(r["model_path"], version=r.get("version", "v2"),
                   index_path=r.get("index_path") or "")
    rvc.set_params(
        f0method=r.get("f0_method", "rmvpe"),
        f0up_key=r.get("f0_up_key", 0),
        index_rate=r.get("index_rate", 0.5),
        protect=r.get("protect", 0.33),
        filter_radius=r.get("filter_radius", 3),
        rms_mix_rate=r.get("rms_mix_rate", 0.25),
        resample_sr=r.get("resample_sr", 0),
    )
    rvc.infer_file(str(vocals), str(out_wav))
    rvc.unload_model()


def mix_audio(cfg: dict, vocals: Path, accomp: Path, out_wav: Path) -> None:
    """4. 转换后的人声 + 伴奏 混音"""
    m = cfg["mix"]
    sr = m.get("sample_rate", 44100)
    fmt = f"aresample={sr},aformat=sample_fmts=fltp:channel_layouts=stereo"
    chain = (f"[0:a]{fmt},volume={m.get('vocal_volume', 1.0)}[v];"
             f"[1:a]{fmt},volume={m.get('accompaniment_volume', 1.0)}[a];"
             f"[v][a]amix=inputs=2:duration=longest:normalize=0")
    chain += ",loudnorm=I=-16:TP=-1.5:LRA=11[out]" if m.get("loudnorm", True) else "[out]"
    run([cfg["ffmpeg"], "-y", "-i", str(vocals), "-i", str(accomp),
         "-filter_complex", chain, "-map", "[out]", "-ar", str(sr),
         "-c:a", "pcm_s16le", str(out_wav)])


def mux_video(cfg: dict, video: Path, audio: Path, out_video: Path) -> None:
    """5. 新音频与原视频画面合成（视频流直接拷贝，不重编码）"""
    run([cfg["ffmpeg"], "-y", "-i", str(video), "-i", str(audio),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
         "-c:a", "aac", "-b:a", cfg["output"].get("audio_bitrate", "256k"),
         "-shortest", str(out_video)])

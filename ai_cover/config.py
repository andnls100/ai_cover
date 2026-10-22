from pathlib import Path

import yaml


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    for key in ("input_video", "rvc"):
        if key not in cfg:
            raise ValueError(f"配置缺少必填项: {key}")

    video = Path(cfg["input_video"])
    if not video.is_file():
        raise FileNotFoundError(f"输入视频不存在: {video}")

    model = Path(cfg["rvc"]["model_path"])
    if not model.is_file():
        raise FileNotFoundError(f"RVC 模型不存在: {model}")

    index = cfg["rvc"].get("index_path") or ""
    if index and not Path(index).is_file():
        raise FileNotFoundError(f"RVC index 文件不存在: {index}")

    cfg.setdefault("output_dir", "output")
    cfg.setdefault("resume", True)
    cfg.setdefault("ffmpeg", "ffmpeg")
    cfg.setdefault("separation", {})
    cfg.setdefault("mix", {})
    cfg.setdefault("output", {})
    return cfg

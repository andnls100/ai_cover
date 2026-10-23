from pathlib import Path

from ai_cover.steps import separate, convert_voice, mix_audio


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input.mp3"
MODEL = ROOT / "model" / "my.pth"
OUTPUT = ROOT / "output"


def main() -> None:
    if not INPUT.is_file():
        raise FileNotFoundError(f"找不到输入歌曲：{INPUT}")
    if not MODEL.is_file():
        raise FileNotFoundError(f"找不到 RVC 模型：{MODEL}")

    OUTPUT.mkdir(parents=True, exist_ok=True)

    cfg = {
        "ffmpeg": "ffmpeg",
        "separation": {
            "model": "htdemucs",
            "device": "cuda",
        },
        "rvc": {
            "model_path": str(MODEL),
            "index_path": "",
            "version": "v2",
            "device": "cuda:0",
            "f0_method": "rmvpe",
            "f0_up_key": 0,
            "index_rate": 0.5,
            "protect": 0.33,
            "filter_radius": 3,
            "rms_mix_rate": 0.25,
            "resample_sr": 0,
        },
        "mix": {
            "vocal_volume": 1.0,
            # -2 dB: 20 * log10(0.794328) ≈ -2
            "accompaniment_volume": 0.794328,
            "sample_rate": 44100,
            # Keep the requested relative accompaniment reduction; do not
            # apply loudness normalization that could change the mix balance.
            "loudnorm": False,
        },
        "output": {
            "audio_bitrate": "256k",
        },
    }

    print("[1/3] 分离人声与伴奏")
    vocals, accompaniment = separate(cfg, INPUT, OUTPUT)

    converted = OUTPUT / "my_vocals_converted.wav"
    print("[2/3] RVC 人声转换")
    convert_voice(cfg, vocals, converted)

    final = OUTPUT / "my_vocals.wav"
    print("[3/3] 混合转换后的人声与伴奏")
    mix_audio(cfg, converted, accompaniment, final)

    print(f"完成：{final}")
    print(f"转换后的人声：{converted}")
    print(f"分离出的人声：{vocals}")
    print(f"分离出的伴奏：{accompaniment}")


if __name__ == "__main__":
    main()

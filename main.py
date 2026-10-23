import argparse

from ai_cover.config import load_config
from ai_cover.pipeline import run_pipeline


def main():
    p = argparse.ArgumentParser(
        description="AI 翻唱：视频模式沿用原流程，音频模式输出翻唱音频"
    )
    p.add_argument("-c", "--config", default="config.yaml", help="视频模式配置文件")
    p.add_argument(
        "--mode",
        choices=("video", "audio"),
        default="video",
        help="video：按原流程处理视频并合成；audio：处理当前目录 input.mp3 并输出 output/my_vocals.wav",
    )
    args = p.parse_args()

    if args.mode == "audio":
        from audio_main import main as run_audio_pipeline

        run_audio_pipeline()
        return

    # 默认保持原有视频处理逻辑不变。
    run_pipeline(load_config(args.config))


if __name__ == "__main__":
    main()

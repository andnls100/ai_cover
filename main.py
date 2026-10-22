import argparse

from ai_cover.config import load_config
from ai_cover.pipeline import run_pipeline


def main():
    p = argparse.ArgumentParser(description="视频 AI 翻唱：分离 -> 人声克隆 -> 混音 -> 合成视频")
    p.add_argument("-c", "--config", default="config.yaml", help="配置文件路径")
    args = p.parse_args()
    run_pipeline(load_config(args.config))


if __name__ == "__main__":
    main()

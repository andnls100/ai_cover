# ai_cover
AI 翻唱工具，支持视频翻唱和纯音频翻唱。

- 视频模式：提取音频 → Demucs 分离人声/伴奏 → RVC 人声转换 → 混音 → 合成回视频。
- 音频模式：处理完整歌曲 → Demucs 分离人声/伴奏 → RVC 人声转换 → 伴奏降低 2 dB → 输出 WAV。

## 安装 (Windows + NVIDIA)

1. 安装 ffmpeg 并加入 PATH
2. 按 CUDA 版本从 https://pytorch.org 安装 torch
3. `pip install -r requirements.txt`

将 RVC 文件放在项目根目录的 `model` 文件夹中：
- `model/tt.pth`：RVC 模型
- `model/tt.index`：RVC 索引

## 视频模式（默认，保留原逻辑）

编辑 `config.yaml`（视频路径、变调等），然后运行：

    python main.py
    python main.py -c other.yaml
    python main.py --mode video

产物在 `output/<视频名>/`：`01_audio.wav`、`demucs/…`、`03_vocals_converted.wav`、`04_mix.wav`、`<视频名>_cover.mp4`。

## 纯音频模式

将完整歌曲放在项目根目录并命名为 `input.mp3`，确认 `model/tt.pth` 和 `model/tt.index` 存在，然后运行：

    python main.py --mode audio

输出文件：
- `output/my_vocals.wav`：转换后人声与伴奏的混合成品，伴奏降低 2 dB。
- `output/my_vocals_converted.wav`：单独转换后的人声。

也可以直接运行 `python audio_main.py`。

视频模式和音频模式相互独立；不传 `--mode` 时默认运行原有视频流程。

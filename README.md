# ai_cover

对视频里的声音做 AI 翻唱：提取音频 → 人声/伴奏分离(Demucs) → 人声克隆(RVC) → 混音 → 合成回视频。

## 安装 (Windows + NVIDIA)
1. 安装 ffmpeg 并加入 PATH
2. 按 CUDA 版本从 https://pytorch.org 安装 torch
3. `pip install -r requirements.txt`

## 使用
编辑 `config.yaml`（视频路径、RVC 模型 .pth/.index、变调等），然后：

    python main.py
    python main.py -c other.yaml

产物在 `output/<视频名>/`：`01_audio.wav`、`demucs/…`、`03_vocals_converted.wav`、`04_mix.wav`、`<视频名>_cover.mp4`。
`resume: true` 时已存在的中间文件会跳过，改了参数想重跑某一步，删掉对应文件即可。

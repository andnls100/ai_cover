import subprocess


def run(cmd: list[str]) -> None:
    print(">>", " ".join(str(c) for c in cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"命令执行失败 (exit {result.returncode}):\n{result.stdout[-3000:]}")

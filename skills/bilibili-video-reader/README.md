# Bilibili Video Reader

一句话安装：

```text
帮我安装这个 skill：https://github.com/vinsonhi/AI-Skills/tree/main/skills/bilibili-video-reader
```

如果你的 Codex 支持从 GitHub 路径安装，直接说上面这句就够了。

## 你会得到什么

这是一个让 Codex 真正“读”B 站视频内容的 skill。它不会只看标题、简介或评论，而是下载音频、在本地转写语音，再基于 transcript 总结视频观点。

适合用来：

- 总结 B 站长视频
- 提取嘉宾观点和论证链路
- 做投资/商业/技术视角的二次整理
- 生成逐字稿或要点摘要
- 在视频标题党、简介太少时读取真实内容

默认会把音频和中间文件放在临时目录，结束后自动清理，不污染你的工作区。

## 怎么使用

直接把视频链接发给 Codex：

```text
帮我读一下这个 B 站视频：https://www.bilibili.com/video/BV...
```

也可以指定输出风格：

```text
帮我总结这个视频，重点看商业判断和可以落地的建议
```

```text
帮我把这个视频压成 5 条关键观点，再给一句话结论
```

```text
帮我提取逐字稿，并标出最值得引用的几段
```

## 它会怎么做

这个 skill 默认会让 Codex：

1. 用脚本下载视频音频到临时目录。
2. 用 `ffmpeg` 转成适合转写的 wav。
3. 用本地 `whisper.cpp` 模型转写语音。
4. 从 transcript 里提炼观点，而不是用页面元信息代替内容。
5. 自动清理临时音频、wav 和转写中间文件。

手动运行示例：

```bash
python3 ~/.codex/skills/bilibili-video-reader/scripts/read_bilibili_video.py "https://www.bilibili.com/video/BV..."
```

排查问题时才保留临时文件：

```bash
python3 ~/.codex/skills/bilibili-video-reader/scripts/read_bilibili_video.py "https://www.bilibili.com/video/BV..." --keep-temp
```

## 准备工作

需要这些本地工具：

- `yt-dlp`
- `ffmpeg`
- `whisper-cli` from `whisper-cpp`
- 本地 whisper.cpp 模型

安装示例：

```bash
brew install ffmpeg whisper-cpp
/opt/homebrew/bin/python3.11 -m pip install --user yt-dlp
```

默认模型路径：

```text
~/.agent-reach/models/ggml-base.bin
```

如果模型不存在，可以下载：

```bash
mkdir -p ~/.agent-reach/models
curl -L -o ~/.agent-reach/models/ggml-base.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin
```

## 输出会长什么样

最终回答会是可读的总结，不会把原始 transcript 直接糊给你：

```markdown
这期视频的主线很清楚，核心是在讲 MiniMax 财报 + 中国大模型为什么正在变成“制造业”逻辑。

关键点我给你压成 5 条：

- 中国正在把 AI 做成低成本、高供给、可规模化的制造业，而不只是硅谷那种“冲 AGI 叙事”的高估值故事。
- token 成本快速下降会改变工作流设计。以前很多 AI 用法不是没人想要，而是太贵。
- MiniMax 的竞争力不一定是“绝对最强”，而是便宜、够用、压缩做得狠。
- 用 AI 不能再用“省 token”的穷人思维。重要任务应该把 token 当生产资料投入。
- AI 的商业价值越来越像雇人：关键不是会员费，而是这些 token 能不能稳定换来产出。

一句话结论：

中国大模型正在从“讲故事的 AI”转向“低成本、可量产、能替代部分脑力劳动的 AI 基础设施”。
```

## 注意事项

- 优先基于 transcript 总结，不用标题和简介冒充“看过视频”。
- 如果视频本身有可用字幕，可以用字幕，但仍要避免把下载文件放进工作区。
- 临时文件默认清理；只有调试时使用 `--keep-temp`。
- 长视频转写会比较慢，取决于本机性能和模型大小。

## 文件

- `SKILL.md`：核心读取流程
- `scripts/read_bilibili_video.py`：下载、转写和清理脚本
- `agents/openai.yaml`：agent 配置

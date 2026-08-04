# 火山引擎 Seed-TTS 2.0 配音规范

## 官方链接

- 单向流式语音合成 HTTP：<https://www.volcengine.com/docs/6561/2528925?lang=zh>
- 双向流式语音合成 WebSocket：<https://www.volcengine.com/docs/6561/2532486?lang=zh>
- 音色与产品动态：<https://www.volcengine.com/docs/6561/162929?lang=en>

API 文档会更新；接口异常或参数变化时，先重新读取官方文档，不要猜参数。

## 默认配置

- Endpoint：`https://openspeech.bytedance.com/api/v3/tts/unidirectional`
- Header `X-Api-Key`：来自环境变量 `VOLC_API_KEY`
- Header `X-Api-Resource-Id`：`seed-tts-2.0`
- Header `X-Api-Request-Id`：每次请求生成新的 UUID
- Speaker：`zh_female_vv_uranus_bigtts`
- 音频格式：MP3
- 采样率：24000 Hz
- `speech_rate`：先从 8–15 试起，再按实际时长调整
- `loudness_rate`：0

官方音色信息中，`zh_female_vv_uranus_bigtts` 对应 TTS 2.0 的 Vivi 2.0 音色。

## 凭证安全

- 首次使用向用户索取 API Key，或让用户自己设置 `VOLC_API_KEY`。
- 不在命令回显、错误日志和最终回答中重复显示完整 Key。
- 不把 Key 写入仓库、配置文件、shell 脚本或示例。
- 不提交生成的私密凭证文件。

## 生成与时间轴

优先按场景分段生成：

```bash
python3 scripts/tts_volc.py segment-01.txt segment-01.mp3 --speech-rate 12
```

生成后用 `ffprobe` 获取每段真实时长，再排视频。不要按字数估时后强制切画面。

建议处理顺序：

1. 生成短句试听，确认音色、语速和 `AI` 等缩写发音；
2. 分段生成正式配音；
3. 检查每段首尾是否吞字；
4. 在段与段之间保留自然停顿；
5. 对齐画面后再混入背景音乐和音效；
6. 最终检查没有重叠、抢跑或切尾。

如果需要更快，优先精简逐字稿；如果需要更慢，优先增加页面停留。不要依赖大幅 time-stretch。

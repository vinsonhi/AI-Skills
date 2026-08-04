# HyperFrames 产品宣传视频 Skill

一句话安装：

```text
帮我安装这个 skill：https://github.com/vinsonhi/AI-Skills/tree/main/skills/hyperframes-product-promo-video
```

如果你的 Codex 支持从 GitHub 路径安装，直接说上面这句就够了。

## 你会得到什么

这是一个用真实产品录屏、截图、GIF 和文案制作中文产品宣传视频的 Skill。它会先和你确认逐字稿、分镜、素材顺序和时间，再调用 HyperFrames 生成视频，不会一上来就直接渲染。

用户没有另行指定时，会直接套用已经验证过的“抖音直播机构版 Fluent 产品宣传片”预设，不需要你重新描述风格：蓝白渐变、亚克力半透明框架、柔和层叠光影、企业生产力工具质感、固定中心构图、真实 UI 大面积呈现、底部亚克力字幕和顺滑转场。

默认包含：

- 真实 UI 强参考，不把产品页面重画成抽象 dashboard
- 中文普通话产品配音
- 产品宣传感背景音乐和轻量音效
- 右下角常驻“抖音直播行业产品团队”白色水印
- 2 秒“直播服务平台·机构版”品牌结束页
- 配音、画面切换和页面停留的逐段对齐

Skill 内置默认产品宣传配乐，以及页签、卡片、AI 展开和 Logo 收束音效。除非你明确要求无配乐，否则会自动加入并按人声优先的规则混音，避免做成只有配音的“干视频”。

点击高亮默认不加。需要高亮时，你要提供圈出点击位置的关键帧截图或时间码，Skill 才会添加。

## 怎么使用

把物料和需求发给 Codex：

```text
用产品宣传视频 skill，基于我提供的两个录屏和三张截图做一条功能介绍视频。先给我逐字稿和逐镜脚本，我确认后再生成。
```

第一次使用时，Codex 会先检查：

1. 是否安装了 HyperFrames 插件；
2. 是否已有火山引擎豆包语音 API Key；
3. 录屏、截图、文字、Logo 和素材对应关系是否齐全。

HyperFrames 插件：

```text
plugin://hyperframes@openai-curated-remote
```

火山引擎语音 API 文档：

<https://www.volcengine.com/docs/6561/2528925?lang=zh>

API Key 只用于当前环境调用，不应写入项目或 Git 仓库。

## 工作流程

1. 你提供录屏、截图、GIF、功能文字和品牌物料。
2. Codex 检查素材并给出完整逐字稿和带时间码的逐镜脚本。
3. 你确认或修改脚本。
4. 你明确确认后，Codex 才生成火山配音并制作 HyperFrames 视频。
5. Codex 检查配音不重叠、画面不抢跑、水印和结束页正确，再交付 MP4。

## 品牌规范

正片右下角固定使用纯白极简水印：

```text
[抖音 Icon] 抖音直播行业产品团队
```

结束页固定停留 2 秒：

```text
直播服务平台·机构版
抖音直播-行业产品团队出品
```

Skill 已包含正确的抖音 Icon 和机构版 Logo，不需要重新截图或手绘。

结束页使用独立的自包含模板，蓝白背景从第一帧起完全不透明，只让品牌卡片和文字进入，避免上一段产品页面或其他视频素材穿透。

## 点击高亮

默认关闭。如果需要，请提供：

- 圈出按钮或入口的截图；
- 对应时间码；
- 每一步应该点击哪个控件。

Codex 会让高亮在点击前出现并留出识别时间，不会猜坐标，也不会默认把所有点击都标红。

## 文件

- `SKILL.md`：完整制作流程和门禁
- `references/brand-spec.md`：水印与结束页规范
- `references/default-video-style.md`：默认 Fluent 画面、字幕、动效和节奏规范
- `references/audio-style.md`：配乐、音效、配音和混音规范
- `references/volcengine-tts.md`：火山配音设置
- `scripts/tts_volc.py`：Seed-TTS 2.0 配音脚本
- `assets/`：默认 DESIGN 模板、产品宣传配乐、UI 音效、标准抖音水印 Icon 和机构版 Logo
- `assets/templates/brand-end-card.html`：不会透出上一段画面的自包含 2 秒结束页模板
- `agents/openai.yaml`：Agent 展示配置

---
name: hyperframes-product-promo-video
description: Create or revise Chinese product launch, feature introduction, and operation tutorial videos from real UI recordings, screenshots, GIFs, copy, logos, and voiceover requirements. Use when the user wants a consistent HyperFrames-based Microsoft Fluent product promo with real UI as the visual truth, bundled product-launch music and UI sound effects, script confirmation before rendering, Volcengine Seed-TTS 2.0 Mandarin narration, the standard Douyin Live Industry Product Team watermark and end card, and optional user-specified click highlights.
---

# HyperFrames 产品宣传视频

把用户提供的真实录屏、截图、GIF、文字和品牌物料制作成中文产品宣传或操作讲解视频。真实产品 UI 是视觉主体，不要把素材重新设计成抽象 dashboard。

## 默认成片预设

除非用户明确指定其他风格，必须使用本 Skill 的“抖音直播机构版 Fluent 产品宣传片”预设，不得临时自由发挥成另一套风格：

- 画面规范：[references/default-video-style.md](references/default-video-style.md)
- 声音与混音：[references/audio-style.md](references/audio-style.md)
- 项目视觉模板：[assets/templates/DESIGN.md](assets/templates/DESIGN.md)
- 品牌规范：[references/brand-spec.md](references/brand-spec.md)

新建 HyperFrames 项目时，将 `assets/templates/DESIGN.md` 复制到项目根目录作为 `DESIGN.md`，再根据用户真实 UI 的原始品牌色做有限调整。禁止只写一句“Microsoft Fluent 风格”就开始制作。

默认成片特征：蓝白渐变画布、亚克力半透明框架、柔和层叠光影、企业生产力工具质感、固定中心构图、真实 UI 大面积呈现、平滑转场、底部亚克力字幕、专业普通话配音、轻量但有推进感的产品宣传配乐、克制的 UI 操作音效、右下角团队水印和 2 秒品牌结束页。

如果用户没有指定画幅、时长或渠道，在脚本提案中给出 `1920×1080、30fps、约 25–45 秒` 的建议值并等待确认；不要在用户确认前把建议当成最终规格。

## 硬门禁

必须按以下顺序工作：

1. 收齐并检查物料。
2. 先交付逐字稿和逐镜脚本。
3. 等用户明确确认。
4. 确认后才生成配音和视频。

用户没有明确说“可以做”“开始生成”或同等意思时，不得开始合成、渲染正式视频。用户修改文案或节奏后，先更新逐字稿和脚本，再次等待确认。

## 首次使用检查

### HyperFrames

先检查当前环境是否已有 HyperFrames 插件及对应 skills/CLI：

- `hyperframes:hyperframes`
- `hyperframes:hyperframes-cli`
- 可运行的 `npx hyperframes`

若缺失，暂停制作并让用户安装：

```text
请先安装 HyperFrames 插件：plugin://hyperframes@openai-curated-remote
```

安装完成后再继续。制作和验证时必须遵守 HyperFrames skill 的最新说明。

### 火山引擎配音

首次使用先检查 `VOLC_API_KEY`。若不存在，向用户索取火山引擎豆包语音 API Key，并给出官方文档链接：

```text
请先参考火山引擎豆包语音 API 文档创建 API Key：
https://www.volcengine.com/docs/6561/2528925?lang=zh

创建后请把 API Key 提供给我，或在本机设置环境变量 VOLC_API_KEY。
```

不要把 Key 写入 `SKILL.md`、脚本、日志、项目文件、README 或 Git。只通过当前进程环境变量使用。详细调用规范见 [references/volcengine-tts.md](references/volcengine-tts.md)。

## 第一步：收集物料

开始时主动让用户提供：

- 产品录屏：MP4、MOV、GIF；
- 页面截图和关键状态截图；
- 功能说明、卖点、必须出现的文字；
- 产品 Logo、团队署名及品牌限制；
- 希望的时长、画幅、发布渠道；
- 已有配音、背景音乐或音乐方向；
- 每份素材对应哪个功能、允许出现在哪个段落。

如果用户已给齐，不重复询问。若缺少的内容不影响脚本，可先做合理假设并明确标注；若会改变叙事或素材对应关系，先向用户确认。

对每个视频读取分辨率、帧率、时长和音轨；抽取首帧、尾帧及关键帧，确认真实 UI 布局、表格层级、卡片结构、字体比例和交互位置。

## 第二步：先交逐字稿和脚本

第一次交付只包含脚本，不生成视频。至少给出：

1. 视频定位和一句话主线；
2. 建议总时长；
3. 完整配音逐字稿；
4. 带时间码的逐镜脚本；
5. 每段使用的具体素材；
6. 屏幕字幕、转场、音乐和音效说明；
7. 仍需用户确认的内容。

脚本中的音乐与音效不能只写“科技感 BGM”。必须按 [references/audio-style.md](references/audio-style.md) 标注开场建立、功能推进、重点强调和结尾收束，并写出哪些可见点击需要 `tab.wav`、`card.wav` 或 `ai-open.wav`。

逐镜脚本使用此结构：

| 时间 | 画面与素材 | 配音逐字稿 | 屏幕文字 | 音乐/音效 |
| --- | --- | --- | --- | --- |

节奏规则：

- 画面切换必须等对应句子讲完，禁止配音未结束就跳到下一功能；
- 禁止两段配音重叠；
- 关键页面出现后至少保留足够阅读时间；
- 简单入口可以快，但多步骤操作必须让观众看清点击位置；
- 逐字稿要口语化、信息密度高，避免把所有指标名机械念完；
- 英文缩写按用户要求朗读。`AI` 默认保留连续写法，不在 A 和 I 之间加空格或停顿，并先生成短句试听验证。

结尾必须明确问用户是否确认逐字稿、画面顺序和总时长。只有得到明确确认才进入下一步。

## 第三步：生成配音并锁定时间轴

默认使用：

- 模型资源：`seed-tts-2.0`
- Speaker：`zh_female_vv_uranus_bigtts`
- 语言：中文普通话
- 语气：专业、清晰、有产品发布感，不过度广告腔

使用 [scripts/tts_volc.py](scripts/tts_volc.py) 生成配音：

```bash
export VOLC_API_KEY='用户提供的 Key'
python3 scripts/tts_volc.py script.txt narration.mp3 --speech-rate 12
```

优先按场景分段生成，保留每段独立音频，便于精确对齐。生成后读取实际音频时长，再锁定画面时间轴；不要先写死画面时长再强塞配音。

若配音太快、吞字或缩写发音不清：

- 优先重写句子或重新生成；
- 小幅调整 `speech_rate`；
- 不用极端倍速拉伸掩盖问题；
- 不让两个语音片段重叠；
- 调整后重新检查功能名、数字、英文缩写和停顿。

## 第四步：用 HyperFrames 制作

先读取项目 `DESIGN.md`；没有则复制 [assets/templates/DESIGN.md](assets/templates/DESIGN.md)。完整读取并执行 [references/default-video-style.md](references/default-video-style.md) 与 [references/audio-style.md](references/audio-style.md)。将真实录屏和截图作为强视觉参考：

- 保留真实 UI 构图、页面比例、表格层级、卡片结构和产品配色；
- 不虚构按钮、数字、页面和操作；
- 不把真实后台改造成抽象科技 dashboard；
- 不混用用户指定不能混用的素材；
- 镜头移动、转场和景深不能影响 UI 可读性；
- 画面运动优先发生在 UI 主体内部。

需要 first frame / last frame 时，从原视频自动抽取合适帧；支持 reference video 的工作流中，将对应录屏绑定到对应段落。

### 默认音乐与音效资产

默认复制以下资产到项目中，并按 [references/audio-style.md](references/audio-style.md) 混音：

- `assets/audio/product-promo-music.wav`：默认产品宣传配乐；
- `assets/audio/tab.wav`：页签、轻按钮点击；
- `assets/audio/card.wav`：卡片展开、页面结果出现；
- `assets/audio/ai-open.wav`：AI 总结、智能结果展开；
- `assets/audio/logo-sting.wav`：结束页收束音。

音乐不是可有可无的装饰。默认必须加入，除非用户明确要求无配乐。音乐应有可感知的产品发布推进感，但不能压住人声；可见的关键操作默认加入少量 UI 音效，禁止每次鼠标移动都发声。

## 默认品牌规范

品牌规范默认开启，除非用户明确要求换品牌或不加。

### 右下角常驻水印

使用本 Skill 的 [assets/douyin-icon-white.png](assets/douyin-icon-white.png)，文字固定为：

```text
抖音直播行业产品团队
```

必须遵守 [references/brand-spec.md](references/brand-spec.md) 的位置、尺寸、透明度、阴影和禁用样式。水印只出现在正片；进入结束页后隐藏。

### 两秒结束页

正片结束后追加 2 秒品牌页。使用 [assets/live-service-platform-institution.png](assets/live-service-platform-institution.png)，署名固定为：

```text
抖音直播-行业产品团队出品
```

结束页视觉和动效必须遵守 [references/brand-spec.md](references/brand-spec.md)。不要重绘或替换 Logo。

优先复制并使用 [assets/templates/brand-end-card.html](assets/templates/brand-end-card.html) 作为独立子合成：将模板放到项目 `compositions/brand-end-card.html`，将 Logo 复制为项目 `assets/brand/live-service-platform-institution.png`，将收束音复制为项目 `assets/audio/logo-sting.wav`。结束页必须自包含，禁止从另一条成片截取带有底层业务页面的结束片段。结束页根画布从第一帧起必须 100% 不透明；只能让卡片、Logo、分隔线和署名淡入，禁止对整个结束页根节点做 `opacity: 0 → 1` 动画。

## 可选：点击高亮

点击高亮默认关闭。不要因为视频是教程就自动添加。

只有用户明确要求时才开启，并要求用户提供以下任一种标注：

- 在关键帧截图上用圈、框或箭头标出点击位置；
- 提供时间码和点击区域；
- 提供每一步“点哪里”的截图序列。

不要凭印象猜坐标。每个高亮都应：

- 在点击前留出识别时间；
- 覆盖真实控件，不偏移；
- 高亮结束后再切页面；
- 必要时配合点击音效；
- 不长期遮挡 UI 内容。

推荐样式为醒目的红色粗框、黄色外圈和小型“点这里”标签；不要置灰整张底图。用户可要求减弱或增强。

## 验收与交付

渲染前：

1. `npx hyperframes lint`
2. `npx hyperframes check` 或 `inspect`
3. 在每次功能切换、点击、配音起止、Logo 出现处抽帧检查

渲染后：

- 用 `ffprobe` 核对分辨率、帧率、时长和音轨；
- 完整检查配音无重叠、无截断、无抢跑；
- 确认水印在正片全程可见、未进入结束页；
- 确认结束页完整停留 2 秒；
- 在结束页切入帧、切入后 `0.1s` 和 `0.3s` 分别抽帧，确认没有上一段 UI、手机轮廓、截图或视频残影；
- 确认 Logo 使用原始资产；
- 确认音乐没有盖过人声；
- 确认正片不是“只有配音的干视频”，音乐在普通扬声器上可感知且有推进；
- 确认配乐开头、功能段和结束页的能量变化符合 `audio-style.md`；
- 确认字幕、UI 框架、背景、阴影和转场符合默认 Fluent 预设；
- 对关键点击和转场抽帧复核。

最终交付新文件，不覆盖用户已确认的旧版本。文件名应包含版本特征，例如：

```text
产品名-51s-团队水印结束页版.mp4
```

---
name: self-daily-briefing-skill
description: "中文 Morning Brief skill。用于生成综合早报、财经早报、科技早报、AI 深度日报，以及美股自选股票早报。用户说“牛马牛马”、'早报'、'美股股票早报'、'股票日报' 时使用。"
---

# 中文 Morning Brief skill

用于生成中文日报。默认直接在对话中输出日报内容；只有用户明确要求 PDF、Markdown、HTML、保存文件或其他格式时，才导出对应文件。

## 严格规则

- 使用本 skill 的任何功能前，先检查 `instructions/local_onboarding_state.json`。如果文件不存在、解析失败、或 `onboardingComplete` 不是 `true`，必须先运行完整 onboarding；不要直接生成日报，也不要只展示菜单后跳过 onboarding。兼容旧安装中的 `instructions/.local_onboarding_state.json`，但新写入统一使用非隐藏文件。
- 首次 onboarding 完成后再继续用户的原始任务。如果用户只是说“牛马牛马”，onboarding 后展示菜单；如果用户是第一次直接要求生成日报，onboarding 后继续生成对应日报。
- 后续使用时不要重复 onboarding；只有用户明确说“重新设置日报偏好”“修改语言/股票/关注主题”时才重新进入设置流程。
- 如果用户没有指定日报类型，默认生成“标准日报”。
- 默认输出渠道是当前对话：直接给出完整日报正文，不保存文件，不让用户跳转找文件。
- 如果用户没有指定日报类型，默认生成“标准日报”并直接在对话里输出。
- 只有用户明确要求 PDF、Markdown、HTML、保存文件、原始数据或过程文件时，才生成并交付对应文件。
- 如果用户要求 PDF，使用本文的 PDF 导出规则；PDF 导出失败时，不要把 Markdown/HTML/低保真 PDF 冒充最终产物，必须明确说明 PDF 被阻塞。
- 如果用户要的是“标准日报”，默认生成包含综合/财经/科技/AI 深度/美股的完整日报；如果用户只要某个模块，再单独生成对应模块。
- 生成标准日报前，必须先生成或读取各板块源文件，再按固定顺序组装。
- 生成标准日报时，`general_report.md`、`finance_report.md`、`tech_report.md`、`ai_daily_report.md` 这四个板块把源文件内容视为最终内容，直接拼接，不要二次改写、二次摘要、重写观点。
- 标准日报展示时，为避免双层标题重复，保留标准日报稿里的外层章节标题，去掉各源文件自身的首个 `# 标题` 行后再拼接正文。
- 标准日报稿的章节标题应保留视觉识别，推荐使用带 emoji 的外层标题，例如 `🌅 一、综合早报`、`💰 二、财经早报`。
- 标题层级应保持一致：标准日报稿主标题用 `#`，五个外层章节用 `##`，章节内部的小分组和“数据缺口”统一用 `###`。
- 标准日报稿主标题后不要先放元信息列表；开头必须直接进入 `## 🌅 一、综合早报`。
- 生成时间、数据窗口、合并来源、说明等元信息统一放到全文末尾，并用 Markdown 引用块表示。
- 标准日报稿允许新增的内容只有：
  - 顶部总标题；
  - 文末引用式元信息块（生成时间、数据窗口、合并来源、说明）；
  - 板块分隔符；
  - 美股股票早报板块；
  - 明确的数据缺口说明。
- 如果某一板块已有当天源文件，就优先复用该源文件；不要为了“统一文风”重写。
- 如果用户直接给了某个板块的完整版本，按用户版本原文覆盖该板块，不要改写措辞。
- 缺数据就写缺口，不补推断性内容。
- 综合/财经/科技这类“今天发生了什么”的板块，默认只收当天新增事件或当天有明确新进展的延续事件。
- 当前默认时效门槛是**最近 24 小时**；不满足这个窗口的条目不得因为“缺内容”而自动补进今天成稿。
- 如果某条信息只是前几天已经写过的旧闻、今天没有明确增量，就不能伪装成今天头条；要么删掉，要么明确标记为“延续跟踪”。
- 生成综合早报前，必须对最近 3 天内已交付的同类成稿做标题级去重检查；如果同一事件已经在近几天做过主条且今天没有实质新进展，不得再次放进 `全网速览` 前列。
- 每个板块不要求凑固定条数；宁可直接写 `### 📌 数据缺口`，也不要回填 24 小时窗口之外的旧稿。
- PDF 要尽量保留 Markdown 原始阅读结构，优先走“Markdown -> HTML 阅读页 -> 浏览器导出 PDF”，不要自创杂志式重排。
- HTML 导出 PDF 的正确链路固定为：`Markdown -> 完整 HTML 文件 -> 浏览器直接打开该 HTML 页面 -> 浏览器打印 PDF`。
- PDF 导出优先使用当前 Agent 环境可用的浏览器打印能力，例如系统浏览器、Agent 提供的浏览器工具、Chromium 或 Chrome；不要在浏览器链路实际可用时误判为“浏览器不可用”。
- 如果没有可用浏览器打印链路，才允许把 PDF 标记为“被阻塞”。
- 禁止把整篇 HTML 用 `data:` URL 注入浏览器后再打印长文 PDF；这条链路会发生静默截断，导致后半篇缺页。
- 禁止把 `reportlab` 当作 HTML/Markdown 阅读页的默认 PDF 导出器；它只能用于程序化排版文档，不能保证与 HTML 阅读结构一致。
- 如果浏览器直打链路不可用，应明确报错说明卡点，并把 PDF 状态标记为“未完成 / 被阻塞”；不要静默切换到低保真方案后继续交付。
- 对 Morning Brief 这类要求 HTML 保真的交付，`reportlab` fallback 不算成功交付，只能算失败占位。
- 任何日报流程如果启动了 `http.server`、headless browser、Playwright、MCP、或其他临时后台进程，交付前必须主动做收尾，确保这些进程在任务结束后退出；不能把清理动作留给下次重启。
- PDF 导出完成后，必须核对 HTML 和 PDF 内容是否完整一致，至少完成以下检查：
  - `pdfinfo` 检查页数是否与内容规模相符，不能异常偏少。
  - `pdftotext` 提取 PDF 尾部文本，并与 HTML 尾部文本逐段对比，确保最后一个板块完整出现。
  - `pdftoppm` 渲染最后 1-2 页 PNG，人工确认末页不是空白页、截断页、或停在中间章节。
  - 只看首页或前两页不算验收通过。
- 参考示例：
  - `examples/merged_daily_report_2026-03-11.md`
  - `examples/merged_daily_report_2026-03-11.pdf`

## 安装

最简单的说法：

```text
帮我安装这个 skill：https://github.com/vinsonhi/AI-Skills/tree/main/skills/self-daily-briefing-skill
```

如果对方支持 GitHub 仓库路径安装，通常这句话就够了。

如果运行环境不支持自动安装，可以下载本目录，并放到对应 Agent 的 skills 目录；安装后刷新或重启 Agent，让它重新索引 skills。

### 首次安装 onboarding

只在首次安装后的第一次使用时做 onboarding。后续生成日报时不要重复询问；只有当用户明确说“重新设置日报偏好”“修改语言/股票/关注主题”时才重新进入设置流程。

执行任何菜单或日报任务前，先检查本地状态文件：`instructions/local_onboarding_state.json`。如果 `onboardingComplete: true`，直接进入用户要的日报任务；否则必须先完成 onboarding。旧版本隐藏状态文件 `instructions/.local_onboarding_state.json` 只作为兼容读取。

首次 onboarding 按 4 步走：

1. **自我介绍**：说明这个 skill 会生成综合、财经、科技、AI 深度和美股自选 Morning Brief。
2. **语言偏好**：询问中文、英文或双语；默认中文，并保留关键英文产品名、论文名和公司名。
3. **股票跟踪偏好和额外关注**：询问美股 ticker 列表，以及用户想长期关注的公司、产品、人物或主题。如果用户说没有，告诉用户会先用 Mag 7（AAPL、MSFT、NVDA、AMZN、GOOGL、META、TSLA）作为默认名单，以后随时能改。
4. **展示信息源并询问是否运行一遍**：展示 X builders、播客、官方博客等默认源，问用户是否现在先跑一版看效果。

如果用户给出 ticker 列表，把列表写入**本地已安装 skill** 的 `instructions/us_stocks_watchlist_default.txt`，一行一个 ticker；如果用户没有给，使用公开版本内置的 Mag 7 默认名单，不要留空。

可复用脚本：

```bash
python3 scripts/onboarding.py
python3 scripts/onboarding.py --language zh --watchlist "NVDA, AMD, MSFT" --interests "Claude Code, AI 搜索, 机器人"
python3 scripts/onboarding.py --accept-defaults
python3 scripts/onboarding.py --force
```

非交互环境中，如果没有拿到用户偏好，不要把 onboarding 标记为完成；应先把四步问题展示给用户。只有用户回答，或用户/调用方明确接受默认设置时，才写入完成状态。

## 可用日报

### 1. 综合早报
- 适用场景：要看今天科技、创投、社交和金融的大盘动态
- 信息源：
  - Hacker News
  - GitHub Trending
  - 36Kr
  - Product Hunt
  - Weibo
  - WallStreetCN
  - Tencent News

### 2. 财经早报
- 适用场景：要看宏观、市场、板块和加密
- 信息源：
  - WallStreetCN
  - 36Kr 财经
  - Tencent 财经
  - Hacker News 金融/加密关键词

### 3. 科技早报
- 适用场景：要看 AI、开发工具、创业产品
- 信息源：
  - GitHub Trending
  - Hacker News
  - Product Hunt
  - 36Kr

### 4. AI 深度日报
- 适用场景：要看前沿论文和 AI 行业观点
- 信息源：
  - Hugging Face Papers
  - X Fixed AI Builders（登录个人 X 账号后抓取固定 builder 账号列表的今日热帖）
  - AI Podcasts（6 档顶级 AI 播客，默认 14 天窗口）
  - AI Official Blogs（AI 公司官方博客）
  - ChinAI
  - Ben's Bites
  - One Useful Thing
  - Memia
  - Interconnects

#### AI 深度日报里的 X 板块规则

- X 不是匿名抓公开搜索，也不再依赖 `Following` 或 `For you` 推荐流，而是复用用户登录态打开固定 builder 账号列表逐个查看。
- 固定账号列表见 `instructions/x_ai_accounts.txt`，按 `follow-builders` 的 builder 取向维护，关注真实做产品、做研究、经营公司的人，而不是泛搬运账号。
- 对这类登录态来源，默认先复用用户已经登录 X 的浏览器会话或运行环境提供的等价登录态，不要直接用匿名搜索、推荐流、无状态浏览器替代固定账号列表。
- 可接受的登录态方式包括：
  - Agent 提供的已登录浏览器会话；
  - 用户授权的浏览器 profile / cookie bridge；
  - 用户在当前浏览器自动化环境中手动登录后的会话；
  - 其他能稳定访问固定账号主页的等价机制。
- 不要把“某个隔离浏览器没登录”误判成“用户 X 登录态失效”。只有确认当前可用登录态都无法访问 X 后，才允许标记为登录态失效。
- 必须逐个检查固定列表中的账号主页；不要用推荐流替代固定列表，也不要只看用户自己的关注流。
- 数据窗口默认只看最近 24 小时。
- 热度排序不能只看点赞，要综合 replies / reposts / likes / views / bookmarks。
- 跨账号排序时优先选择“最近 24 小时 + 明确 AI/模型/产品/研究/产业信号 + 高互动”的内容；账号身份只能作为背景，不能替代事实来源。
- 如果推文里带外链，优先打开外链正文再写 `Summary` 和 `Deep Dive`，不要只复述发帖文案。
- 如果没有外链，再基于推文本身做摘要和解读。
- 最终输出仍要遵守日报格式：`Source`、`Time`、`Summary`、`Deep Dive`。
- 缺正文就写缺口，不要把猜测当事实。
- 如果 X 或其他需要登录的来源出现登录过期、登录页、扫码、验证码、或权限校验，不能把它当作普通“数据缺口”直接跳过。
- 在判定“登录态失效”之前，必须先验证当前运行环境可访问的真实登录态；如果只是临时 profile、隔离浏览器或无状态 context 没有登录，不算用户登录态失效。
- 只有在可用登录态都失效时，才允许明确标记为“登录态失效”，并停在可恢复步骤上。
- 登录失效时，不能私自改用匿名抓取、公开搜索、替代站点、或完全不同的技术路线来冒充同一数据源。

#### AI 播客和官方博客规则

- 播客列表见 `instructions/ai_podcasts.txt`，默认包含 Latent Space、Training Data、No Priors、Unsupervised Learning、The MAD Podcast with Matt Turck、AI & I by Every。
- 播客默认窗口是最近 14 天；播客不是日更源，不能套 24 小时硬过滤，也不要因为当天没有新节目就写大段缺口。
- 播客摘要应先给一句 `The Takeaway`，再说明嘉宾是谁、为什么值得关注，并优先提炼反直觉、具体经验、产品判断和研究路线判断。
- 官方博客列表见 `instructions/ai_official_blogs.txt`，默认包含 Anthropic Engineering 和 Claude Blog。
- 官方博客摘要要优先写清核心公告、产品能力、研究发现、API/能力变化、关键数字或 benchmark；没有原文链接的内容不要写入日报。

#### 登录态浏览器执行约定

- 验证 X 会话时，优先确认当前可用登录态是否能访问 `https://x.com/home` 和固定账号主页。
- 如果运行环境支持读取浏览器 cookie，可检查 `x.com` 的 `auth_token`、`ct0` 等登录 cookie；如果不支持，应让用户在可用浏览器环境中完成登录。
- 可复用脚本：
  - `scripts/real_chrome_helpers.py`
  - `scripts/check_x_personal_chrome_session.py`
  - `scripts/extract_x_accounts_with_personal_chrome.py`
  - `scripts/export_pdf_with_system_chrome.sh`
  - `scripts/filter_recent_brief_items.py`
- 上述 Chrome helper 脚本是 macOS + Google Chrome 的参考实现；其他 Agent 或运行环境可以用等价浏览器会话、cookie bridge、浏览器 MCP 或人工登录流程替代。
- 使用上述脚本或等价工具后，若本轮任务额外拉起了 headless browser、本地 HTTP server、Playwright MCP、或其他浏览器自动化辅助进程，结束前必须再次检查并关闭它们。

### 5. 美股股票早报
- 适用场景：要看自选股票的最新价格、涨跌、驱动因素和重要新闻
- 默认观察名单：见 `instructions/us_stocks_watchlist_default.txt`；公开版本默认内置 Mag 7（AAPL、MSFT、NVDA、AMZN、GOOGL、META、TSLA），用户可在 onboarding 或后续对话中改成自己的名单
- 信息源：
  - 最新价格：优先用 `web.finance`
  - 涨跌幅：用最新价和昨收价计算
  - 驱动因素：公司 IR、财报、官方博客、官方新闻稿
  - 重要新闻：优先 Reuters，其次公司官网和权威媒体
- 如果某个网页源、爬虫链路或公开 API（例如 Yahoo 页面 / 无认证接口）被频控、超时、或返回不稳定结果，**不能**直接把整块标成“拿不到”。
- 正确处理顺序是：
  1. 先用同一轮 `web.finance` 批量拿完整观察名单快照；
  2. 若 `web.finance` 本身失败，再尝试其他能一次性返回同轮价格的正式来源；
  3. 只有当“同轮批量快照”这件事本身确实失败时，才允许写数据缺口。
- 禁止因为单一来源失败，就回退成旧日报数字、逐只股票零散搜价、或连续几天都保留同样的“统一快照缺口”占位。
- 禁止把 Google Finance / Yahoo / 搜索结果页上的单页 quote 当作主价格源直接写进日报；这些来源只能用于排错，不可替代同轮批量快照。
- 时间口径规则：
  - 默认使用“生成时最新价快照”，不是自动回退成“上一交易日收盘后版本”。
  - 全部股票必须来自同一轮 `web.finance` 查询，不能混用不同时间点或不同来源的价格。
  - 报告顶部必须写清 `as of` 时间；如果美股正在交易，要明确写“盘中最新价快照”。
  - 只有当用户明确要求“收盘版 / 复盘版 / 对应美东某交易日收盘后版本”时，才允许按收盘口径写，并且标题和注释都要写清对应交易日。
  - 分析和一句话判断必须和同一轮价格口径一致；不能拿前一日收盘分析去解释当前盘中价格。
  - 按北京时间处理周末与周一：
    - 周六运行：默认允许使用刚结束的周五收盘口径，做统一价格对比和驱动分析。
    - 周日运行：默认不做价格对比，只收集信息、催化、官方新闻和下周观察点。
    - 周一运行：默认写最近一个美股交易日的盘后价格波动和信息更新，不能伪装成新的周一盘中价格。
  - 周日和周一如果采用最近一个交易日收盘口径，板块顶部必须明确写清对应的是哪个美东交易日。
- 二次校验规则：
  - 在写 Markdown 之前，必须校验最终要写入的 ticker、价格、涨跌额、涨跌幅、时间戳与主快照逐项一致。
  - 允许用第二来源做漂移检测，但第二来源只能用来发现异常，不能用来覆盖主快照。
  - 如果任一 ticker 出现明显漂移、交易所映射异常、时间戳显著不一致，整块股票板块必须阻断并写明待核实，不要继续生成方向判断。
  - 股票叙述和一句话判断只能在数值校验通过后生成。
  - 建议同时保存原始主快照；可复用 `scripts/validate_us_stocks_snapshot.py` 做批量校验。

## 日报格式示例

说明里要给出最终 Markdown 的样子，不只讲规则。每个日报板块至少放 1-2 个条目示例，最后用 `...省略` 表示完整报告会更长。

### 标准日报示例约束

```markdown
# Morning Brief | 2026-03-11

## 🌅 一、综合早报

### 🌍 全网速览

...这里直接贴 general_report.md 去掉首个 `# 标题` 后的正文...

---

## 📈 五、美股股票早报

...这里放美股正文...

---

> 生成时间：2026-03-11 14:58 CST  
> 数据窗口：以当天公开网页和统一行情快照为准。  
> 说明：综合/财经/科技/AI 深度板块以下均直接来自已有日报内容。  
> 合并来源：general_report.md / finance_report.md / tech_report.md / ai_daily_report.md + 美股股票早报
```

### 综合早报示例

```markdown
# 🌅 综合早报 | 2026-03-11

## 🌍 全网速览

#### 1. [百度智能云发布 DuClaw](https://example.com)
- **Source**: 36Kr | **Time**: 5秒前 | **Heat**: Unknown Heat
- **Summary**: 百度智能云发布零部署 OpenClaw 服务 DuClaw。
- **Deep Dive**: 💡 **Insight**: 云厂商开始把 Agent 竞争点从模型调用转向工作流和企业可用性。

#### 2. [Tony Hoare 去世](https://example.com)
- **Source**: Hacker News | **Time**: 13 hours ago | **Heat**: 🔥 1601 points
- **Hacker News**: [Discussion](https://news.ycombinator.com/)
- **Summary**: 社区回顾其在 quicksort、ALGOL 和 Hoare logic 上的长期贡献。
- **Deep Dive**: 💡 **Insight**: 形式化方法与程序正确性重新被工程圈重视。

...省略
```

### 财经早报示例

```markdown
# 💰 财经早报 | 2026-03-11

## 🌏 宏观与大盘

#### 1. [创业板涨 1%，光伏产业链爆发](https://example.com)
> **Time**: 2026-03-11 12:08 | **Impact**: 🟢 Bullish | **Heat**: Unknown
> **Summary**: A 股与港股科技成长板块走强，新能源链条领涨。
> **Deep Dive**: 💡 **Insight**: 资金回流成长板块，说明市场风险偏好正在修复。

#### 2. [设定美国财政部账户上限？](https://example.com)
> **Time**: 2026-03-11 11:29 | **Impact**: ⚪ Neutral | **Heat**: Unknown
> **Summary**: 报道讨论通过 TGA 工具影响流动性的可能性。
> **Deep Dive**: 💡 **Insight**: 这类政策工具会直接传导到美债、成长股和全球风险资产定价。

...省略
```

### 科技早报示例

```markdown
# 🤖 科技早报 | 2026-03-11

## 🚨 AI 前沿

#### 1. [Show HN: ClawSoc – Observe Your AI Agent in an AI Society](https://example.com)
- **Source**: Hacker News | **Time**: Today
- **Summary**: 开发者在“多 agent 社会”里观察 agent 行为。
- **Deep Dive**: 💡 **Insight**: 单 agent 评测正在失效，多体系统会成为下一代 agent 产品的关键壁垒。

## 🛠️ 开发者工具

#### 2. [promptfoo](https://github.com/promptfoo/promptfoo)
- **Source**: GitHub Trending | **Time**: Today
- **Summary**: 面向 prompts、agents 和 RAG 的测试与红队工具。
- **Deep Dive**: 💡 **Insight**: AI 工具链正在补齐 QA 和安全评测环节。

...省略
```

### AI 深度日报示例

```markdown
# 🧠 AI 深度日报 | 2026-03-11

## 🔬 SOTA Research

#### 1. [Omni-Diffusion：统一多模态理解与生成](https://example.com)
- **Source**: Hugging Face Papers | **Time**: 2026-03-11
- **Summary**: 用 masked discrete diffusion 统一多模态理解与生成任务。
- **Deep Dive**: Innovation：减少多模态系统“模型分裂”问题。
- **Deep Dive**: Impact：有机会降低多模态训练和部署的切换成本。

#### 2. [A Guide to Which AI to Use in the Agentic Era](https://example.com)
- **Source**: One Useful Thing | **Time**: Wed, 18 Feb 2026 01:45:41 GMT
- **Summary**: 讨论在 agentic 时代该如何选择不同 AI 工具。
- **Insight**: 💡 真正稀缺的是决策框架，而不是单个模型。

...省略
```

### 美股股票早报示例

```markdown
# 美股股票早报 | 2026-03-11

> 注：对应美东 2026-03-10 交易日收盘后版本。

| Ticker | 最新价 | 较昨收变动 | 一句话判断 |
|---|---:|---:|---|
| NVDA | $184.77 | +2.13 / +1.16% | GTC 预期继续支撑 |
| AMD | $203.23 | +0.56 / +0.28% | Meta 大单逻辑还在，日内偏稳 |

## NVDA
- **最新股价**：$184.77
- **较昨天**：+1.16%
- **关键因素**：GTC 预期、产品发布、生态合作。
- **重要新闻**：
  - [NVIDIA GTC 2026 官方预告](https://example.com)
- **我的判断**：会前预热行情仍在。

## AMD
- **最新股价**：$203.23
- **较昨天**：+0.28%
- **关键因素**：Meta 大规模 GPU 部署合作仍在支撑逻辑。
- **重要新闻**：
  - [AMD 与 Meta 扩大战略合作](https://example.com)
- **我的判断**：大涨后进入消化阶段。

...省略
```

## 输出规则

- 默认在当前对话直接输出日报正文，格式参考 `follow-builders`：标题、分组、条目摘要、来源链接和必要的判断，用户不用跳转文件。
- 如果用户要求 Markdown，可以在对话中输出 Markdown，或按用户指定路径保存 `.md`。
- 如果用户要求 PDF，建议文件名：
  - `reports/YYYY-MM-DD/morning_brief_YYYY-MM-DD.pdf`
  - `reports/YYYY-MM-DD/general_report_YYYY-MM-DD.pdf`
  - `reports/YYYY-MM-DD/finance_report_YYYY-MM-DD.pdf`
  - `reports/YYYY-MM-DD/tech_report_YYYY-MM-DD.pdf`
  - `reports/YYYY-MM-DD/ai_daily_report_YYYY-MM-DD.pdf`
  - `reports/YYYY-MM-DD/us_stocks_report_YYYY-MM-DD.pdf`
- `*.html`、`*.json`、`*.png`、`*_snapshot.*` 默认都视为过程文件；除非用户明确要求，不要交付。
- 如果用户要求文件导出，最终回复给文件路径和必要说明；不要列出无关过程文件。

## 新闻日报工作流

### 数据抓取

```bash
python3 scripts/daily_briefing.py --profile general --no-save
python3 scripts/daily_briefing.py --profile finance --no-save
python3 scripts/daily_briefing.py --profile tech --no-save
python3 scripts/daily_briefing.py --profile ai_daily --no-save
```

### 输出要求
- 语言：简体中文
- 必带字段：标题、时间、摘要、Deep Dive
- 不编造新闻，不补不存在的数据
- 对综合 / 财经 / 科技 / AI 深度板块，先经过 `最近 24 小时` 过滤，再做近 3 天成稿去重；过不了这两道门槛的条目不能进入最终稿。
- 默认直接按对应 instructions 在对话里生成日报正文。
- 只有用户要求 PDF 或保存文件时，才生成临时 Markdown/HTML 并走导出流程。

## 标准日报工作流

1. 先确认本轮是否已有以下源稿内容：
   - `reports/YYYY-MM-DD/general_report.md`
   - `reports/YYYY-MM-DD/finance_report.md`
   - `reports/YYYY-MM-DD/tech_report.md`
   - `reports/YYYY-MM-DD/ai_daily_report.md`
2. 如果不存在，就先按对应 profile 生成源稿内容。
2.1 对 raw items 先执行近 24 小时过滤；可复用 `scripts/filter_recent_brief_items.py` 对候选条目做时效与近 3 天去重检查。
3. 生成标准日报时按以下顺序组装：
   - 综合早报
   - 财经早报
   - 科技早报
   - AI 深度日报
   - 美股股票早报
4. 对前四个板块，直接贴源文件原文，不改写。
5. 美股板块单独生成；如果用户提供了更完整的版本，用用户版本覆盖。
6. 默认直接在对话中输出标准日报。
6.1 如果用户要求 PDF，走“Markdown -> HTML 阅读页 -> 可用浏览器打印 PDF”：可以复用 `scripts/export_pdf_with_system_chrome.sh`，也可以使用运行环境提供的等价浏览器打印能力；禁止回退到会截断长文的 `file:// + print-to-pdf`。
7. 如果用户指定路径或格式，则按用户要求保存；不要额外保存无关格式，除非用户明确要求。

## 美股股票早报工作流

1. 读取用户给的股票列表；如果没给，就用默认观察名单。
2. 用一次 `web.finance` 调用获取所有股票的最新价格和昨收，锁定为同一轮行情快照。
2.1 立刻把原始快照写入临时文件，并运行 `scripts/validate_us_stocks_snapshot.py`：
   - 校验观察名单是否齐全；
   - 校验关键数字字段是否完整；
   - 校验时间戳是否保持同轮口径；
   - 若接入了第二来源，做漂移检测但不要用它覆盖主源。
2.2 若校验失败，直接输出数据缺口或“待核实”，不要继续写股票判断。
3. 用搜索获取近 1-7 天的重要新闻：
   - 优先 Reuters
   - 其次公司 IR / 新闻稿
   - 再其次权威媒体
4. 先确定并写明价格时间口径：
   - 默认：`生成时最新价快照`
   - 仅在用户明确要求时：`上一交易日收盘后版本`
   - 北京时间周六：默认允许使用周五收盘口径
   - 北京时间周日：默认改为“信息版”，不做价格对比
   - 北京时间周一：默认改为“最近一个美股交易日盘后波动 + 信息版”
5. 对同一份报告里的所有股票，判断必须围绕同一轮价格口径来写；如果当天缺少个股催化，要明确写“主要受板块 / 市场情绪驱动”。
6. 对每只股票输出：
   - 最新价
   - 较昨收变动（绝对值和百分比）
   - 关键因素
   - 重要新闻链接
   - 一句话判断
7. 默认直接在对话中输出美股股票早报。
8. 如果用户要求 PDF，生成临时 Markdown 后导出 `reports/YYYY-MM-DD/us_stocks_report_YYYY-MM-DD.pdf`，并按 PDF 规则验收。

### 美股股票早报模板

```markdown
# 美股股票早报 | YYYY-MM-DD

> 注：以下价格为北京时间 YYYY-MM-DD HH:MM 对应的盘中最新价快照；如用户明确要求收盘版，再改写为对应美东交易日收盘后版本。

| Ticker | 最新价 | 较昨收变动 | 一句话判断 |
|---|---:|---:|---|
| NVDA | $184.77 | +2.13 / +1.16% | GTC 预期继续支撑 |

## NVDA
- **最新股价**：$184.77
- **较昨天**：+1.16%
- **关键因素**：GTC 预期、产品发布、订单、CapEx、生态合作。
- **重要新闻**：
  - [新闻标题](https://example.com)
- **我的判断**：一句话说明今天为何涨跌。
```

## 交互菜单

用户说“牛马牛马”时，先执行 onboarding 状态检查；如果首次未完成，先完成 onboarding，再读取 `templates.md` 并展示菜单。

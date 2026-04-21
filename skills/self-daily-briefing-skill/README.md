# 中文 Morning Brief Skill

一句话安装：

```text
帮我安装这个 skill：https://github.com/vinsonhi/AI-Skills/tree/main/skills/self-daily-briefing-skill
```

如果你的 AI Agent 支持从 GitHub 路径安装 skill，直接使用上面这句即可。

如果不支持自动安装，可以下载本目录，并放到你的 Agent 指定的 skills 目录；安装后刷新或重启 Agent，让它重新索引 skills。

## 你会得到什么

这是一个通用的中文 Morning Brief skill。你可以让支持 skills 的 AI Agent 帮你生成：

- 综合早报：科技、创投、社交、财经大盘动态
- 财经早报：宏观、市场、板块、加密和关键驱动
- 科技早报：AI、开发者工具、创业产品
- AI 深度日报：论文、AI builders、播客、官方博客、newsletter
- 美股股票早报：自选股票价格、涨跌、重要新闻和一句话判断
- 标准日报：默认完整日报，包含综合、财经、科技、AI 深度和美股自选；如果只想看细节，也可以单独点某个模块

默认最终只交付 PDF。生成过程里可能临时使用 Markdown、HTML 或 JSON，但这些都只是工作文件，不应该作为最终产物展示给用户。

## 第一次使用

第一次安装后，Agent 第一次使用这个 skill 时，必须先帮你设置一次日报偏好。以后正常生成日报不会重复问，除非你明确说“重新设置日报偏好”。

如果第一次使用时你直接说“生成日报”或“牛马牛马”，也应该先完成 onboarding，再继续日报任务。

onboarding 会问四件事：

1. 先简单介绍它会帮你生成什么日报。
2. 问你想用中文、英文还是双语；默认中文。
3. 问你有没有长期关注的美股 ticker，以及有没有特别想关注的公司、产品、人物或主题；如果你不填，先默认跟踪 Mag 7。
4. 展示默认信息源，并问你要不要现在先跑一版看看效果。

你的股票名单和偏好只会记在这台电脑本地；公开仓库只内置 Mag 7 作为通用默认名单，不内置任何个人股票名单。

## 怎么使用

常用说法：

```text
牛马牛马
```

会展示日报菜单。

如果你没有指定日报类型，默认生成“标准日报”。

也可以直接说：

```text
帮我生成今天的综合早报
帮我生成今天的 AI 深度日报
帮我生成美股股票早报
帮我生成今天的标准日报
重新设置日报偏好
```

如果你要美股早报，可以直接给股票列表：

```text
帮我生成 NVDA、AMD、MSFT、GOOGL 的美股股票早报
```

## 默认信息源

### 综合 / 财经 / 科技

- Hacker News
- GitHub Trending
- Product Hunt
- 36Kr
- Weibo
- WallStreetCN
- Tencent News
- V2EX

这些源主要用于“今天发生了什么”的快速扫描。默认只收最近 24 小时内的新事件或明确新进展。

### AI builders on X

AI 深度日报会跟踪一组固定 builders，不再依赖个人关注流或 X 推荐流。账号列表在 `instructions/x_ai_accounts.txt`。

默认包含 25 个账号：

- Andrej Karpathy
- Swyx
- Josh Woodward
- Kevin Weil
- Peter Yang
- Nan Yu
- Madhu Guru
- Amanda Askell
- Cat Wu
- Thariq
- Google Labs
- Amjad Masad
- Guillermo Rauch
- Alex Albert
- Aaron Levie
- Ryo Lu
- Garry Tan
- Matt Turck
- Zara Zhang
- Nikunj Kothari
- Peter Steinberger
- Dan Shipper
- Aditya Agarwal
- Sam Altman
- Claude

规则很简单：只看固定账号的主页，不用 `Following`，不用 `For you`，也不用匿名搜索替代。帖子要有实质内容，优先保留原创观点、产品发布、技术讨论、行业判断和 builder 经验。

### AI 播客

播客不是日更源，所以默认看最近 14 天，不强行塞进 24 小时窗口。

默认 6 档：

- Latent Space
- Training Data
- No Priors
- Unsupervised Learning
- The MAD Podcast with Matt Turck
- AI & I by Every

播客摘要会优先提炼 `The Takeaway`，而不是流水账复述访谈内容。

### AI 官方博客

默认官方博客：

- Anthropic Engineering
- Claude Blog

这部分主要看产品能力变化、工程实践、API 更新、研究发现和 benchmark。没有原文链接的内容不会写进日报。

## 最终产物

默认最终只交付一个 PDF：

```text
reports/YYYY-MM-DD/morning_brief_YYYY-MM-DD.pdf
```

规则：

- 用户没有特别要求时，生成“标准日报”，最终只交付这一个 PDF。
- 用户指定某个单独模块，例如“AI 深度日报”或“美股股票早报”，也只交付对应 PDF。
- Markdown、HTML、JSON、原始抓取结果、校验快照都属于过程文件；可以临时创建，但成功导出并验收 PDF 后要删除或放入临时目录，不要展示给用户。
- 只有用户明确要求“给我 Markdown / 保留原始数据 / 保留过程文件”时，才额外交付这些文件。

标准日报会按这个顺序：

1. 综合早报
2. 财经早报
3. 科技早报
4. AI 深度日报
5. 美股股票早报

如果某个板块当天已经生成过，生成标准日报时可以临时复用原文件内容，不为了统一文风重新改写；最终仍只交付标准日报 PDF。

## 质量规则

- 不编造新闻，不补不存在的数据。
- 缺数据就写缺口，不拿旧闻冒充今天的新进展。
- 综合、财经、科技默认只看最近 24 小时。
- 播客默认看最近 14 天。
- 最近 3 天写过的同类头条，如果今天没有实质新进展，不重复放进前列。
- 每条内容都要有来源、时间、摘要和 Deep Dive。
- X 内容必须来自固定账号列表；登录态失效时停下来让用户恢复，不用匿名路线冒充。
- 美股价格必须来自同一轮行情快照，不能混用不同时间点或不同来源。

## 美股观察名单

公开版本默认跟踪 Mag 7：

```text
AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA
```

第一次 onboarding 时，如果你给了 ticker，Agent 会记在本地已安装的 skill 目录：

```text
instructions/us_stocks_watchlist_default.txt
```

如果你没有给 ticker，就先沿用 Mag 7；如果你给了自己的 ticker，之后生成美股早报时会默认使用你的名单。你也可以随时说：

```text
把我的美股观察名单改成 NVDA、AMD、MSFT、META
```

## PDF 导出

PDF 会尽量保留 Markdown 的阅读结构。默认链路是：

```text
Markdown -> HTML 阅读页 -> 可用浏览器打印 PDF
```

如果浏览器打印链路不可用，应该明确说明 PDF 被阻塞，而不是悄悄切到低保真导出。

## 示例

参考：

- `examples/merged_daily_report_2026-03-11.md`
- `examples/merged_daily_report_2026-03-11.pdf`

## 辅助脚本

onboarding：

```bash
python3 scripts/onboarding.py
python3 scripts/onboarding.py --force
python3 scripts/onboarding.py --accept-defaults
python3 scripts/onboarding.py --language zh --watchlist "NVDA, AMD, MSFT" --interests "Claude Code, AI 搜索, 机器人"
```

非交互环境里，不要只打印 onboarding 就标记完成；需要用户回复偏好，或显式使用 `--accept-defaults`。

抓固定 X builders：

```bash
python3 scripts/check_x_personal_chrome_session.py
python3 scripts/extract_x_accounts_with_personal_chrome.py
```

这两个脚本是 macOS + Google Chrome 的参考实现。其他 Agent 或运行环境可以使用等价的已登录浏览器会话、cookie bridge、浏览器 MCP 或人工登录流程，只要仍然按固定账号列表抓取即可。

抓基础新闻源：

```bash
python3 scripts/daily_briefing.py --profile general --no-save
python3 scripts/daily_briefing.py --profile finance --no-save
python3 scripts/daily_briefing.py --profile tech --no-save
python3 scripts/daily_briefing.py --profile ai_daily --no-save
```

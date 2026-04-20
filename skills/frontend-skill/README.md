# Frontend Skill

一句话安装：

```text
帮我安装这个 skill：https://github.com/vinsonhi/AI-Skills/tree/main/skills/frontend-skill
```

如果你的 Codex 支持从 GitHub 路径安装，直接说上面这句就够了。

手动复制：

```bash
mkdir -p ~/.codex/skills
cp -R skills/frontend-skill ~/.codex/skills/
```

## 你会得到什么

这是一个让 Codex 做前端时更有审美判断的 skill。它会把页面先当成“视觉作品”和“产品体验”来设计，而不是一上来堆组件。

适合用来做：

- 落地页、品牌站、活动页
- 视觉要求高的产品首页或专题页
- App 界面、dashboard、prototype
- demo、game UI、交互页面
- 想避免“AI 味很重”的通用前端输出

它会强制 Codex 先想清楚三件事：

- visual thesis：页面的气质、材料感和能量
- content plan：首屏、支撑内容、细节、行动入口
- interaction thesis：哪些动效真的能提升体验

## 怎么使用

直接描述你想做的页面：

```text
帮我做一个视觉强一点的 AI 产品官网
```

或者更具体一点：

```text
帮我做一个给 Claude Code 插件用的 landing page，要有强主视觉、少文字、首屏能一眼看懂
```

如果是产品界面，也可以说：

```text
帮我做一个偏 Linear 风格的项目管理 dashboard，不要营销首页，要直接进入可用界面
```

## 它会怎么做

这个 skill 默认会让 Codex：

- 先处理构图、层级、主视觉和节奏，再写组件
- 用一个强视觉锚点支撑首屏
- 控制文案长度，让页面能快速扫读
- 默认少用卡片，优先用完整 section、图片、列表、分割和留白
- 为视觉型页面加入 2-3 个有目的的动效
- 对 app / dashboard 优先使用工具型文案，不写空泛广告语

## 默认审美取向

- 一个页面先有一个大想法
- 首屏像海报，不像文档
- 品牌或产品名要足够明确
- 图片要承担叙事，不做装饰性背景
- 动效要服务层级和氛围，不做噪音
- 卡片只在它真的是交互边界时使用
- 不用通用 SaaS 卡片矩阵糊首屏

## 适合的提示词

```text
帮我做一个视觉更高级的版本，不要常见 SaaS 卡片堆砌
```

```text
这个页面要像一个完整产品，不要像嵌在网页里的 demo preview
```

```text
先给我 visual thesis / content plan / interaction thesis，再实现
```

```text
做成可直接打开的 HTML 页面，并用 Playwright 截图检查桌面和移动端
```

## 文件

- `SKILL.md`：核心设计规则
- `agents/openai.yaml`：agent 配置
- `LICENSE.txt`：许可证

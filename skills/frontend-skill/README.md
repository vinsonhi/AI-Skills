# frontend-skill

用于做视觉要求高的前端页面和界面的 skill。

这个 skill 的重点不是告诉模型“写一个页面”，而是先建立明确的审美和结构约束：

- 先写 visual thesis、content plan、interaction thesis
- 默认从构图、主视觉、层级和节奏开始，而不是先堆组件
- 优先全屏视觉锚点、强品牌层级、短文案、少量但明确的动效
- 明确限制常见失败模式，比如首屏卡片堆砌、弱品牌、无叙事轮播、装饰性动效

## Files

- [`SKILL.md`](./SKILL.md)
- [`LICENSE.txt`](./LICENSE.txt)
- [`agents/openai.yaml`](./agents/openai.yaml)

## 安装

最简单的说法：

```text
帮我安装这个 skill：https://github.com/vinsonhi/AI-Skills/tree/main/skills/frontend-skill
```

如果对方支持 GitHub 仓库路径安装，通常这句话就够了。

或者手动复制：

```bash
mkdir -p ~/.codex/skills
cp -R skills/frontend-skill ~/.codex/skills/
```

## 适用场景

- 落地页、品牌站、活动页
- 视觉要求高的产品首页或专题页
- 需要更强 art direction 的 demo、prototype、game UI
- 想避免“AI 味很重”的通用前端输出

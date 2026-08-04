# 品牌画面规范

以下数值以 1920×1080 为基准。其他画幅按宽高等比例缩放，保持安全边距和光学对齐。

## 正片右下角水印

内容：白色抖音音符 Icon + `抖音直播行业产品团队`。

基准参数：

- 位置：`right: 36px; bottom: 33px`
- 整体不透明度：`0.92`
- 布局：横向 flex，垂直居中
- Icon：`29px × 35px`，使用 `assets/douyin-icon-white.png`
- Icon 与文字间距：`11px`
- 字体：`PingFang SC, Microsoft YaHei, sans-serif`
- 字号：`23px`
- 字重：`650`
- 行高：`1`
- 字间距：`0.4px`
- 文字颜色：`#FFFFFF`
- 阴影：`drop-shadow(0 2px 2.8px rgba(16, 36, 63, 0.58))`
- 层级：高于画面内容，避免覆盖主字幕

参考 CSS：

```css
.team-watermark {
  position: absolute;
  right: 36px;
  bottom: 33px;
  z-index: 76;
  display: flex;
  align-items: center;
  gap: 11px;
  color: #fff;
  opacity: .92;
  filter: drop-shadow(0 2px 2.8px rgba(16, 36, 63, .58));
  pointer-events: none;
  white-space: nowrap;
}
.team-watermark img {
  display: block;
  width: 29px;
  height: 35px;
  object-fit: contain;
}
.team-watermark span {
  font: 650 23px/1 "PingFang SC", "Microsoft YaHei", sans-serif;
  letter-spacing: .4px;
}
```

禁止：

- 不加胶囊、底板、描边框或渐变块；
- 不放在字幕中间；
- 不裁入 Icon 右侧的其他文字；
- 不让 Icon 与文字上下错位；
- 不把透明度降到浅色背景上难以识别；
- 不在结束页继续叠加水印。

## 两秒结束页

时长固定 2 秒。使用蓝白 Fluent 风格，背景平静、企业级，不加粒子或抽象 dashboard。

1920×1080 基准参数：

- 背景：`linear-gradient(135deg, #EDF5FF 0%, #FBFDFF 52%, #E6F0FF 100%)`
- 右上与左下可加入低透明蓝色径向柔光
- 主卡片：居中，`850px × 360px`
- 卡片圆角：`34px`
- 卡片背景：`rgba(255,255,255,.72)`
- 卡片描边：`1px solid rgba(255,255,255,.96)`
- 卡片阴影：`0 20px 60px rgba(49,93,157,.16)`
- 卡片可使用 `backdrop-filter: blur(20px)`
- Logo：`assets/live-service-platform-institution.png`，宽 `620px`，保持原比例
- 分隔线：宽 `400px`、高 `2px`、`rgba(51,120,246,.18)`
- 署名：`抖音直播-行业产品团队出品`
- 署名字体：28px、字重 520、颜色 `#47627F`、字间距 1px

动效：

- 结束页整体用 0.3–0.4 秒淡入；
- 卡片轻微上移和缩放进入；
- Logo、分隔线、署名依次出现；
- 至少留下约 1 秒完整静止画面；
- 可加入 0.5–0.8 秒轻微、干净的品牌收束音。

不得重绘 Logo，不得改字，不得拉伸，不得用错误的抖音 Icon 替代。

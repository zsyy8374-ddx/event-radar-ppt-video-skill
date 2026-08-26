# 深蓝科技风配色规则

## 背景色
- BG_DARK  = RGB(0x0D, 0x1B, 0x2A) — 主背景
- BG_MID   = RGB(0x18, 0x2A, 0x3E) — 卡片/区块底

## 强调色（明亮可用）
- ACCENT_GOLD  = RGB(0xFF, 0xD5, 0x4F) — 标题/强调
- ACCENT_BLUE  = RGB(0x42, 0xA5, 0xF5) — 次要强调/横线
- ACCENT_CYAN  = RGB(0x80, 0xDE, 0xEA) — 科技点缀/标签
- ACCENT_ORANGE= RGB(0xFF, 0xAA, 0x44) — 次级警示/中等级
- ACCENT_RED   = RGB(0xFF, 0x66, 0x66) — 危险/跌/回避
- GREEN_OK     = RGB(0x66, 0xCC, 0x77) — 利好/涨/优质

## 文字色（全部亮色，深蓝背景可见）
- LIGHT_GRAY = RGB(0xD0, 0xDD, 0xEE) — 正文
- MID_GRAY   = RGB(0x99, 0xAA, 0xBB) — 次要信息/标签
- DIM_LABEL  = RGB(0x88, 0x99, 0xAA) — 底部条品牌文字
- WHITE      = RGB(0xFF, 0xFF, 0xFF) — 大标题

## ❌ 禁用
- 任何 brightness < 100 的颜色作为文字色
- 默认 python-pptx 字体颜色（渲染成深蓝背景上不可见的RGB(21,37,56)级别）
- 表格中的段落颜色（python-pptx 经常渲染异常）

## 表格替代方案
用 `paras()` 多段文字+空格对齐替代表格。每段手动指定亮色。

## 位置链约束
badge(0.06in)→横线(0.38in)→标题(0.50in)→副标题(1.0in)→正文(≥1.5in)→底部条(7.0in)
所有文本框 bottom ≤ 6.9in

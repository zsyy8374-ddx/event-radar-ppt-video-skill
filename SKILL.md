---
name: event-radar-ppt-video
description: "重磅事件雷达 ⚡ PPT视频流水线。从docx/文本生成深蓝科技风PPT→配音→视频→发邮件。用户说「PPT视频：xxx.docx」或「跑事件雷达PPT视频」时触发。深蓝科技风(0D1B2A)，字号≥15pt，yuv420p编码。"
---

# 重磅事件雷达 ⚡ PPT视频流水线

从 docx/文本 → PPT（深蓝科技风/暗紫科技风）→ PNG导出 → Edge TTS配音 → ffmpeg视频合成 → 背景音乐 → 发邮件。一站式。

## 触发方式

用户说：
- 「PPT视频：xxx.docx」
- 「跑事件雷达PPT视频」
- 「重磅事件雷达PPT视频」

## 流水线结构

```
用户内容 (docx/文本)
    ↓
Step 1: create_ppt.py     → 深蓝科技风PPT (12页模板，字号≥15pt)
    ↓
Step 2: 导出PNG            → PowerPoint COM (PowerShell脚本，1920×1080)
    ↓
Step 3: gen_tts.py         → Edge TTS 配音 (12段wav，云健男声)
    ↓
Step 4: make_video.py      → ffmpeg合成 (Ken Burns缩放 + 720p + yuv420p)
    ↓
Step 5: 背景音乐            → ffmpeg混合 (环境音轨，音量0.5)
    ↓
Step 6: send_email.py      → smtp.qq.com 发邮件 (PPT+视频两件套)
```

## 配色系统

### 样式A：深蓝科技风（默认/事件雷达）

| 用途 | 颜色 | RGB |
|------|------|-----|
| 背景 | 深蓝 | `0x0D, 0x1B, 0x2A` |
| 卡片底 | 中蓝 | `0x18, 0x2A, 0x3E` |
| 顶底栏 | 亮蓝 | `0x42, 0xA5, 0xF5` |
| 强调色 | 亮金 | `0xFF, 0xD5, 0x4F` |
| 点缀色 | 亮青 | `0x80, 0xDE, 0xEA` |
| 正文 | 亮灰 | `0xD0, 0xDD, 0xEE` |

### 样式B：暗紫科技风（紫苏雷达专属）

| 用途 | 颜色 | RGB |
|------|------|-----|
| 背景 | 暗紫 | `0x1A, 0x1A, 0x2E` |
| 卡片底 | 中紫 | `0x25, 0x25, 0x3F` |
| 顶底栏 | 紫苏紫 | `0x9B, 0x59, 0xB6` |
| 强调色 | 暖金 | `0xE8, 0xC5, 0x4A` |
| 点缀色 | 亮蓝 | `0x5B, 0x9B, 0xD5` |
| 正文 | 亮灰白 | `0xE8, 0xE8, 0xF0` |

### 通用（两种样式共用）

| 用途 | 颜色 | RGB |
|------|------|-----|
| 警告 | 亮红 | `0xFF, 0x66, 0x66` |
| 利好 | 亮绿 | `0x66, 0xCC, 0x77` |
| 强调色 | 亮青 | `0x80, 0xDE, 0xEA` |
| 标签 | 中灰 | `0x99, 0xAA, 0xBB` |
| 文字 | 白色 | `0xFF, 0xFF, 0xFF` |

### 选择规则
- 主题包含「紫苏雷达」「紫苏叶」「紫苏」→ 用样式B（暗紫科技风）
- 其他主题（事件雷达、重磅雷达、订单雷达）→ 用样式A（深蓝科技风）

## 🚨 硬规则（违反则重做）

1. **字号≥15pt** — 任何页任何位置不得小于15pt
2. **yuv420p** — 所有ffmpeg编码步骤加 `-pix_fmt yuv420p`（否则播放器黑屏）
3. **深蓝背景上文字必须明亮** — 禁用默认python-pptx暗色文字
4. **内容不超底部** — 所有元素 bottom ≤ 6.9in（底部装饰条在7.0in）
5. **PPT视频禁用词** — 不出现「Serenity」「股神」→ 改「紫苏叶理论」「紫苏雷达」「Dengxian AI Research」
6. **表格替代** — python-pptx表格文字颜色渲染异常，用 `paras()` 多段文字+空格对齐替换
7. **英文简称逐字母读（不拼读）** — 英文专用简称（GCP/ICH/SOP/SAE/SUSAR/DSUR/CRF/NMPA/IVD/IIT/PI 等）配音必须逐字母朗读（G-C-P），禁止拼读成单词；版本号（E6/R3）、表单编号（AF/ZZ-01、SOP04.01）同样处理（字母逐字母+数字保留）。实现：配音文本统一经 `expand_abbr()` 处理，模板见 `scripts/gen_tts.py`（内置）

## 预检清单（视频发前逐项勾）

- [ ] 字号检查：`grep "sz=" create_ppt.py | grep -oP '(?<=sz=)\d+'` 全部 ≥ 15
- [ ] yuv420p：`grep "pix_fmt" make_video.py` 至少2行
- [ ] 英文简称逐字母：`grep "expand_abbr" gen_tts.py`（配音文本会自动展开 GCP→G C P）
- [ ] 底部条检查：所有文本框 bottom ≤ 6.9
- [ ] 视频大小：`ls -lh /tmp/xxx.mp4` ≤ 25MB
- [ ] 配音已生成：12个wav文件存在
- [ ] 是否配乐：包含背景音乐混合步骤
- [ ] 邮件附件齐全：PPT + 视频两件套

## PPT结构模板（12页）

| Slide | 内容 | 说明 |
|-------|------|------|
| 1 | 封面 | 标题+副标题+冲击等级+日期 |
| 2 | 扫描状态+成色评估 | 引擎状态+板块数据 |
| 3 | 主线一 | 最大集群催化链 |
| 4 | 主线二 | ⭐ 最强主题 |
| 5 | 主线三 | 事件催化 |
| 6 | 主线四+五 | 双主线同页 |
| 7 | 催化链条图示 | 独狼/早期信号深度 |
| 8 | 全球视角验证 | 国外引擎证据 |
| 9 | TOP5核心标的 | 四视角评分 |
| 10 | 配置建议 | 梯队+多空 |
| 11 | 风险提示 | 6项主要风险 |
| 12 | Ending | 品牌页 |

*内容多时可增页至14-16页，保持每页≤12行*

## 脚本说明

- `scripts/create_ppt.py` — 标准模板，每次复制到`~/strategy/`改写内容
- `scripts/gen_tts.py` — 配音模板，每次复制改写narrations数组
- `scripts/make_video.py` — 视频合成模板，改SLIDES变量即可
- `scripts/export_ppt.ps1` — 复制到Windows `/tmp/` 后通过PowerShell导出
- `scripts/send_email.py` — 发邮件

## 固定配置

- 邮箱：1628354330@qq.com → 自收自发
- SMTP：smtp.qq.com:465，密码通过环境变量 `QQMAIL_PASS` 传入
- TTS语音：zh-CN-YunjianNeural（云健，男声，播报解说风）
- **英文简称：逐字母读**（gen_tts.py 内置 `expand_abbr()` 自动把 GCP→"G C P"、E6→"E 6" 等，禁止拼读）
- 视频尺寸：1280×720 (导出用1920×1080，压缩到720p)
- 背景音乐：ffmpeg生成环境粉噪+55Hz/110Hz正弦波混合
- ffmpeg：`~/.local/lib/python3.12/site-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2`

## 参考

- 配色规则详细：`references/color_rules.md`
- 完整示例：本次运行脚本在 `~/strategy/create_ppt_radar_zt.py` 等

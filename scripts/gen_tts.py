#!/usr/bin/env python3
"""gen_tts · Edge TTS配音 — 改narrations数组即可
英文专用简称自动逐字母读（GCP→G C P，E6→E 6），禁止拼读"""
import asyncio, os, re

# ═══ 每次改这里 ═══
narrations = [
    # Slide 1: 封面
    "重磅事件雷达。主题名称。报告日期。Dengxian AI Research。",
    # Slide 2-N: 按需写...
]
TOTAL = len(narrations)
# ═════════════════

DIR = "/tmp/ppt_audio"
os.makedirs(DIR, exist_ok=True)
VOICE = "zh-CN-YunjianNeural"  # 云健男声/播报解说风

# ---------- 英文专用简称 → 逐字母展开（不拼读） ----------
# 已知英文单词（保持原样按单词读）
_SKIP_WORDS = {"AGENDA"}

def expand_abbr(text):
    """GCP→'G C P'，SOP04.01→'S O P 04 01'，AF/ZZ-01→'A F Z Z 01'，E6→'E 6'，R3→'R 3'"""
    text = text.replace("**", "").replace("*", "").replace("–", " ").replace("—", " ")
    pat = re.compile(
        r"[A-Z]{2,}(?:[0-9]+(?:\.[0-9]+)?)?(?:\s*[/\-–—]\s*[A-Z0-9]+(?:\.[0-9]+)?)*"
        r"|[A-Z][0-9]+(?:\.[0-9]+)?"
    )
    def repl(m):
        tok = m.group(0).strip()
        if tok in _SKIP_WORDS:
            return tok
        items = re.findall(r"[A-Z]+|[0-9]+", tok)
        out = []
        for it in items:
            if it.isalpha():
                out.append(" ".join(it))   # 逐字母
            else:
                out.append(it)             # 数字保留
        return " ".join(out)
    return pat.sub(repl, text)

async def gen(i, t):
    import edge_tts
    o = os.path.join(DIR, f"slide_{i+1:02d}.wav")
    t = expand_abbr(t)  # 英文简称逐字母读
    await edge_tts.Communicate(t, VOICE).save(o)
    print(f"Slide {i+1}: {os.path.getsize(o)//1024}KB", flush=True)

async def main():
    print(f"Generating {TOTAL} slides...", flush=True)
    for i, t in enumerate(narrations):
        await gen(i, t)
    print("DONE!", flush=True)

asyncio.run(main())

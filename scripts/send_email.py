#!/usr/bin/env python3
"""send_email · 发邮件 — 改文件路径和主题即可"""
import smtplib, ssl, os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.header import Header

# ═══ 每次改这里 ═══
PPT_PATH   = "/tmp/ppt_gene_edit_death.pptx"
VIDEO_PATH = "/tmp/gene_edit_video_bgm.mp4"
SUBJECT    = "🔬 科普视频：首例脑部基因编辑致死事件"
PPT_NAME   = "科学伦理_首例脑部基因编辑致死事件.pptx"
VIDEO_NAME = "科学伦理_首例脑部基因编辑致死事件.mp4"
# ══════════════════

FROM  = "1628354330@qq.com"
TO    = "1628354330@qq.com"

msg = MIMEMultipart()
msg["From"] = FROM; msg["To"] = TO
msg["Subject"] = Header(SUBJECT, "utf-8")

body = MIMEText(f"""<html><body style="font-family:Microsoft YaHei;color:#333">
<h2>⚡ 重磅事件雷达 · {SUBJECT}</h2>
<hr><p><b>附件：</b></p>
<p>1️⃣ PPT源文件</p>
<p>2️⃣ 视频</p>
<hr><p style="color:#888;font-size:12px">Dengxian AI Research</p>
</body></html>""", "html", "utf-8")
msg.attach(body)

def attach_file(path, display_name):
    with open(path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=("utf-8", "", display_name))
        msg.attach(part)
        print(f"  📎 {display_name}")

attach_file(PPT_PATH, PPT_NAME)
attach_file(VIDEO_PATH, VIDEO_NAME)

PASS = os.environ.get("QQMAIL_PASS", "")
if not PASS:
    # 兜底尝试
    import subprocess as sp
    r = sp.run(["grep","-r","QQMAIL_PASS","/home/ddx/.bashrc","/home/ddx/.profile","/home/ddx/.env"],
               capture_output=True,text=True,timeout=5)
    for line in r.stdout.split("\n"):
        if "QQMAIL_PASS" in line and "=" in line:
            PASS = line.split("=",1)[1].strip().strip("'\"")
            break

if not PASS:
    print("❌ QQMAIL_PASS not found. Export it or set in .bashrc")
    exit(1)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.qq.com", 465, context=ctx) as s:
    s.login(FROM, PASS)
    s.sendmail(FROM, TO, msg.as_string())
    print(f"✅ Email sent to {TO}")

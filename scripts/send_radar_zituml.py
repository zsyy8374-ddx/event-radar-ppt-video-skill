#!/usr/bin/env python3
"""send_email · 题材纯度雷达·人形机器人·宇树科技IPO"""
import smtplib, ssl, os, subprocess as sp
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.header import Header

PPT_PATH   = "/tmp/radar_zituml.pptx"
VIDEO_PATH = "/tmp/radar_zituml_video_bgm.mp4"
SUBJECT    = "题材纯度雷达 · 人形机器人·宇树科技IPO概念"
PPT_NAME   = "题材纯度雷达_人形机器人_宇树科技IPO.pptx"
VIDEO_NAME = "题材纯度雷达_人形机器人_宇树科技IPO.mp4"

FROM  = "1628354330@qq.com"
TO    = "1628354330@qq.com"

msg = MIMEMultipart()
msg["From"] = FROM; msg["To"] = TO
msg["Subject"] = Header(SUBJECT, "utf-8")

body = MIMEText(f"""<html><body style="font-family:Microsoft YaHei;color:#333">
<h2>⚡ 题材纯度雷达 · {SUBJECT}</h2>
<hr><p><b>附件：</b></p>
<p>1️⃣ PPT源文件（13页）</p>
<p>2️⃣ 视频（配乐：Kiss The Rain）</p>
<hr><p style="font-size:12px;color:#888">
生成日期：2026年7月30日<br>
引擎：25引擎全维度扫描<br>
署名：Dengxian AI Research
</p>
<hr><p style="color:#999;font-size:11px">
免责声明：本报告基于公开信息整理，仅供参考，不构成投资建议。市场有风险，投资需谨慎。
</p>
</body></html>""", "html", "utf-8")
msg.attach(body)

def attach_file(path, display_name):
    with open(path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename=("utf-8", "", display_name))
        msg.attach(part)
        print(f"  📎 {display_name} ({os.path.getsize(path)//1024}KB)")

attach_file(PPT_PATH, PPT_NAME)
attach_file(VIDEO_PATH, VIDEO_NAME)

PASS = os.environ.get("QQMAIL_PASS", "")
if not PASS:
    r = sp.run(["grep","-r","QQMAIL_PASS","/home/ddx/.bashrc","/home/ddx/.profile","/home/ddx/.env"],
               capture_output=True,text=True,timeout=5)
    for line in r.stdout.split("\n"):
        if "QQMAIL_PASS" in line and "=" in line:
            PASS = line.split("=",1)[1].strip().strip("'\"")
            break

if not PASS:
    print("❌ QQMAIL_PASS not found.")
    exit(1)

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.qq.com", 465, context=ctx) as s:
    s.login(FROM, PASS)
    s.sendmail(FROM, TO, msg.as_string())
    print(f"✅ Email sent to {TO}")

print("\n🔎 视频文件信息:")
os.system(f"ls -lh {VIDEO_PATH}")

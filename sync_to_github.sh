#!/bin/bash
# ⚡ 一键同步 event-radar-ppt-video skill 到 GitHub
# 用法：bash ~/.openclaw/skills/event-radar-ppt-video/sync_to_github.sh
# 依赖：~/.git-credentials 里的 GitHub token（已配置）

cd ~/.openclaw/skills/event-radar-ppt-video || exit 1

# 1. 查看改动
echo "=== 改动文件 ==="
git status --short

# 2. 提交
git add -A
if git diff --cached --quiet; then
    echo "✅ 无改动，已是最新"
    exit 0
fi
git commit -m "sync: $(date '+%Y-%m-%d %H:%M')"

# 3. 推送（失败自动重试一次）
echo "=== 推送到 GitHub ==="
if timeout 120 git push origin main 2>&1; then
    echo "✅ 同步完成: https://github.com/zsyy8374-ddx/event-radar-ppt-video-skill"
else
    echo "⚠️ git push 失败，改用 API 上传..."
    python3 /tmp/gh_push.py 2>/dev/null || echo "❌ 同步失败，请手动检查"
fi

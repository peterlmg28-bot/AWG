#!/bin/bash

# ----------------------------
# 設定路徑與 repo
# ----------------------------
PROJECT_PATH="/Users/peterlin/Documents/augment-projects/AWG"
MARKDOWN_FILE="$PROJECT_PATH/resume.md"
HTML_FILE="$PROJECT_PATH/index.html"
GITHUB_REPO="git@github.com:peterlmg28-bot/AWG.git"

cd "$PROJECT_PATH" || exit

# ----------------------------
# 確保 git 遠端是 SSH
# ----------------------------
if git remote | grep origin >/dev/null; then
    git remote set-url origin "$GITHUB_REPO"
else
    git init
    git remote add origin "$GITHUB_REPO"
    git branch -M main
fi

# ----------------------------
# 生成 HTML
# ----------------------------
if [ ! -f "$MARKDOWN_FILE" ]; then
    echo "Error: 找不到 Markdown 檔案 $MARKDOWN_FILE"
    exit 1
fi

echo "Step 1: 將 Markdown 轉成 HTML"
pandoc "$MARKDOWN_FILE" -s -o "$HTML_FILE"

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: HTML 轉換失敗"
    exit 1
fi
echo "HTML 已生成: $HTML_FILE"

# ----------------------------
# 本地預覽
# ----------------------------
echo "Step 2: 本地預覽 HTML"
open "$HTML_FILE"

# ----------------------------
# Git commit & push
# ----------------------------
echo "Step 3: Commit & push 到 GitHub"
git add .
git commit -m "Update AWG.py and portfolio site"
git push -u origin main

echo "部署完成！"
echo "GitHub Pages 網址: https://peterlmg28-bot.github.io/AWG/"



#!/bin/bash

PROJECT_PATH="/Users/peterlin/Documents/augment-projects/AWG"
GITHUB_REPO="git@github.com:peterlmg28-bot/AWG.git"
FILE="AWG.py"

cd "$PROJECT_PATH"

# 初始化 git（如尚未初始化）
if [ ! -d ".git" ]; then
  git init
  git remote add origin "$GITHUB_REPO"
  git branch -M main
fi

# Git commit & push
git add "$FILE"
git commit -m "Update AWG.py code"
git push -u origin main

echo "$FILE 已成功上傳到 GitHub!"


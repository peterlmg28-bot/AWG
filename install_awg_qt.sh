#!/bin/bash
set -e

# 安裝 Homebrew（如尚未安裝）
if ! command -v brew &> /dev/null; then
  echo "安裝 Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 安裝 Qt5 和 pkg-config
brew install pkg-config qt@5

# 設定 Qt5 pkg-config 路徑
export PKG_CONFIG_PATH="/usr/local/opt/qt@5/lib/pkgconfig"

# 編譯 awg_qt.cpp
if [ ! -f awg_qt.cpp ]; then
  echo "找不到 awg_qt.cpp，請確認檔案在此資料夾。"
  exit 1
fi

g++ -std=c++11 awg_qt.cpp -o awg_qt `pkg-config --cflags --libs Qt5Widgets`

# 執行程式
./awg_qt

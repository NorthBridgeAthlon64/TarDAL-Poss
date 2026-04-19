#!/usr/bin/env bash
# TarDAL-Poss：一键启动后端 + 前端（macOS / Linux）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "========================================"
echo "  TarDAL-Poss 一键启动（后端 + 前端）"
echo "========================================"

if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
  echo "[错误] 未找到 python，请先安装 Python 3.10+。"
  exit 1
fi
PYTHON="python3"
command -v python3 >/dev/null 2>&1 || PYTHON="python"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PYTHON="$ROOT/.venv/bin/python"
  echo "[TarDAL-Poss] 使用虚拟环境: .venv"
fi

if ! "$PYTHON" -c "import flask" 2>/dev/null; then
  echo "[提示] 未检测到 Flask 等依赖，请在项目根目录执行:"
  echo "  pip install -r requirements.txt"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "[错误] 未找到 npm，请先安装 Node.js LTS。"
  exit 1
fi

if [[ ! -d "$ROOT/frontend/node_modules" ]]; then
  echo "[提示] 正在安装前端依赖..."
  (cd "$ROOT/frontend" && npm install)
fi

cleanup() {
  [[ -n "${BACK_PID:-}" ]] && kill "$BACK_PID" 2>/dev/null || true
  [[ -n "${FRONT_PID:-}" ]] && kill "$FRONT_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "[1/2] 启动后端 (Flask)..."
(cd "$ROOT" && "$PYTHON" backend/app.py) &
BACK_PID=$!

sleep 2

echo "[2/2] 启动前端 (Vite)..."
(cd "$ROOT/frontend" && npm run dev) &
FRONT_PID=$!

echo ""
echo "后端 PID: $BACK_PID  前端 PID: $FRONT_PID"
echo "访问: http://127.0.0.1:5173/TarDAL-Poss/"
echo "按 Ctrl+C 结束两个进程。"
echo ""

wait

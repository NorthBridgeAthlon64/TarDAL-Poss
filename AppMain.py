#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TarDAL 图像融合系统启动脚本
同时启动后端服务器和前端页面
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path
from threading import Thread

def start_backend():
    """启动Flask后端服务器"""
    print("🚀 启动后端服务器...")
    
    # 切换到项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 启动Flask应用
    try:
        subprocess.run([sys.executable, "backend/start_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  后端服务器已停止")
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")

def open_frontend():
    """打开前端页面"""
    time.sleep(3)  # 等待后端启动
    
    frontend_path = Path(__file__).parent / "frontend" / "index.html"
    frontend_url = f"file://{frontend_path.absolute()}"
    
    print(f"🌐 打开前端页面: {frontend_url}")
    webbrowser.open(frontend_url)

def main():
    print("=" * 60)
    print("🎯 TarDAL 图像融合系统")
    print("=" * 60)
    print("📋 系统组件:")
    print("   - 后端服务器: http://localhost:5000")
    print("   - 前端界面: frontend/index.html")
    print("=" * 60)
    
    # 检查依赖
    try:
        import flask
        import torch
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r backend/requirements.txt")
        return
    
    # 在后台线程中打开前端
    frontend_thread = Thread(target=open_frontend, daemon=True)
    frontend_thread.start()
    
    # 启动后端（主线程）
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n👋 系统已停止")

if __name__ == "__main__":
    main()
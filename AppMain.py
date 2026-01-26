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
    """打开前端页面（已禁用 - Vue框架需要通过开发服务器访问）"""
    time.sleep(3)  # 等待后端启动
    
    frontend_path = Path(__file__).parent / "frontend" / "index.html"
    frontend_url = f"file://{frontend_path.absolute()}"
    
    print(f"⚠️  前端页面已禁用自动打开")
    print(f"💡 请使用以下方式启动前端:")
    print(f"   1. 进入前端目录: cd frontend")
    print(f"   2. 安装依赖: npm install")
    print(f"   3. 启动开发服务器: npm run dev")
    print(f"   4. 在浏览器中访问显示的URL（通常是 http://localhost:5173）")
    
    # webbrowser.open(frontend_url)  # 已禁用自动打开

def main():
    print("=" * 60)
    print("🎯 TarDAL 图像融合系统")
    print("=" * 60)
    print("后端服务器通过请求/路由与前端耦合。前后端分开启动，各自运行")
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
    
    # 前端页面已禁用自动打开 - Vue框架需要通过开发服务器访问
    # 如需启动前端，请按照 open_frontend() 函数中的说明操作
    # frontend_thread = Thread(target=open_frontend, daemon=True)
    # frontend_thread.start()
    
    # 启动后端（主线程）
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n👋 系统已停止")

if __name__ == "__main__":
    main()
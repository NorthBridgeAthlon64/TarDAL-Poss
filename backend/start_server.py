#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TarDAL Backend Server 启动脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置工作目录为项目根目录
os.chdir(project_root)

# 导入并运行Flask应用
from backend.app import app, init_tardal_model, logger

if __name__ == '__main__':
    print("=" * 60)
    print("TarDAL 图像融合算法 Web 服务器")
    print("=" * 60)
    
    # 初始化模型
    logger.info("正在初始化TarDAL模型...")
    if init_tardal_model():
        logger.info("✅ 模型初始化成功")
    else:
        logger.error("❌ 模型初始化失败")
        sys.exit(1)
    
    # 启动服务器
    logger.info("🚀 启动Flask服务器...")
    logger.info("📡 服务器地址: http://localhost:5000")
    logger.info("📋 API文档:")
    logger.info("   - GET  /api/health          - 健康检查")
    logger.info("   - POST /api/upload          - 上传图像")
    logger.info("   - POST /api/process         - 处理图像")
    logger.info("   - GET  /api/result/<file>   - 获取结果")
    logger.info("   - DEL  /api/cleanup/<id>    - 清理文件")
    print("=" * 60)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # 生产环境关闭debug
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)
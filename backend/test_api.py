#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TarDAL Backend API 测试脚本
用于测试后端API的各个端点
"""

import requests
import json
from pathlib import Path

# API配置
API_BASE_URL = 'http://localhost:5000/api'

def test_health():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f'{API_BASE_URL}/health')
        result = response.json()
        print(f"✅ 健康检查: {result}")
        return result.get('model_loaded', False)
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_upload():
    """测试文件上传接口"""
    print("📤 测试文件上传接口...")
    
    # 使用示例图像
    ir_path = Path('../assets/sample/s1/ir/M3FD_00471.png')
    vi_path = Path('../assets/sample/s1/vi/M3FD_00471.png')
    
    if not ir_path.exists() or not vi_path.exists():
        print("❌ 示例图像文件不存在")
        return None
    
    try:
        files = {
            'ir_image': ('ir_test.png', open(ir_path, 'rb'), 'image/png'),
            'vi_image': ('vi_test.png', open(vi_path, 'rb'), 'image/png')
        }
        
        response = requests.post(f'{API_BASE_URL}/upload', files=files)
        result = response.json()
        
        # 关闭文件
        files['ir_image'][1].close()
        files['vi_image'][1].close()
        
        if result.get('success'):
            print(f"✅ 文件上传成功: {result}")
            return result.get('session_id')
        else:
            print(f"❌ 文件上传失败: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 文件上传异常: {e}")
        return None

def test_process(session_id):
    """测试图像处理接口"""
    print("⚙️  测试图像处理接口...")
    
    if not session_id:
        print("❌ 没有有效的session_id")
        return None
    
    try:
        data = {'session_id': session_id}
        response = requests.post(
            f'{API_BASE_URL}/process',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        
        result = response.json()
        
        if result.get('success'):
            print(f"✅ 图像处理成功: {result}")
            return result.get('result_filename')
        else:
            print(f"❌ 图像处理失败: {result}")
            return None
            
    except Exception as e:
        print(f"❌ 图像处理异常: {e}")
        return None

def test_result(filename):
    """测试结果获取接口"""
    print("📥 测试结果获取接口...")
    
    if not filename:
        print("❌ 没有有效的结果文件名")
        return False
    
    try:
        response = requests.get(f'{API_BASE_URL}/result/{filename}')
        
        if response.status_code == 200:
            print(f"✅ 结果获取成功，文件大小: {len(response.content)} bytes")
            
            # 保存测试结果
            test_result_path = Path('test_result.png')
            with open(test_result_path, 'wb') as f:
                f.write(response.content)
            print(f"💾 测试结果已保存到: {test_result_path}")
            return True
        else:
            print(f"❌ 结果获取失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 结果获取异常: {e}")
        return False

def test_cleanup(session_id):
    """测试清理接口"""
    print("🧹 测试清理接口...")
    
    if not session_id:
        print("❌ 没有有效的session_id")
        return False
    
    try:
        response = requests.delete(f'{API_BASE_URL}/cleanup/{session_id}')
        result = response.json()
        
        if result.get('success'):
            print(f"✅ 清理成功: {result}")
            return True
        else:
            print(f"❌ 清理失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 清理异常: {e}")
        return False

def main():
    """主测试流程"""
    print("=" * 60)
    print("🧪 TarDAL Backend API 测试")
    print("=" * 60)
    
    # 1. 健康检查
    if not test_health():
        print("❌ 后端服务不可用，请先启动服务器")
        return
    
    print()
    
    # 2. 文件上传
    session_id = test_upload()
    if not session_id:
        print("❌ 文件上传失败，无法继续测试")
        return
    
    print()
    
    # 3. 图像处理
    result_filename = test_process(session_id)
    if not result_filename:
        print("❌ 图像处理失败，无法继续测试")
        return
    
    print()
    
    # 4. 结果获取
    if not test_result(result_filename):
        print("❌ 结果获取失败")
    
    print()
    
    # 5. 清理文件
    test_cleanup(session_id)
    
    print()
    print("=" * 60)
    print("🎉 API 测试完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
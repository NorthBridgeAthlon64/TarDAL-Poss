# TarDAL 图像融合 Web 系统

基于 TarDAL 算法的红外与可见光图像融合 Web 应用系统。

## 🎯 系统架构

```
TarDAL-WebSystem/
├── backend/                 # Flask 后端服务
│   ├── app.py              # 主应用文件
│   ├── start_server.py     # 服务器启动脚本
│   ├── requirements.txt    # Python 依赖
│   ├── uploads/           # 上传文件目录
│   └── results/           # 处理结果目录
├── frontend/               # 前端界面
│   ├── index.html         # 主页面
│   └── script.js          # JavaScript 逻辑
├── run_system.py          # 系统启动脚本
└── README_WebSystem.md    # 本文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装后端依赖
pip install -r backend/requirements.txt
```

### 2. 启动系统

**方法一：一键启动（推荐）**
```bash
python run_system.py
```

**方法二：分别启动**
```bash
# 启动后端服务器
python backend/start_server.py

# 然后在浏览器中打开 frontend/index.html
```

### 3. 使用系统

1. **上传图像**：分别上传红外图像和可见光图像
2. **开始融合**：点击"开始融合"按钮
3. **查看结果**：等待处理完成，查看融合结果和性能指标
4. **下载结果**：点击"下载结果"保存融合图像

## 📡 API 接口

### 后端 API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/upload` | 上传图像文件 |
| POST | `/api/process` | 执行图像融合 |
| GET | `/api/result/<filename>` | 获取结果图像 |
| DELETE | `/api/cleanup/<session_id>` | 清理会话文件 |

### 请求示例

**上传文件**
```javascript
const formData = new FormData();
formData.append('ir_image', irFile);
formData.append('vi_image', viFile);

fetch('http://localhost:5000/api/upload', {
    method: 'POST',
    body: formData
})
```

**处理图像**
```javascript
fetch('http://localhost:5000/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: 'your-session-id' })
})
```

## 🔧 配置说明

### 后端配置

- **端口**: 5000（可在 `backend/app.py` 中修改）
- **最大文件大小**: 16MB
- **支持格式**: PNG, JPG, JPEG, BMP
- **模型配置**: 使用 `config/official/infer/tardal-dt.yaml`

### 前端配置

- **API 地址**: `http://localhost:5000/api`（可在 `frontend/script.js` 中修改）
- **支持的浏览器**: Chrome, Firefox, Safari, Edge

## 📊 性能指标

系统会计算并显示以下指标：

- **PSNR**: 峰值信噪比（dB）
- **SSIM**: 结构相似性指数
- **检测提升**: 目标检测准确率提升百分比
- **处理时间**: 算法执行时间（秒）

## 🛠️ 开发说明

### 后端开发

后端基于 Flask 框架，主要文件：

- `app.py`: 主应用逻辑，包含所有 API 端点
- `start_server.py`: 服务器启动和初始化脚本

核心功能：
- 文件上传和验证
- TarDAL 模型加载和推理
- 图像处理和结果保存
- 会话管理和文件清理

### 前端开发

前端使用原生 JavaScript，主要文件：

- `index.html`: 页面结构和样式
- `script.js`: 交互逻辑和 API 调用

核心功能：
- 拖拽上传界面
- 实时预览和进度显示
- API 交互和错误处理
- 结果展示和下载

## 🔍 故障排除

### 常见问题

**1. 后端启动失败**
- 检查 Python 环境和依赖安装
- 确保端口 5000 未被占用
- 查看控制台错误信息

**2. 模型加载失败**
- 检查 TarDAL 项目文件完整性
- 确保配置文件路径正确
- 检查预训练模型是否下载

**3. 前端无法连接后端**
- 确认后端服务器正在运行
- 检查 API 地址配置
- 查看浏览器控制台错误

**4. 图像处理失败**
- 检查图像格式和大小
- 确保图像文件未损坏
- 查看后端日志信息

### 日志查看

后端日志会显示详细的处理信息：
```
2024-01-24 20:30:11,799 | INFO | 正在初始化TarDAL模型...
2024-01-24 20:30:11,851 | INFO | init generator with (dim: 32 depth: 3)
2024-01-24 20:30:11,999 | INFO | 文件上传成功: xxx_ir.png, xxx_vi.png
```

## 📝 更新日志

### v1.0.0
- ✅ 完整的 Web 系统实现
- ✅ Flask 后端 API 服务
- ✅ 响应式前端界面
- ✅ 拖拽上传功能
- ✅ 实时处理进度
- ✅ 性能指标展示
- ✅ 结果下载功能

## 📄 许可证

本项目基于原 TarDAL 项目的许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个系统！

---

**享受使用 TarDAL 图像融合系统！** 🎉
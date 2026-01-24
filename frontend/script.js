/**
 * TarDAL 图像融合系统前端脚本
 * 与Flask后端API交互，实现图像上传、处理和结果展示
 */

// 配置
const API_BASE_URL = 'http://localhost:5000/api';

// DOM元素
const elements = {
    irUpload: document.getElementById('irUpload'),
    viUpload: document.getElementById('viUpload'),
    irInput: document.getElementById('irInput'),
    viInput: document.getElementById('viInput'),
    irPreview: document.getElementById('irPreview'),
    viPreview: document.getElementById('viPreview'),
    processBtn: document.getElementById('processBtn'),
    clearBtn: document.getElementById('clearBtn'),
    downloadBtn: document.getElementById('downloadBtn'),
    statusInfo: document.getElementById('statusInfo'),
    progressContainer: document.getElementById('progressContainer'),
    progressBar: document.getElementById('progressBar'),
    progressText: document.getElementById('progressText'),
    resultImage: document.getElementById('resultImage'),
    resultPlaceholder: document.getElementById('resultPlaceholder'),
    metricsPanel: document.getElementById('metricsPanel'),
    errorMessage: document.getElementById('errorMessage'),
    successMessage: document.getElementById('successMessage'),
    psnrValue: document.getElementById('psnrValue'),
    ssimValue: document.getElementById('ssimValue'),
    detectionValue: document.getElementById('detectionValue'),
    timeValue: document.getElementById('timeValue')
};

// 应用状态
const appState = {
    irFile: null,
    viFile: null,
    sessionId: null,
    resultFilename: null,
    isProcessing: false
};

// 工具函数
const utils = {
    // 显示错误消息
    showError(message) {
        elements.errorMessage.textContent = message;
        elements.errorMessage.style.display = 'block';
        elements.successMessage.style.display = 'none';
        setTimeout(() => {
            elements.errorMessage.style.display = 'none';
        }, 5000);
    },

    // 显示成功消息
    showSuccess(message) {
        elements.successMessage.textContent = message;
        elements.successMessage.style.display = 'block';
        elements.errorMessage.style.display = 'none';
        setTimeout(() => {
            elements.successMessage.style.display = 'none';
        }, 3000);
    },

    // 更新状态信息
    updateStatus(message, icon = 'info-circle') {
        elements.statusInfo.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
    },

    // 格式化文件大小
    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        else if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        else return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    },

    // 检查文件类型
    isValidImageFile(file) {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp'];
        return validTypes.includes(file.type);
    },

    // 检查文件大小
    isValidFileSize(file, maxSizeMB = 16) {
        return file.size <= maxSizeMB * 1024 * 1024;
    }
};

// 文件处理函数
const fileHandler = {
    // 处理文件选择
    handleFileSelect(file, type) {
        // 验证文件
        if (!utils.isValidImageFile(file)) {
            utils.showError('请选择有效的图像文件（JPG、PNG、BMP格式）');
            return;
        }

        if (!utils.isValidFileSize(file)) {
            utils.showError('文件大小不能超过16MB');
            return;
        }

        // 保存文件到状态
        if (type === 'ir') {
            appState.irFile = file;
            this.showPreview(file, elements.irPreview, elements.irUpload);
        } else {
            appState.viFile = file;
            this.showPreview(file, elements.viPreview, elements.viUpload);
        }

        // 更新UI状态
        this.updateUploadStatus();
    },

    // 显示图像预览
    showPreview(file, previewElement, uploadArea) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
            uploadArea.classList.add('has-image');
            
            // 隐藏上传提示
            const icon = uploadArea.querySelector('.upload-icon');
            const text = uploadArea.querySelector('.upload-text');
            const hint = uploadArea.querySelector('.upload-hint');
            
            icon.style.display = 'none';
            text.style.display = 'none';
            hint.style.display = 'none';
        };
        reader.readAsDataURL(file);
    },

    // 更新上传状态
    updateUploadStatus() {
        const hasIr = appState.irFile !== null;
        const hasVi = appState.viFile !== null;

        if (hasIr && hasVi) {
            utils.updateStatus('图像已准备就绪，可以开始融合', 'check-circle');
            elements.processBtn.disabled = false;
        } else if (hasIr) {
            utils.updateStatus('已上传红外图像，请上传可见光图像', 'thermometer-half');
            elements.processBtn.disabled = true;
        } else if (hasVi) {
            utils.updateStatus('已上传可见光图像，请上传红外图像', 'eye');
            elements.processBtn.disabled = true;
        } else {
            utils.updateStatus('请上传两张图像', 'info-circle');
            elements.processBtn.disabled = true;
        }
    },

    // 清空所有文件
    clearAll() {
        appState.irFile = null;
        appState.viFile = null;
        appState.sessionId = null;
        appState.resultFilename = null;

        // 重置预览
        elements.irPreview.style.display = 'none';
        elements.viPreview.style.display = 'none';
        elements.irUpload.classList.remove('has-image');
        elements.viUpload.classList.remove('has-image');

        // 显示上传提示
        [elements.irUpload, elements.viUpload].forEach(area => {
            area.querySelector('.upload-icon').style.display = 'block';
            area.querySelector('.upload-text').style.display = 'block';
            area.querySelector('.upload-hint').style.display = 'block';
        });

        // 重置结果区域
        elements.resultImage.style.display = 'none';
        elements.resultPlaceholder.style.display = 'block';
        elements.metricsPanel.style.display = 'none';
        elements.downloadBtn.disabled = true;

        // 重置进度条
        elements.progressContainer.style.display = 'none';

        this.updateUploadStatus();
        utils.showSuccess('已清空所有内容');
    }
};

// API调用函数
const api = {
    // 上传文件
    async uploadFiles() {
        const formData = new FormData();
        formData.append('ir_image', appState.irFile);
        formData.append('vi_image', appState.viFile);

        try {
            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || '上传失败');
            }

            appState.sessionId = result.session_id;
            return result;

        } catch (error) {
            throw new Error(`上传失败: ${error.message}`);
        }
    },

    // 处理图像
    async processImages() {
        try {
            const response = await fetch(`${API_BASE_URL}/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: appState.sessionId
                })
            });

            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || '处理失败');
            }

            appState.resultFilename = result.result_filename;
            return result;

        } catch (error) {
            throw new Error(`处理失败: ${error.message}`);
        }
    },

    // 获取结果图像URL
    getResultImageUrl(filename) {
        return `${API_BASE_URL}/result/${filename}`;
    },

    // 清理会话文件
    async cleanupSession() {
        if (!appState.sessionId) return;

        try {
            await fetch(`${API_BASE_URL}/cleanup/${appState.sessionId}`, {
                method: 'DELETE'
            });
        } catch (error) {
            console.warn('清理会话文件失败:', error);
        }
    }
};

// 进度条控制
const progressController = {
    show() {
        elements.progressContainer.style.display = 'block';
        this.reset();
    },

    hide() {
        elements.progressContainer.style.display = 'none';
        this.reset();
    },

    reset() {
        elements.progressBar.style.width = '0%';
        elements.progressText.textContent = '0%';
    },

    update(percent) {
        elements.progressBar.style.width = percent + '%';
        elements.progressText.textContent = Math.round(percent) + '%';
    },

    // 模拟进度动画
    animate(duration = 3000) {
        return new Promise((resolve) => {
            let progress = 0;
            const increment = 100 / (duration / 100);
            
            const interval = setInterval(() => {
                progress += increment + Math.random() * 5;
                if (progress >= 95) {
                    progress = 95;
                    clearInterval(interval);
                    resolve();
                }
                this.update(progress);
            }, 100);
        });
    }
};

// 主要业务逻辑
const imageProcessor = {
    // 开始处理流程
    async startProcessing() {
        if (appState.isProcessing) return;
        
        console.log('开始处理流程');
        appState.isProcessing = true;
        elements.processBtn.disabled = true;
        elements.processBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 处理中...';

        try {
            // 1. 显示进度条
            progressController.show();
            utils.updateStatus('正在上传图像...', 'cloud-upload-alt');

            // 2. 上传文件
            console.log('上传文件...');
            const uploadResult = await api.uploadFiles();
            console.log('上传结果:', uploadResult);
            progressController.update(30);
            
            // 3. 开始处理
            utils.updateStatus('正在执行TarDAL融合算法...', 'cogs');
            
            // 启动进度动画
            const progressPromise = progressController.animate(4000);
            
            // 4. 调用处理API
            console.log('开始处理图像...');
            const processPromise = api.processImages();
            
            // 等待处理完成
            const [, result] = await Promise.all([progressPromise, processPromise]);
            console.log('处理结果:', result);
            
            // 5. 完成进度
            progressController.update(100);
            
            // 6. 显示结果
            console.log('显示结果...');
            await imageProcessor.showResult(result);
            
            utils.showSuccess('图像融合完成！');

        } catch (error) {
            console.error('处理失败:', error);
            utils.showError(error.message);
        } finally {
            // 7. 重置状态
            appState.isProcessing = false;
            elements.processBtn.disabled = false;
            elements.processBtn.innerHTML = '<i class="fas fa-cogs"></i> 开始融合';
            progressController.hide();
            utils.updateStatus('处理完成', 'check-circle');
        }
    },

    // 显示处理结果
    async showResult(result) {
        try {
            console.log('显示结果:', result);
            
            // 显示融合图像
            const imageUrl = api.getResultImageUrl(result.result_filename);
            console.log('图像URL:', imageUrl);
            
            // 添加图像加载事件监听
            elements.resultImage.onload = function() {
                console.log('图像加载成功');
                elements.resultImage.style.display = 'block';
                elements.resultPlaceholder.style.display = 'none';
            };
            
            elements.resultImage.onerror = function() {
                console.error('图像加载失败');
                utils.showError('无法加载融合结果图像');
            };
            
            elements.resultImage.src = imageUrl;

            // 显示性能指标
            const metrics = result.metrics;
            console.log('性能指标:', metrics);
            
            elements.psnrValue.textContent = metrics.psnr.toFixed(1);
            elements.ssimValue.textContent = metrics.ssim.toFixed(3);
            elements.detectionValue.textContent = metrics.detection_improvement.toFixed(0) + '%';
            elements.timeValue.textContent = metrics.processing_time.toFixed(1) + 's';
            
            elements.metricsPanel.style.display = 'grid';
            elements.downloadBtn.disabled = false;

            // 添加动画效果
            setTimeout(() => {
                elements.metricsPanel.style.animation = 'fadeIn 0.5s ease-in';
            }, 100);
            
        } catch (error) {
            console.error('显示结果失败:', error);
            utils.showError('显示结果失败: ' + error.message);
        }
    },

    // 下载结果
    downloadResult() {
        if (!appState.resultFilename) {
            utils.showError('没有可下载的结果');
            return;
        }

        const link = document.createElement('a');
        link.href = api.getResultImageUrl(appState.resultFilename);
        link.download = `TarDAL_fused_${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        utils.showSuccess('结果图像下载开始');
    }
};

// 拖拽处理
const dragDropHandler = {
    init() {
        // 为上传区域添加拖拽事件
        [elements.irUpload, elements.viUpload].forEach((area, index) => {
            const type = index === 0 ? 'ir' : 'vi';
            
            area.addEventListener('dragover', (e) => {
                e.preventDefault();
                area.classList.add('dragover');
            });

            area.addEventListener('dragleave', (e) => {
                e.preventDefault();
                area.classList.remove('dragover');
            });

            area.addEventListener('drop', (e) => {
                e.preventDefault();
                area.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    fileHandler.handleFileSelect(files[0], type);
                }
            });
        });
    }
};

// 事件监听器设置
function setupEventListeners() {
    // 上传区域点击事件
    elements.irUpload.addEventListener('click', () => elements.irInput.click());
    elements.viUpload.addEventListener('click', () => elements.viInput.click());

    // 文件输入事件
    elements.irInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileHandler.handleFileSelect(e.target.files[0], 'ir');
        }
    });

    elements.viInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileHandler.handleFileSelect(e.target.files[0], 'vi');
        }
    });

    // 按钮事件
    elements.processBtn.addEventListener('click', imageProcessor.startProcessing);
    elements.clearBtn.addEventListener('click', fileHandler.clearAll);
    elements.downloadBtn.addEventListener('click', imageProcessor.downloadResult);

    // 页面卸载时清理会话
    window.addEventListener('beforeunload', () => {
        api.cleanupSession();
    });
}

// 初始化应用
function initApp() {
    console.log('TarDAL 图像融合系统初始化...');
    
    // 设置事件监听器
    setupEventListeners();
    
    // 初始化拖拽功能
    dragDropHandler.init();
    
    // 检查后端连接
    checkBackendConnection();
    
    console.log('系统初始化完成');
}

// 检查后端连接
async function checkBackendConnection() {
    try {
        console.log('检查后端连接...');
        const response = await fetch(`${API_BASE_URL}/health`);
        const result = await response.json();
        
        console.log('后端健康检查结果:', result);
        
        if (result.status === 'healthy' && result.model_loaded) {
            utils.updateStatus('系统就绪，请上传图像', 'check-circle');
            console.log('✅ 后端连接成功，模型已加载');
        } else {
            utils.showError('后端模型未加载，请检查服务器状态');
            console.log('❌ 后端模型未加载');
        }
    } catch (error) {
        utils.showError('无法连接到后端服务器，请确保服务器正在运行');
        console.error('❌ 后端连接失败:', error);
    }
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initApp);
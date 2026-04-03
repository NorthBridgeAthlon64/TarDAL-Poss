<template>
  <section class="fusion-shell">
    <header class="fusion-header">
      <h2>TarDAL图像融合系统</h2>
      <p>基于双对抗学习的红外与可见光图像融合算法</p>
    </header>

    <div class="upload-section">
      <div
        class="upload-area"
        :class="{ 'dragover': dragState.ir, 'has-image': !!irImage }"
        @click="triggerFile('ir')"
        @dragover.prevent="dragState.ir = true"
        @dragleave.prevent="dragState.ir = false"
        @drop.prevent="onDrop('ir', $event)"
      >
        <template v-if="!irImage">
          <i class="fas fa-thermometer-half upload-icon"></i>
          <div class="upload-text">上传红外图像</div>
          <div class="upload-hint">点击或拖拽文件到此处</div>
        </template>
        <img v-else class="upload-preview" :src="irImage" alt="红外图像预览" />
        <input ref="irInput" type="file" accept="image/*" class="hidden" @change="onFileChange('ir', $event)" />
      </div>

      <div
        class="upload-area"
        :class="{ 'dragover': dragState.vi, 'has-image': !!viImage }"
        @click="triggerFile('vi')"
        @dragover.prevent="dragState.vi = true"
        @dragleave.prevent="dragState.vi = false"
        @drop.prevent="onDrop('vi', $event)"
      >
        <template v-if="!viImage">
          <i class="fas fa-eye upload-icon"></i>
          <div class="upload-text">上传可见光图像</div>
          <div class="upload-hint">点击或拖拽文件到此处</div>
        </template>
        <img v-else class="upload-preview" :src="viImage" alt="可见光图像预览" />
        <input ref="viInput" type="file" accept="image/*" class="hidden" @change="onFileChange('vi', $event)" />
      </div>
    </div>

    <div class="control-panel">
      <button class="btn process-btn" :disabled="!ready || processing" @click="startFusion">
        <i :class="processing ? 'fas fa-spinner fa-spin' : 'fas fa-cogs'"></i>
        <span>{{ processing ? '融合处理中...' : '开始融合' }}</span>
      </button>
      <button class="btn clear-btn" :disabled="processing && !ready" @click="clearAll">
        <i class="fas fa-trash"></i>
        <span>清空重置</span>
      </button>
      <div class="status-info">
        <i class="fas fa-info-circle"></i>
        <span>{{ statusText }}</span>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="processing" class="progress-container">
        <div class="progress-header">
          <span>处理进度</span>
          <span>{{ Math.round(progress) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress" :style="{ width: `${progress}%` }"></div>
        </div>
      </div>
    </Transition>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

    <div class="result-section">
      <h3>融合结果</h3>
      <div class="stages-container">
        <div class="stage-container">
          <h4>第一阶段：输入图像</h4>
          <div v-if="!irImage || !viImage" class="result-placeholder">
            <i class="fas fa-image"></i>
            请上传红外和可见光图像
          </div>
          <div v-else class="input-images-container">
            <div class="input-image-wrapper">
              <img class="input-image" :src="irImage" alt="红外输入图像" />
              <div class="input-image-label">红外图像</div>
            </div>
            <div class="input-image-wrapper">
              <img class="input-image" :src="viImage" alt="可见光输入图像" />
              <div class="input-image-label">可见光图像</div>
            </div>
          </div>
        </div>
        <div class="stage-container">
          <h4>第二阶段：目标显著性</h4>
          <p class="stage-desc">从红外图提取的目标/人体轮廓（单通道，背景黑）</p>
          <div v-if="!stage2Image" class="result-placeholder">
            <i class="fas fa-image"></i>
            第二阶段结果将显示在此处
          </div>
          <img v-else class="result-image" :src="stage2Image" alt="第二阶段：目标显著性" />
        </div>
        <div class="stage-container">
          <h4>第三阶段：TarDAL 融合图</h4>
          <p class="stage-desc">单通道灰度图：目标像红外（突出），背景像可见光（纹理清晰）</p>
          <div v-if="!stage3Image" class="result-placeholder">
            <i class="fas fa-image"></i>
            第三阶段结果将显示在此处
          </div>
          <img v-else class="result-image" :src="stage3Image" alt="第三阶段：TarDAL 融合图" />
          <button class="btn download-btn" :disabled="!stage3Image" @click="downloadResult">
            <i class="fas fa-download"></i>
            <span>下载结果</span>
          </button>
        </div>
      </div>

      <div v-if="metricsReady" class="metrics-panel">
        <div class="metric">
          <div class="metric-value">{{ metrics.psnr.toFixed(1) }}</div>
          <div class="metric-label">PSNR (dB)</div>
        </div>
        <div class="metric">
          <div class="metric-value">{{ metrics.ssim.toFixed(3) }}</div>
          <div class="metric-label">SSIM</div>
        </div>
        <div class="metric">
          <div class="metric-value">{{ metrics.detection.toFixed(0) }}%</div>
          <div class="metric-label">检测提升</div>
        </div>
        <div class="metric">
          <div class="metric-value">{{ metrics.time.toFixed(1) }}s</div>
          <div class="metric-label">处理时间</div>
        </div>
      </div>

      <div v-if="advancedMetricsReady" class="advanced-metrics-panel">
        <h4>高级指标</h4>
        <div class="metrics-panel">
          <div class="metric">
            <div class="metric-value">{{ advancedMetrics.entropy_preservation.toFixed(3) }}</div>
            <div class="metric-label">熵保持</div>
          </div>
          <div class="metric">
            <div class="metric-value">{{ advancedMetrics.gradient_preservation.toFixed(3) }}</div>
            <div class="metric-label">梯度保持</div>
          </div>
          <div class="metric">
            <div class="metric-value">{{ advancedMetrics.contrast_enhancement.toFixed(3) }}</div>
            <div class="metric-label">对比度增强</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue';

const irInput = ref(null);
const viInput = ref(null);
const irImage = ref(null);
const viImage = ref(null);
const stage1Image = ref(null);
const stage2Image = ref(null);
const stage3Image = ref(null);
const processing = ref(false);
const progress = ref(0);
const errorMessage = ref('');
const successMessage = ref('');
const dragState = ref({ ir: false, vi: false });
const metrics = ref({ psnr: null, ssim: null, detection: null, time: null });
const advancedMetrics = ref({ entropy_preservation: null, gradient_preservation: null, contrast_enhancement: null });
let progressTimer = null;

const ready = computed(() => !!irImage.value && !!viImage.value);
const statusText = computed(() => {
  if (processing.value) return '融合处理中，请稍候';
  if (!ready.value) return '请上传两张图像';
  if (stage3Image.value) return '融合完成，可下载结果';
  return '已就绪，点击开始融合';
});
const metricsReady = computed(() => Object.values(metrics.value).every((v) => typeof v === 'number'));
const advancedMetricsReady = computed(() => Object.values(advancedMetrics.value).every((v) => typeof v === 'number'));

function triggerFile(kind) {
  if (kind === 'ir') irInput.value?.click();
  if (kind === 'vi') viInput.value?.click();
}

function onFileChange(kind, event) {
  const [file] = event.target.files || [];
  loadImageFile(kind, file);
  event.target.value = '';
}

function onDrop(kind, event) {
  dragState.value[kind] = false;
  const [file] = event.dataTransfer?.files || [];
  loadImageFile(kind, file);
}

function loadImageFile(kind, file) {
  if (!file) return;
  if (!file.type.match('image')) {
    errorMessage.value = '请上传图像文件（JPG/PNG 等）';
    return;
  }
  if (file.size > 15 * 1024 * 1024) {
    errorMessage.value = '文件大小不能超过 15MB';
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    if (kind === 'ir') irImage.value = e.target?.result;
    if (kind === 'vi') viImage.value = e.target?.result;
    resetResult();
    successMessage.value = '';
    errorMessage.value = '';
  };
  reader.readAsDataURL(file);
}

async function startFusion() {
  if (!ready.value) {
    errorMessage.value = '请先上传红外和可见光两张图像';
    return;
  }

  processing.value = true;
  progress.value = 0;
  errorMessage.value = '';
  successMessage.value = '';
  startProgressAnimation();

  try {
    const { stage2Url, stage3Url, metrics: resultMetrics, advancedMetrics: resultAdvancedMetrics } = await runFusion(irImage.value, viImage.value);
    stage2Image.value = stage2Url;
    stage3Image.value = stage3Url;
    metrics.value = resultMetrics;
    if (resultAdvancedMetrics) {
      advancedMetrics.value = resultAdvancedMetrics;
    }
    progress.value = 100;
    successMessage.value = '融合完成，您可以下载结果';
  } catch (err) {
    console.error(err);
    errorMessage.value = err?.message || '处理失败，请重试';
  } finally {
    stopProgressAnimation();
    processing.value = false;
    progress.value = 0;
  }
}

function startProgressAnimation() {
  stopProgressAnimation();
  progressTimer = setInterval(() => {
    progress.value = Math.min(96, progress.value + Math.random() * 9 + 4);
  }, 180);
}

function stopProgressAnimation() {
  if (progressTimer) {
    clearInterval(progressTimer);
    progressTimer = null;
  }
}

async function runFusion(irSrc, viSrc) {
  try {
    // 将dataURL转换为Blob
    const irBlob = await dataURLToBlob(irSrc);
    const viBlob = await dataURLToBlob(viSrc);

    // 1. 上传图像
    const uploadForm = new FormData();
    uploadForm.append('ir_image', irBlob, 'ir_image.png');
    uploadForm.append('vi_image', viBlob, 'vi_image.png');

    const uploadResponse = await fetch('http://localhost:5000/api/upload', {
      method: 'POST',
      body: uploadForm
    });

    if (!uploadResponse.ok) {
      throw new Error('上传失败: ' + uploadResponse.statusText);
    }

    const uploadData = await uploadResponse.json();
    if (!uploadData.success) {
      throw new Error('上传失败: ' + uploadData.error);
    }

    const sessionId = uploadData.session_id;

    // 2. 处理融合
    const processResponse = await fetch('http://localhost:5000/api/process', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ session_id: sessionId })
    });

    if (!processResponse.ok) {
      throw new Error('处理失败: ' + processResponse.statusText);
    }

    const processData = await processResponse.json();
    if (!processData.success) {
      throw new Error('处理失败: ' + processData.error);
    }

    // 3. 构建结果图像URL
    const stage2Url = `http://localhost:5000/api/result/${sessionId}_stage2.png`;
    const stage3Url = `http://localhost:5000/api/result/${sessionId}_fused.png`;

    // 4. 构建返回数据
    const resultMetrics = {
      psnr: processData.metrics.psnr,
      ssim: processData.metrics.ssim,
      detection: processData.metrics.detection_improvement,
      time: processData.metrics.processing_time
    };

    // 5. 构建高级指标数据
    const resultAdvancedMetrics = {
      entropy_preservation: processData.metrics.entropy_preservation,
      gradient_preservation: processData.metrics.gradient_preservation,
      contrast_enhancement: processData.metrics.contrast_enhancement
    };

    return { stage2Url, stage3Url, metrics: resultMetrics, advancedMetrics: resultAdvancedMetrics };
  } catch (err) {
    console.error('API调用失败:', err);
    throw new Error('后端服务异常，请确保后端服务已启动并正常运行');
  }
}

function dataURLToBlob(dataUrl) {
  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', dataUrl);
    xhr.responseType = 'blob';
    xhr.onload = () => {
      resolve(xhr.response);
    };
    xhr.send();
  });
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('图像加载失败'));
    img.src = src;
  });
}

function downloadResult() {
  if (!stage3Image.value) return;
  const link = document.createElement('a');
  link.download = 'TarDAL_fused.png';
  link.href = stage3Image.value;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function clearAll() {
  irImage.value = null;
  viImage.value = null;
  resetResult();
  errorMessage.value = '';
  successMessage.value = '';
}

function resetResult() {
  stage2Image.value = null;
  stage3Image.value = null;
  metrics.value = { psnr: null, ssim: null, detection: null, time: null };
  advancedMetrics.value = { entropy_preservation: null, gradient_preservation: null, contrast_enhancement: null };
}

onBeforeUnmount(() => stopProgressAnimation());
</script>

<style scoped>
.fusion-shell {
  border-radius: 20px;
  border: 1px solid rgba(100, 150, 255, 0.2);
  background: linear-gradient(135deg, #0c1e3e 0%, #1a3a5f 100%);
  padding: 18px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
  color: #e0f0ff;
}

.fusion-header {
  text-align: center;
  padding: 12px 10px 20px;
  border-radius: 14px;
  background: linear-gradient(90deg, rgba(20, 40, 80, 0.7) 0%, rgba(30, 60, 120, 0.7) 100%);
  border: 1px solid rgba(100, 150, 255, 0.25);
  margin-bottom: 14px;
}

.fusion-header h2 {
  font-size: 1.6rem;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  letter-spacing: 0.4px;
}

.fusion-header p { color: #a0c8ff; margin-top: 6px; }

.upload-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
  margin-bottom: 14px;
}

.upload-area {
  border: 2px dashed rgba(100, 150, 255, 0.3);
  border-radius: 15px;
  padding: 28px 16px;
  text-align: center;
  background: rgba(0, 20, 40, 0.5);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.upload-area:hover { border-color: rgba(100, 150, 255, 0.6); background: rgba(0, 30, 60, 0.7); transform: translateY(-2px); }
.upload-area.dragover { border-color: #4facfe; background: rgba(79, 172, 254, 0.1); }
.upload-area.has-image { border-color: #00d48e; background: rgba(0, 212, 142, 0.08); }

.upload-icon { font-size: 2.4rem; color: rgba(100, 150, 255, 0.6); margin-bottom: 12px; }
.upload-text { color: #cde1ff; font-size: 1.05rem; margin-bottom: 6px; }
.upload-hint { color: #7090cc; font-size: 0.9rem; }
.upload-preview { max-width: 100%; max-height: 200px; border-radius: 10px; margin-top: 12px; display: block; object-fit: contain; }

.control-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: flex-start;
  padding: 10px 0;
}

.btn {
  padding: 12px 18px;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-width: 150px;
}

.btn:disabled { background: linear-gradient(90deg, #555 0%, #777 100%); cursor: not-allowed; box-shadow: none; }
.process-btn { background: linear-gradient(90deg, #00a86b 0%, #00d48e 100%); color: #fff; box-shadow: 0 5px 15px rgba(0, 168, 107, 0.4); }
.process-btn:hover:not(:disabled) { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0, 168, 107, 0.55); }
.clear-btn { background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%); color: #fff; box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4); }
.clear-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(231, 76, 60, 0.6); }

.status-info {
  padding: 12px 14px;
  background: rgba(0, 30, 60, 0.5);
  border-radius: 10px;
  border: 1px solid rgba(100, 150, 255, 0.25);
  color: #a0c8ff;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-width: 220px;
}

.progress-container {
  padding: 14px;
  background: rgba(0, 30, 60, 0.7);
  border-radius: 14px;
  border: 1px solid rgba(100, 150, 255, 0.25);
  margin-bottom: 12px;
}

.progress-header { display: flex; justify-content: space-between; margin-bottom: 10px; color: #a0c8ff; }
.progress-bar { height: 12px; background: rgba(0, 20, 40, 0.8); border-radius: 6px; overflow: hidden; }
.progress { height: 100%; background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); width: 0%; transition: width 0.4s ease; border-radius: 6px; }

.error-message, .success-message {
  padding: 12px;
  border-radius: 10px;
  border: 1px solid transparent;
  margin-bottom: 10px;
}
.error-message { background: rgba(231, 76, 60, 0.1); border-color: rgba(231, 76, 60, 0.35); color: #ff7b7b; }
.success-message { background: rgba(0, 212, 142, 0.1); border-color: rgba(0, 212, 142, 0.35); color: #00d48e; }

.result-section { margin-top: 14px; }

.result-section h3 {
  color: #4facfe;
  font-size: 1.2rem;
  margin-bottom: 12px;
  text-align: center;
}

.stages-container {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 18px;
  justify-content: center;
}

.stage-container {
  flex: 1;
  min-width: 280px;
  max-width: 350px;
  background: rgba(0, 20, 40, 0.55);
  border-radius: 15px;
  padding: 18px;
  text-align: center;
  border: 1px solid rgba(100, 150, 255, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stage-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
  border-color: rgba(100, 150, 255, 0.4);
}

.stage-container h4 {
  color: #a0c8ff;
  font-size: 1rem;
  margin-bottom: 6px;
}
.stage-container .stage-desc {
  font-size: 0.8rem;
  color: rgba(160, 200, 255, 0.75);
  margin-bottom: 10px;
  line-height: 1.35;
  font-weight: 500;
}

.advanced-metrics-panel {
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px solid rgba(100, 150, 255, 0.2);
}

.advanced-metrics-panel h4 {
  color: #4facfe;
  font-size: 1rem;
  margin-bottom: 12px;
  text-align: center;
}

.advanced-metrics-panel .metrics-panel {
  margin-top: 12px;
}

/* 第一梯队：核心创新指标 */
.core-metrics-panel {
  margin-top: 20px;
  margin-bottom: 20px;
  padding: 20px;
  background: rgba(0, 30, 60, 0.7);
  border-radius: 15px;
  border: 1px solid rgba(100, 150, 255, 0.3);
  width: 100%;
}

.core-metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 15px;
}

.core-metric-item {
  background: rgba(16, 32, 64, 0.8);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid rgba(100, 150, 255, 0.25);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.core-metric-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 212, 142, 0.4);
  border-color: rgba(0, 212, 142, 0.4);
}

.core-metric-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #00d48e;
  margin-bottom: 8px;
}

.core-metric-value .arrow {
  font-size: 1.8rem;
  margin-left: 5px;
}

.core-metric-label {
  font-size: 1.05rem;
  color: #a0c8ff;
  margin-bottom: 10px;
}

.precision-metric-value {
  font-size: 2.0rem;
  font-weight: 700;
  color: #00d48e;
  margin-bottom: 8px;
}

.core-metric-stars {
  margin-top: 10px;
}

/* 第二梯队：图像质量指标 */
.quality-metrics-panel {
  margin-top: 15px;
  margin-bottom: 15px;
  padding: 15px;
  background: rgba(0, 25, 50, 0.7);
  border-radius: 15px;
  border: 1px solid rgba(100, 150, 255, 0.2);
  width: 100%;
}

.quality-metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-top: 12px;
}

.quality-metric-item {
  background: rgba(16, 32, 64, 0.8);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  border: 1px solid rgba(100, 150, 255, 0.25);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.quality-metric-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: #00f2fe;
  margin-bottom: 6px;
}

.quality-metric-label {
  font-size: 1rem;
  color: #a0c8ff;
  margin-bottom: 8px;
}

.quality-metric-quality {
  font-size: 0.9rem;
  color: #4facfe;
  margin-bottom: 8px;
  font-weight: 600;
}

.quality-metric-stars {
  margin-top: 8px;
}

/* 第三梯队：技术指标 */
.tech-metrics-panel {
  margin-top: 15px;
  margin-bottom: 15px;
  padding: 12px;
  background: rgba(0, 20, 40, 0.7);
  border-radius: 15px;
  border: 1px solid rgba(100, 150, 255, 0.15);
  width: 100%;
}

.tech-metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 10px;
}

.tech-metric-item {
  background: rgba(16, 32, 64, 0.8);
  border-radius: 10px;
  padding: 12px;
  text-align: center;
  border: 1px solid rgba(100, 150, 255, 0.2);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
}

.tech-metric-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #a0c8ff;
  margin-bottom: 4px;
}

.tech-metric-label {
  font-size: 0.85rem;
  color: #7090cc;
  margin-bottom: 6px;
}

.tech-metric-stars {
  margin-top: 6px;
}

/* 星级评分样式 */
.star {
  font-size: 1rem;
  color: #f0c420;
  margin: 0 2px;
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .core-metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .quality-metrics-grid,
  .tech-metrics-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .core-metric-value {
    font-size: 2.0rem;
  }
  
  .precision-metric-value {
    font-size: 1.6rem;
  }
  
  .quality-metric-value {
    font-size: 1.4rem;
  }
  
  .tech-metric-value {
    font-size: 1.0rem;
  }
}
.result-placeholder { color: #7090cc; font-size: 1rem; padding: 40px 10px; display: grid; place-items: center; gap: 10px; }
.result-placeholder i { font-size: 2.4rem; }
.result-image { max-width: 100%; max-height: 480px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); display: block; margin: 0 auto; }

.download-btn { background: linear-gradient(90deg, #d4a017 0%, #f0c420 100%); color: #fff; box-shadow: 0 5px 15px rgba(212, 160, 23, 0.4); margin-top: 14px; }
.download-btn:hover:not(:disabled) { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(212, 160, 23, 0.6); }

.metrics-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.metric {
  background: rgba(16, 32, 64, 0.8);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  border: 1px solid rgba(100, 150, 255, 0.25);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.metric-value { font-size: 1.6rem; font-weight: 800; color: #00f2fe; text-shadow: 0 2px 10px rgba(0, 242, 254, 0.25); }
.metric-label { font-size: 0.9rem; color: #a0c8ff; margin-top: 4px; }

.hidden { display: none; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 输入图像横向排列样式 */
.input-images-container {
  display: flex;
  gap: 16px;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  max-width: 100%;
}

.input-image-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
  max-width: 48%;
}

.input-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  display: block;
  object-fit: contain;
}

.input-image-label {
  color: #a0c8ff;
  font-size: 0.9rem;
  font-weight: 500;
}

@media (max-width: 720px) {
  .control-panel { flex-direction: column; align-items: stretch; }
  .btn { width: 100%; justify-content: center; }
  .status-info { width: 100%; justify-content: center; }
  .input-images-container {
    flex-direction: column;
  }
  .input-image-wrapper {
    max-width: 100%;
  }
}
</style>

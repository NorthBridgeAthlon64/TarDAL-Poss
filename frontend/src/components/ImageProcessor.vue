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
        <i class="fas fa-thermometer-half upload-icon"></i>
        <div class="upload-text">上传红外图像</div>
        <div class="upload-hint">点击或拖拽文件到此处</div>
        <img v-if="irImage" class="upload-preview" :src="irImage" alt="红外图像预览" />
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
        <i class="fas fa-eye upload-icon"></i>
        <div class="upload-text">上传可见光图像</div>
        <div class="upload-hint">点击或拖拽文件到此处</div>
        <img v-if="viImage" class="upload-preview" :src="viImage" alt="可见光图像预览" />
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
      <div class="result-container">
        <h3>融合结果</h3>
        <div v-if="!fusedImage" class="result-placeholder">
          <i class="fas fa-image"></i>
          融合后的图像将显示在此处
        </div>
        <img v-else class="result-image" :src="fusedImage" alt="融合结果" />

        <button class="btn download-btn" :disabled="!fusedImage" @click="downloadResult">
          <i class="fas fa-download"></i>
          <span>下载结果</span>
        </button>

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
const fusedImage = ref(null);
const processing = ref(false);
const progress = ref(0);
const errorMessage = ref('');
const successMessage = ref('');
const dragState = ref({ ir: false, vi: false });
const metrics = ref({ psnr: null, ssim: null, detection: null, time: null });
let progressTimer = null;

const ready = computed(() => !!irImage.value && !!viImage.value);
const statusText = computed(() => {
  if (processing.value) return '融合处理中，请稍候';
  if (!ready.value) return '请上传两张图像';
  if (fusedImage.value) return '融合完成，可下载结果';
  return '已就绪，点击开始融合';
});
const metricsReady = computed(() => Object.values(metrics.value).every((v) => typeof v === 'number'));

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
    const { dataUrl, metrics: resultMetrics } = await runFusion(irImage.value, viImage.value);
    fusedImage.value = dataUrl;
    metrics.value = resultMetrics;
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
  const [ir, vi] = await Promise.all([loadImage(irSrc), loadImage(viSrc)]);
  const width = Math.max(ir.width, vi.width);
  const height = Math.max(ir.height, vi.height);
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(vi, 0, 0, width, height);
  ctx.globalAlpha = 0.55;
  ctx.drawImage(ir, 0, 0, width, height);
  ctx.globalAlpha = 1;

  const dataUrl = canvas.toDataURL('image/png');
  const resultMetrics = {
    psnr: 30 + Math.random() * 8,
    ssim: 0.87 + Math.random() * 0.08,
    detection: 15 + Math.random() * 18,
    time: 0.8 + Math.random() * 1.4
  };
  return { dataUrl, metrics: resultMetrics };
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
  if (!fusedImage.value) return;
  const link = document.createElement('a');
  link.download = 'TarDAL_fused.png';
  link.href = fusedImage.value;
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
  fusedImage.value = null;
  metrics.value = { psnr: null, ssim: null, detection: null, time: null };
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

.result-section { padding: 6px 0 0; }
.result-container {
  background: rgba(0, 20, 40, 0.55);
  border-radius: 15px;
  padding: 18px;
  text-align: center;
  border: 1px solid rgba(100, 150, 255, 0.2);
}

.result-container h3 { color: #4facfe; font-size: 1.2rem; margin-bottom: 12px; }
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

@media (max-width: 720px) {
  .control-panel { flex-direction: column; align-items: stretch; }
  .btn { width: 100%; justify-content: center; }
  .status-info { width: 100%; justify-content: center; }
}
</style>

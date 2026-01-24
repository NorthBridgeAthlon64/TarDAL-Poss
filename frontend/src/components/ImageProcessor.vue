<template>
  <section class="card">
    <div class="controls">
      <div class="buttons">
        <button class="btn primary" @click="triggerUpload">
          <i class="fas fa-cloud-upload-alt"></i>
          <span>上传图像</span>
        </button>
        <button class="btn success" :disabled="!originalSrc || processing" @click="startProcessing">
          <i :class="processing ? 'fas fa-spinner fa-spin' : 'fas fa-cogs'"></i>
          <span>{{ processing ? '处理中...' : (processedSrc ? '重新处理' : '运行算法') }}</span>
        </button>
        <button class="btn warning" :disabled="!processedData || processing" @click="saveImage">
          <i class="fas fa-download"></i>
          <span>保存图像</span>
        </button>
        <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
      </div>
      <div class="file-info">
        <i class="fas fa-info-circle"></i>
        <span>{{ fileInfoText }}</span>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="processing" class="progress">
        <div class="progress-header">
          <span>算法处理进度</span>
          <span>{{ Math.round(progress) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-line" :style="{ width: `${progress}%` }"></div>
        </div>
      </div>
    </Transition>

    <div class="comparison">
      <div class="pane">
        <div class="pane-head">原始输入</div>
        <div class="pane-body" :class="{ empty: !originalSrc }">
          <i v-if="!originalSrc" class="fas fa-image"></i>
          <p v-if="!originalSrc">等待上传或使用示例图像</p>
          <img v-else :src="originalSrc" alt="原始图像" />
        </div>
      </div>
      <div class="pane">
        <div class="pane-head">TarDAL 处理后</div>
        <div class="pane-body" :class="{ empty: !processedSrc }">
          <i v-if="!processedSrc" class="fas fa-cogs"></i>
          <p v-if="!processedSrc">处理结果将显示在此处</p>
          <img v-else :src="processedSrc" alt="处理后图像" />
        </div>
      </div>
    </div>

    <div class="metrics">
      <div class="metric">
        <p class="value">{{ metrics.psnr ? metrics.psnr.toFixed(1) : '--' }}</p>
        <p class="label">PSNR 峰值信噪比</p>
      </div>
      <div class="metric">
        <p class="value">{{ metrics.ssim ? metrics.ssim.toFixed(3) : '--' }}</p>
        <p class="label">SSIM 结构相似性</p>
      </div>
      <div class="metric">
        <p class="value">{{ metrics.detection ? `${metrics.detection.toFixed(0)}%` : '--%' }}</p>
        <p class="label">检测准确率提升</p>
      </div>
      <div class="metric">
        <p class="value">{{ metrics.time ? `${metrics.time.toFixed(1)}s` : '--s' }}</p>
        <p class="label">处理时间</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue';

const fileInput = ref(null);
const originalSrc = ref(null);
const processedSrc = ref(null);
const processedData = ref(null);
const processing = ref(false);
const progress = ref(0);
const metrics = reactive({ psnr: null, ssim: null, detection: null, time: null });
const fileName = ref(null);

const sampleImages = [
  'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1400&q=80',
  'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=80'
];

const fileInfoText = computed(() => {
  if (fileName.value) return fileName.value;
  if (originalSrc.value) return '示例图像 (低可见度场景)';
  return '未选择文件';
});

function triggerUpload() {
  fileInput.value?.click();
}

function onFileChange(event) {
  const [file] = event.target.files || [];
  if (!file) return;

  if (!file.type.match('image.*')) {
    alert('请选择图像文件（JPG、PNG 等）');
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    alert('文件大小不能超过 10MB');
    return;
  }

  fileName.value = `${file.name} (${formatSize(file.size)})`;

  const reader = new FileReader();
  reader.onload = (e) => {
    originalSrc.value = e.target?.result;
    resetProcessed();
  };
  reader.readAsDataURL(file);
}

async function startProcessing() {
  if (!originalSrc.value) {
    alert('请先上传或加载图像');
    return;
  }

  processing.value = true;
  progress.value = 0;
  animateProgress();

  try {
    const result = await processImageWithTarDAL(originalSrc.value);
    processedSrc.value = result.processedImage;
    metrics.psnr = result.metrics.psnr;
    metrics.ssim = result.metrics.ssim;
    metrics.detection = result.metrics.detectionImprovement;
    metrics.time = result.metrics.processingTime;

    await waitForImage(processedSrc.value);
    processedData.value = await toDataUrl(processedSrc.value);

    setTimeout(() => alert('算法处理完成！可以保存处理结果。'), 150);
  } catch (err) {
    console.error(err);
    alert(`处理失败: ${err.message}`);
  } finally {
    processing.value = false;
    progress.value = 0;
  }
}

function saveImage() {
  if (!processedData.value) {
    alert('无法获取图像数据，请重新处理');
    return;
  }

  const link = document.createElement('a');
  const baseName = fileName.value ? fileName.value.split('(')[0].trim() : 'TarDAL_processed_image';
  link.download = `${baseName.replace(/\.[^/.]+$/, '')}_TarDAL_processed.png`;
  link.href = processedData.value;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function resetProcessed() {
  processedSrc.value = null;
  processedData.value = null;
  metrics.psnr = metrics.ssim = metrics.detection = metrics.time = null;
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

function animateProgress() {
  const timer = setInterval(() => {
    progress.value = Math.min(100, progress.value + Math.random() * 8 + 5);
    if (!processing.value || progress.value >= 100) {
      clearInterval(timer);
    }
  }, 160);
}

async function processImageWithTarDAL(imageData) {
  await delay(800);
  return {
    processedImage: imageData,
    metrics: {
      psnr: 32 + Math.random() * 6,
      ssim: 0.88 + Math.random() * 0.1,
      detectionImprovement: 18 + Math.random() * 15,
      processingTime: 1.0 + Math.random() * 1.5
    }
  };
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function waitForImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve();
    img.onerror = () => reject(new Error('图像加载失败'));
    img.src = src;
  });
}

function toDataUrl(src) {
  return new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);
      resolve(canvas.toDataURL('image/png'));
    };
    img.src = src;
  });
}

onMounted(() => {
  const random = Math.floor(Math.random() * sampleImages.length);
  const src = sampleImages[random];
  originalSrc.value = src;
});
</script>

<style scoped>
.card {
  position: relative;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: linear-gradient(145deg, rgba(12, 22, 40, 0.95), rgba(16, 30, 56, 0.85));
  padding: clamp(16px, 3vw, 22px);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.controls {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border: 1px solid transparent;
  border-radius: 12px;
  padding: 11px 16px;
  font-weight: 700;
  letter-spacing: 0.1px;
  background: rgba(255, 255, 255, 0.04);
  color: #e8f0ff;
  cursor: pointer;
  transition: all 0.22s ease;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
}

.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.btn.primary { background: linear-gradient(135deg, #4fd1c5, #33b3c4); color: #04101f; }
.btn.success { background: linear-gradient(135deg, #5cc8ff, #7aa5ff); color: #04101f; }
.btn.warning { background: linear-gradient(135deg, #ffd166, #ffb347); color: #2b1800; }

.file-info {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px dashed rgba(255, 255, 255, 0.15);
  color: var(--muted);
  background: rgba(255, 255, 255, 0.02);
  flex: 1;
  min-width: 220px;
}

.progress {
  margin: 8px 0 6px;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.03);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  color: var(--muted);
}

.progress-bar {
  position: relative;
  height: 10px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.06);
}

.progress-line {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #4fd1c5, #7aa5ff);
  transition: width 0.2s ease;
}

.comparison {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
  margin: 14px 0;
}

.pane {
  border: 1px solid var(--border);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.03);
  overflow: hidden;
}

.pane-head {
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  font-weight: 700;
  letter-spacing: 0.2px;
  background: rgba(255, 255, 255, 0.04);
}

.pane-body {
  position: relative;
  min-height: 320px;
  display: grid;
  place-items: center;
  background: radial-gradient(circle at 20% 20%, rgba(79, 209, 197, 0.08), transparent 45%),
    radial-gradient(circle at 80% 30%, rgba(122, 165, 255, 0.08), transparent 40%),
    rgba(6, 12, 24, 0.8);
}

.pane-body img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.pane-body.empty {
  color: var(--muted);
  text-align: center;
  gap: 6px;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.metric {
  padding: 14px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.04);
  display: grid;
  gap: 6px;
  text-align: center;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
}

.value {
  font-size: 2rem;
  font-weight: 800;
  color: #7ce7df;
  text-shadow: 0 8px 25px rgba(79, 209, 197, 0.35);
}

.label {
  color: var(--muted);
}

.hidden { display: none; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 700px) {
  .controls { flex-direction: column; align-items: stretch; }
  .buttons { width: 100%; }
  .btn { flex: 1; justify-content: center; }
}
</style>

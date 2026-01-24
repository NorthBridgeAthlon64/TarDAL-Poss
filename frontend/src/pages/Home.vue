<template>
  <section class="page">
    <div class="hero">
      <div class="hero-copy">
        <p class="eyebrow">TarDAL 项目主页</p>
        <h1>双对抗学习驱动的多模态图像融合框架</h1>
        <p class="lede">
          面向低可见度与复杂场景，TarDAL 通过特征约束与对抗一致性，融合可见光、红外及深度信息，输出高信噪比、结构一致的画面。下方快速了解架构、指标与应用版块。
        </p>
        <div class="badges">
          <span class="badge"><i class="fas fa-layer-group"></i> 多模态融合</span>
          <span class="badge"><i class="fas fa-shield-alt"></i> 对抗一致性</span>
          <span class="badge"><i class="fas fa-gauge-high"></i> 低时延推理</span>
        </div>
      </div>
      <div class="hero-visual">
        <div class="orb"></div>
        <div class="orb small"></div>
        <div class="lines"></div>
      </div>
    </div>

    <div class="stat-grid">
      <div class="stat">
        <p class="stat-value">+4.8 dB</p>
        <p class="stat-label">平均 PSNR 提升（低光基线）</p>
      </div>
      <div class="stat">
        <p class="stat-value">+0.06</p>
        <p class="stat-label">SSIM 增益，纹理保持</p>
      </div>
      <div class="stat">
        <p class="stat-value">18–30%</p>
        <p class="stat-label">检测/识别准确率提升范围</p>
      </div>
      <div class="stat">
        <p class="stat-value">~1.3 s</p>
        <p class="stat-label">单张推理延迟（示例模型）</p>
      </div>
    </div>

    <div class="panel-grid">
      <article class="panel">
        <h3><i class="fas fa-diagram-project"></i> 核心架构</h3>
        <p>双对抗约束（重建/融合）+ 多尺度特征金字塔，结合感知/风格损失，强化纹理与亮度一致性。</p>
        <ul>
          <li>可插拔的编码器/解码器</li>
          <li>跨模态特征对齐与注意力融合</li>
          <li>支持离线批处理与流式推理</li>
        </ul>
      </article>
      <article class="panel">
        <h3><i class="fas fa-gears"></i> 部署形态</h3>
        <p>支持前后端解耦：前端做交互/预览，后端（Python/ONNX/TensorRT）完成推理，可扩展到边缘盒子。</p>
        <ul>
          <li>REST/WebSocket 推理接口</li>
          <li>ONNX/TensorRT/NCNN 可选</li>
          <li>CI/CD 一键构建与容器化</li>
        </ul>
      </article>
      <article class="panel">
        <h3><i class="fas fa-route"></i> 应用蓝图</h3>
        <p>针对个人、商业、国家/军事三个版块定制体验：不同页面直接内嵌演示，无需跳转主页。</p>
        <ul>
          <li>个人：影像增强 / 户外穿戴 / 家庭安防</li>
          <li>商业：工业质检 / 智慧安防 / 零售</li>
          <li>国家：边海防 / 应急救援 / 无人系统</li>
        </ul>
      </article>
    </div>

    <div class="cta">
      <div>
        <p class="eyebrow">快速导航</p>
        <h3>选择你的场景，直接在对应页面完成演示与验证。</h3>
      </div>
      <div class="cta-actions">
        <RouterLink to="/personal" class="btn primary"><i class="fas fa-user"></i><span>个人</span></RouterLink>
        <RouterLink to="/commercial" class="btn primary"><i class="fas fa-building"></i><span>商业</span></RouterLink>
        <RouterLink to="/national" class="btn primary"><i class="fas fa-shield-alt"></i><span>国家/军事</span></RouterLink>
      </div>
    </div>

    <div class="capabilities">
      <div class="cap-head">
        <p class="eyebrow">能力矩阵</p>
        <h2>从影像增强到任务级检测，TarDAL 的核心价值</h2>
        <p class="lede">融合提升不仅提升视觉观感，也为下游检测、分割、跟踪提供更稳定的输入，降低误报、提升召回。</p>
      </div>
      <div class="cap-grid">
        <article class="cap-card">
          <div class="cap-icon"><i class="fas fa-eye"></i></div>
          <h3>可视性提升</h3>
          <p>消除雾霾与逆光，增强暗部对比度，保持肤色与材质质感。</p>
        </article>
        <article class="cap-card">
          <div class="cap-icon"><i class="fas fa-wave-square"></i></div>
          <h3>稳健特征</h3>
          <p>跨模态对齐减少伪影，保护边缘结构，为分割/检测提供更干净的特征图。</p>
        </article>
        <article class="cap-card">
          <div class="cap-icon"><i class="fas fa-microchip"></i></div>
          <h3>多端部署</h3>
          <p>支持浏览器预览、云端推理、边缘盒子与移动端轻量模型，满足带宽/算力限制。</p>
        </article>
        <article class="cap-card">
          <div class="cap-icon"><i class="fas fa-lock"></i></div>
          <h3>安全与隐私</h3>
          <p>可选本地离线推理与水印，减少数据出域；支持权限控制与日志审计。</p>
        </article>
      </div>
    </div>

    <div class="flow">
      <p class="eyebrow">推理链路</p>
      <h2>从输入到融合输出的 5 步流程</h2>
      <div class="flow-grid">
        <div class="flow-step">
          <span class="step-index">01</span>
          <p class="step-title">采集 / 上传</p>
          <p class="step-body">接入可见光、红外或多谱段帧；支持本地文件与流式 RTSP。</p>
        </div>
        <div class="flow-step">
          <span class="step-index">02</span>
          <p class="step-title">预处理</p>
          <p class="step-body">归一化、尺度对齐、模态同步，保障对齐精度。</p>
        </div>
        <div class="flow-step">
          <span class="step-index">03</span>
          <p class="step-title">特征编码</p>
          <p class="step-body">多尺度特征金字塔提取纹理、亮度与语义信息。</p>
        </div>
        <div class="flow-step">
          <span class="step-index">04</span>
          <p class="step-title">对抗融合</p>
          <p class="step-body">双对抗损失约束重建与融合分支，保持结构与细节一致。</p>
        </div>
        <div class="flow-step">
          <span class="step-index">05</span>
          <p class="step-title">输出 / 下游</p>
          <p class="step-body">生成高信噪比画面；可接入检测、分割、跟踪或存档。</p>
        </div>
      </div>
    </div>

    <div class="stack">
      <p class="eyebrow">技术栈与集成</p>
      <h2>前后端解耦，灵活插拔</h2>
      <div class="stack-badges">
        <span class="pill"><i class="fas fa-vial"></i> Vue + Vite 交互</span>
        <span class="pill"><i class="fas fa-brain"></i> PyTorch/ONNX/TensorRT 推理</span>
        <span class="pill"><i class="fas fa-network-wired"></i> REST / WebSocket / gRPC</span>
        <span class="pill"><i class="fas fa-box"></i> Docker / K8s / 边缘盒子</span>
        <span class="pill"><i class="fas fa-code-branch"></i> CI/CD 与模型版本管理</span>
      </div>
    </div>

    <div class="timeline">
      <p class="eyebrow">里程碑</p>
      <h2>迭代计划</h2>
      <div class="timeline-grid">
        <div class="tl-item">
          <span class="tl-dot"></span>
          <div>
            <p class="tl-title">Q1 · 公开演示</p>
            <p class="tl-body">提供前端预览、示例模型与指标看板。</p>
          </div>
        </div>
        <div class="tl-item">
          <span class="tl-dot"></span>
          <div>
            <p class="tl-title">Q2 · 轻量化与边缘版</p>
            <p class="tl-body">发布 ARM/NCNN 版本，加入自动量化与剪枝工具。</p>
          </div>
        </div>
        <div class="tl-item">
          <span class="tl-dot"></span>
          <div>
            <p class="tl-title">Q3 · 多任务协同</p>
            <p class="tl-body">融合同步输出检测/分割结果，降低多模型链路延迟。</p>
          </div>
        </div>
        <div class="tl-item">
          <span class="tl-dot"></span>
          <div>
            <p class="tl-title">Q4 · 自适应策略</p>
            <p class="tl-body">根据环境光/天气自动选择融合强度与推理精度档位。</p>
          </div>
        </div>
      </div>
    </div>

    <div class="faq">
      <p class="eyebrow">FAQ</p>
      <h2>常见问题</h2>
      <div class="faq-grid">
        <div class="faq-item">
          <h4>可以离线运行吗？</h4>
          <p>支持，将推理端部署为本地服务或边缘盒子，前端仅做可视化与调用。</p>
        </div>
        <div class="faq-item">
          <h4>如何接入现有检测模型？</h4>
          <p>在融合输出后接入检测/分割 API，或通过 gRPC/REST 将输出帧送入现有推理管线。</p>
        </div>
        <div class="faq-item">
          <h4>推理性能如何调优？</h4>
          <p>提供 ONNX/TensorRT/NCNN 选项，可按 GPU/CPU/ARM 选择量化与分辨率，平衡画质与延迟。</p>
        </div>
        <div class="faq-item">
          <h4>数据是否安全？</h4>
          <p>可选择不出网部署，支持访问控制、水印与日志审计；前端不持久化用户图像。</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.hero {
  position: relative;
  overflow: hidden;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: linear-gradient(135deg, rgba(20, 32, 64, 0.9), rgba(16, 30, 56, 0.8));
  padding: clamp(18px, 4vw, 28px);
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 18px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
}

.hero-copy h1 {
  font-size: clamp(26px, 4vw, 34px);
  line-height: 1.25;
  margin-bottom: 10px;
}

.hero-copy .lede {
  color: var(--muted);
  max-width: 720px;
  line-height: 1.6;
}

.eyebrow {
  color: var(--primary);
  letter-spacing: 0.8px;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  font-weight: 600;
  color: #f0f5ff;
}

.hero-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.orb {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(79, 209, 197, 0.55), rgba(12, 24, 46, 0.05));
  filter: blur(2px);
  animation: float 6s ease-in-out infinite;
}

.orb.small {
  position: absolute;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(122, 165, 255, 0.6), rgba(12, 24, 46, 0.05));
  animation-duration: 7s;
  animation-delay: 1s;
  right: 14%;
}

.lines {
  position: absolute;
  inset: 8% 14%;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.stat {
  padding: 14px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.03);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 800;
  color: #7ce7df;
}

.stat-label {
  color: var(--muted);
  margin-top: 4px;
}

.panel-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}

.panel {
  padding: 16px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.03);
  box-shadow: 0 12px 34px rgba(0, 0, 0, 0.26);
  display: grid;
  gap: 8px;
}

.panel h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.05rem;
}

.panel p {
  color: #dfe6ff;
  line-height: 1.5;
}

.panel ul {
  list-style: none;
  padding: 0;
  color: var(--muted);
  display: grid;
  gap: 6px;
}

.panel ul li::before {
  content: '• ';
  color: var(--primary);
}

.cta {
  margin-top: 4px;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: linear-gradient(120deg, rgba(79, 209, 197, 0.15), rgba(122, 165, 255, 0.12));
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.cta-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 12px;
  border: none;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
}

.btn.primary {
  background: linear-gradient(135deg, #4fd1c5, #7aa5ff);
  color: #04101f;
}

.capabilities {
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.28);
  display: grid;
  gap: 12px;
}

.cap-head h2 {
  margin: 6px 0;
  font-size: clamp(22px, 3.4vw, 30px);
}

.cap-head .lede {
  color: var(--muted);
  max-width: 860px;
}

.cap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
}

.cap-card {
  padding: 14px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.02);
  display: grid;
  gap: 6px;
}

.cap-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, rgba(79, 209, 197, 0.15), rgba(122, 165, 255, 0.14));
  color: #7ce7df;
}

.cap-card p {
  color: #dfe6ff;
}

.flow {
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  display: grid;
  gap: 10px;
}

.flow-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
}

.flow-step {
  padding: 12px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.02);
}

.step-index {
  font-weight: 800;
  color: #7ce7df;
  letter-spacing: 0.5px;
}

.step-title {
  font-weight: 700;
  margin: 4px 0;
}

.step-body {
  color: var(--muted);
}

.stack {
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  display: grid;
  gap: 10px;
}

.stack-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pill {
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.03);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #dfe8ff;
}

.timeline {
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  display: grid;
  gap: 10px;
}

.timeline-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
}

.tl-item {
  position: relative;
  padding: 12px 12px 12px 18px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.02);
}

.tl-dot {
  position: absolute;
  left: 10px;
  top: 16px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #7ce7df;
}

.tl-title { font-weight: 700; }
.tl-body { color: var(--muted); }

.faq {
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  display: grid;
  gap: 10px;
}

.faq-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 10px;
}

.faq-item {
  padding: 12px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.02);
}

.faq-item h4 { margin-bottom: 6px; }
.faq-item p { color: var(--muted); line-height: 1.5; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@media (max-width: 960px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: 180px;
  }
}
</style>

<template>
  <section class="page">
    <header class="section-head">
      <p class="eyebrow">应用蓝图 · 商业</p>
      <h1>为工业质检、安防监控与智慧零售提供清晰可见的多模态画面</h1>
      <p class="lede">TarDAL 通过双对抗学习提升成像质量，适配边缘设备与云端部署，助力企业在低光与强干扰环境中保持稳定识别率。</p>
    </header>

    <div class="grid">
      <article class="card">
        <h3><i class="fas fa-industry"></i> 工业质检</h3>
        <p>在烟雾、油污或反光环境下提升缺陷检测的鲁棒性，减少漏检与误报。</p>
        <ul>
          <li>可见光+红外/深度数据融合</li>
          <li>边缘推理，毫秒级延迟</li>
          <li>与现有 SCADA/MES 接口对接</li>
        </ul>
      </article>
      <article class="card">
        <h3><i class="fas fa-video"></i> 智慧安防</h3>
        <p>夜间、逆光、雨雪等复杂场景下保持清晰画面，提升行为分析与人车识别精度。</p>
        <ul>
          <li>与 VMS/NVR 兼容的 REST/RTSP 旁路</li>
          <li>可选隐私遮罩与水印</li>
          <li>GPU/CPU 灵活切换</li>
        </ul>
      </article>
      <article class="card">
        <h3><i class="fas fa-store"></i> 智慧零售</h3>
        <p>商场、仓储弱光环境下提升货架识别、客流分析的信噪比，降低灯光成本。</p>
        <ul>
          <li>与现有 BI/数据看板对接</li>
          <li>批量处理历史录像</li>
          <li>可集成到自助收银或盘点终端</li>
        </ul>
      </article>
    </div>

    <div class="cta">
      <div>
        <p class="eyebrow">PoC / 集成</p>
        <h3>直接在本页验证效果，或咨询 SDK/API 部署方案。</h3>
      </div>
      <div class="actions">
        <button class="btn primary" type="button" @click="scrollToDemo"><i class="fas fa-play"></i><span>下滑演示</span></button>
        <a class="btn ghost" href="mailto:team@tardal.local">预约技术交流</a>
      </div>
    </div>

    <div ref="demoRef" class="demo-block">
      <h2 class="demo-title">商业场景即时演示</h2>
      <ImageProcessor />
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import ImageProcessor from '../components/ImageProcessor.vue';

const demoRef = ref(null);
const scrollToDemo = () => demoRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' });
</script>

<style scoped>
.page { display: grid; gap: 18px; }
.section-head h1 { font-size: clamp(24px, 3.6vw, 32px); margin: 6px 0; }
.section-head .lede { color: var(--muted); max-width: 820px; }
.eyebrow { color: var(--primary); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.card { padding: 16px; border-radius: 14px; border: 1px solid var(--border); background: rgba(255,255,255,0.03); box-shadow: 0 12px 30px rgba(0,0,0,0.24); display: grid; gap: 10px; }
.card h3 { display: flex; align-items: center; gap: 8px; font-size: 1.05rem; }
.card p { color: var(--text-secondary); }
.card ul { list-style: none; display: grid; gap: 6px; color: var(--muted); padding: 0; }
.card ul li::before { content: '• '; color: var(--primary); }
.cta { margin-top: 6px; padding: 14px 16px; border-radius: 12px; border: 1px solid var(--border); background: linear-gradient(120deg, rgba(79,209,197,0.15), rgba(122,165,255,0.12)); display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.actions { display: flex; gap: 10px; flex-wrap: wrap; }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 12px; border: none; font-weight: 700; cursor: pointer; text-decoration: none; }
.btn.primary { background: linear-gradient(135deg, #4fd1c5, #7aa5ff); color: #04101f; }
.btn.ghost { border: 1px solid var(--border-strong); background: transparent; color: var(--text-main); }
.demo-block { margin-top: 4px; display: grid; gap: 12px; }
.demo-title { font-size: 1.1rem; font-weight: 800; letter-spacing: 0.3px; }

@media (max-width: 720px) {
  .cta { flex-direction: column; align-items: flex-start; }
  .actions { width: 100%; }
  .actions .btn { flex: 1; justify-content: center; }
}
</style>

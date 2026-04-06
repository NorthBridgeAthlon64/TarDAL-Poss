<template>
  <section class="page">
    <header class="section-head">
      <p class="eyebrow">应用蓝图 · 个人</p>
      <h1>雾霾、夜景、室内弱光的视觉提升助手</h1>
      <p class="lede">为摄影爱好者、户外运动者和安防玩家提供即开即用的图像融合体验，快速改善低可见度画面质量。</p>
    </header>

    <div class="grid">
      <article class="card">
        <h3><i class="fas fa-camera-retro"></i> 影像增强</h3>
        <p>一键优化手机/相机照片，提升细节与对比度，保留肤色与自然色调。</p>
        <ul>
          <li>夜景拍摄降噪，保留暗部纹理</li>
          <li>雾气/逆光场景自动均衡</li>
          <li>批量处理旅拍素材</li>
        </ul>
      </article>
      <article class="card">
        <h3><i class="fas fa-hiking"></i> 户外穿戴</h3>
        <p>结合运动相机或头戴设备，实时提升骑行、徒步的低光画面，安全导航更清晰。</p>
        <ul>
          <li>行车记录仪低光增强</li>
          <li>红外/可见光融合用于夜跑</li>
          <li>离线模式，保护隐私</li>
        </ul>
      </article>
      <article class="card">
        <h3><i class="fas fa-shield-alt"></i> 家庭安防</h3>
        <p>家用摄像头通过 TarDAL 对暗角与雨夜画面进行融合，减少误报并保留细节。</p>
        <ul>
          <li>异常检测更稳定</li>
          <li>与 NAS/本地网关集成</li>
          <li>小型设备低功耗推理</li>
        </ul>
      </article>
    </div>

    <div class="cta">
      <div>
        <p class="eyebrow">快速上手</p>
        <h3>直接在本页上传你的样例，或将算法嵌入本地工具链。</h3>
      </div>
      <button class="btn primary" type="button" @click="scrollToDemo">
        <i class="fas fa-rocket"></i>
        <span>下滑立即演示</span>
      </button>
    </div>

    <div ref="demoRef" class="demo-block">
      <h2 class="demo-title">个人场景即时演示</h2>
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
.section-head .lede { color: var(--muted); max-width: 780px; }
.eyebrow { color: var(--primary); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.card { padding: 16px; border-radius: 14px; border: 1px solid var(--border); background: rgba(255,255,255,0.03); box-shadow: 0 12px 30px rgba(0,0,0,0.24); display: grid; gap: 10px; }
.card h3 { display: flex; align-items: center; gap: 8px; font-size: 1.05rem; }
.card p { color: var(--text-secondary); }
.card ul { list-style: none; display: grid; gap: 6px; color: var(--muted); padding: 0; }
.card ul li::before { content: '• '; color: var(--primary); }
.cta { margin-top: 6px; padding: 14px 16px; border-radius: 12px; border: 1px solid var(--border); background: linear-gradient(120deg, rgba(79,209,197,0.15), rgba(122,165,255,0.12)); display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 12px; border: none; font-weight: 700; cursor: pointer; text-decoration: none; }
.btn.primary { background: linear-gradient(135deg, #4fd1c5, #7aa5ff); color: #04101f; }
.demo-block { margin-top: 4px; display: grid; gap: 12px; }
.demo-title { font-size: 1.1rem; font-weight: 800; letter-spacing: 0.3px; }

@media (max-width: 720px) {
  .cta { flex-direction: column; align-items: flex-start; }
}
</style>

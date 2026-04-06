<template>
  <section class="page">
    <header class="section-head">
      <p class="eyebrow">应用蓝图 · 国家</p>
      <h1>全天候、全谱段的态势感知与任务保障</h1>
      <p class="lede">TarDAL 在极端天气、复杂电磁与低照条件下融合多源图像，面向边海防、应急救援和战术级侦察提供可靠的视觉能力。</p>
    </header>

    <div class="grid">
      <article class="card">
        <h3><i class="fas fa-radar"></i> 边海防巡察</h3>
        <p>融合红外/可见光/星光摄像数据，提升远距离微小目标探测与跟踪稳定性。</p>
        <ul>
          <li>雾霾、雨雪和夜间低光场景鲁棒</li>
          <li>可与雷达/ AIS 数据联动</li>
          <li>前哨站或舰载边缘部署</li>
        </ul>
      </article>
      <article class="card">
        <h3><i class="fas fa-helmet-safety"></i> 应急救援</h3>
        <p>火场、塌方、雪崩等极端环境中提升搜救可见度，辅助目标定位与路径规划。</p>
        <ul>
          <li>单兵端/无人机载融合</li>
          <li>低带宽传输的高效编解码</li>
          <li>可叠加热力、分割、深度信息</li>
        </ul>
      </article>
      <article class="card">
        <h3><i class="fas fa-drone"></i> 无人系统</h3>
        <p>面向无人机、无人车的昼夜侦察与导航，提升 SLAM/检测算法在遮挡和烟尘下的可靠度。</p>
        <ul>
          <li>轻量化模型，支持 ARM/GPU</li>
          <li>时序稳定，减少抖动伪影</li>
          <li>可与任务规划/指控系统对接</li>
        </ul>
      </article>
    </div>

    <div class="cta">
      <div>
        <p class="eyebrow">验证与适配</p>
        <h3>本页即可验证画质提升，或联系团队获取离线包与加固版部署方案。</h3>
      </div>
      <div class="actions">
        <button class="btn primary" type="button" @click="scrollToDemo"><i class="fas fa-play"></i><span>下滑演示</span></button>
        <a class="btn ghost" href="mailto:mission@tardal.local">需求沟通</a>
      </div>
    </div>

    <div ref="demoRef" class="demo-block">
      <h2 class="demo-title">国家场景即时演示</h2>
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
.section-head .lede { color: var(--muted); max-width: 860px; }
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

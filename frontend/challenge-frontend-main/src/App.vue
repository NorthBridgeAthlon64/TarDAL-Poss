<template>
  <div class="app-shell">
    <div class="bg-glow bg-glow-one"></div>
    <div class="bg-glow bg-glow-two"></div>
    <header class="topbar">
      <div class="brand">
        <span class="logo">TarDAL</span>
        <div class="brand-meta">
          <p class="title">多模态图像融合·双对抗学习</p>
          <small class="subtitle">项目概览 | 场景蓝图 | 在线演示</small>
        </div>
      </div>
      <nav class="nav">
        <RouterLink class="nav-item" to="/" exact-active-class="active">
          <i class="fas fa-home"></i>
          <span>主页</span>
        </RouterLink>
        <RouterLink class="nav-item" to="/personal" exact-active-class="active">
          <i class="fas fa-user"></i>
          <span>个人</span>
        </RouterLink>
        <RouterLink class="nav-item" to="/commercial" exact-active-class="active">
          <i class="fas fa-building"></i>
          <span>商业</span>
        </RouterLink>
        <RouterLink class="nav-item" to="/national" exact-active-class="active">
          <i class="fas fa-shield-alt"></i>
          <span>国家</span>
        </RouterLink>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.app-shell {
  position: relative;
  min-height: 100vh;
  padding: 32px clamp(16px, 4vw, 40px) 48px;
  overflow: hidden;
}

.bg-glow {
  position: absolute;
  filter: blur(90px);
  opacity: 0.6;
  pointer-events: none;
  z-index: 0;
}

.bg-glow-one {
  width: 420px;
  height: 420px;
  background: radial-gradient(circle, rgba(79, 209, 197, 0.55), transparent 65%);
  top: -80px;
  left: -40px;
}

.bg-glow-two {
  width: 520px;
  height: 520px;
  background: radial-gradient(circle, rgba(122, 165, 255, 0.5), transparent 60%);
  bottom: -140px;
  right: -80px;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 18px;
  margin-bottom: 20px;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(14, 25, 46, 0.9), rgba(12, 28, 56, 0.85));
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(10px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 54px;
  height: 54px;
  border-radius: 14px;
  background: linear-gradient(145deg, #4fd1c5, #7aa5ff);
  color: #0c152b;
  font-weight: 800;
  letter-spacing: 0.4px;
  box-shadow: 0 12px 30px rgba(79, 209, 197, 0.35);
}

.brand-meta .title {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.2px;
}

.brand-meta .subtitle {
  color: var(--muted);
}

.nav {
  display: flex;
  gap: 10px;
  align-items: center;
}

.nav-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid transparent;
  color: #dfe8ff;
  font-weight: 600;
  letter-spacing: 0.1px;
  transition: all 0.25s ease;
}

.nav-item:hover {
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
  transform: translateY(-1px);
}

.nav-item.active {
  border-color: rgba(79, 209, 197, 0.7);
  background: linear-gradient(135deg, rgba(79, 209, 197, 0.15), rgba(122, 165, 255, 0.12));
  color: #ffffff;
}

.content {
  position: relative;
  z-index: 1;
}

@media (max-width: 860px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .nav {
    width: 100%;
    flex-wrap: wrap;
  }

  .nav-item {
    flex: 1;
    justify-content: center;
  }
}
</style>

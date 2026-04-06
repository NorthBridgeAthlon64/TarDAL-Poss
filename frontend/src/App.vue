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
      <div class="actions">
        <button class="theme-toggle" type="button" @click="toggleTheme">
          <i :class="theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon'"></i>
          <span>{{ theme === 'dark' ? '浅色模式' : '深色模式' }}</span>
        </button>
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
      </div>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useTheme } from './composables/useTheme';

const { theme, toggleTheme } = useTheme();
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
  background: var(--surface-strong);
  box-shadow: 0 20px 50px var(--shadow-color);
  backdrop-filter: blur(10px);
}

.actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.theme-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border-radius: 12px;
  border: 1px solid var(--border-strong);
  padding: 10px 12px;
  background: var(--surface-soft);
  color: var(--text-main);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.theme-toggle:hover {
  border-color: var(--border-accent);
  transform: translateY(-1px);
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
  color: var(--text-main);
  font-weight: 600;
  letter-spacing: 0.1px;
  transition: all 0.25s ease;
}

.nav-item:hover {
  border-color: var(--border-strong);
  background: var(--surface-soft);
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

  .actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .theme-toggle {
    justify-content: center;
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

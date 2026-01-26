import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../pages/Home.vue';
import Personal from '../pages/Personal.vue';
import Commercial from '../pages/Commercial.vue';
import National from '../pages/National.vue';

const routes = [
  { path: '/', name: 'home', component: Home, meta: { title: 'TarDAL 图像融合演示' } },
  { path: '/personal', name: 'personal', component: Personal, meta: { title: '个人应用 | TarDAL' } },
  { path: '/commercial', name: 'commercial', component: Commercial, meta: { title: '商业应用 | TarDAL' } },
  { path: '/national', name: 'national', component: National, meta: { title: '国家/军事应用 | TarDAL' } }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

router.afterEach((to) => {
  if (to.meta.title) document.title = to.meta.title;
});

export default router;

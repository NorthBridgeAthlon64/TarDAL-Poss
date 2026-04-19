import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import '@fontsource/space-grotesk/400.css';
import '@fontsource/space-grotesk/500.css';
import '@fontsource/space-grotesk/600.css';
import '@fontsource/space-grotesk/700.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './assets/base.css';

const app = createApp(App);
app.use(router);
app.mount('#app');

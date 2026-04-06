import { onMounted, shallowRef } from 'vue';

const STORAGE_KEY = 'tardal-theme';
const theme = shallowRef('dark');

function applyTheme(value) {
  const nextTheme = value === 'light' ? 'light' : 'dark';
  theme.value = nextTheme;
  document.documentElement.setAttribute('data-theme', nextTheme);
  localStorage.setItem(STORAGE_KEY, nextTheme);
}

function resolvePreferredTheme() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === 'light' || stored === 'dark') {
    return stored;
  }

  const prefersLight = window.matchMedia?.('(prefers-color-scheme: light)').matches;
  return prefersLight ? 'light' : 'dark';
}

export function useTheme() {
  onMounted(() => {
    applyTheme(resolvePreferredTheme());
  });

  const toggleTheme = () => {
    applyTheme(theme.value === 'dark' ? 'light' : 'dark');
  };

  return {
    theme,
    toggleTheme,
    applyTheme
  };
}

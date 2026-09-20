(function () {
  'use strict';
  var key = 'worldcopy-site-theme';
  var root = document.documentElement;
  var preference = null;
  var system = window.matchMedia('(prefers-color-scheme: dark)');
  try { preference = localStorage.getItem(key); } catch (_) {}
  if (preference !== 'light' && preference !== 'dark') preference = null;
  function apply(theme) {
    root.dataset.theme = theme;
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = theme === 'dark' ? '#12201e' : '#f4f3ee';
    var button = document.querySelector('.theme-toggle');
    if (!button) return;
    var zh = root.lang.indexOf('zh') === 0;
    var dark = theme === 'dark';
    button.setAttribute('aria-pressed', String(dark));
    button.setAttribute('aria-label', zh ? '深色外观' : 'Dark appearance');
    button.title = zh ? (dark ? '切换为浅色外观' : '切换为深色外观') : (dark ? 'Switch to light appearance' : 'Switch to dark appearance');
    button.querySelector('.theme-icon').textContent = dark ? '☀' : '☾';
    button.querySelector('.theme-label').textContent = zh ? (dark ? '浅色' : '深色') : (dark ? 'Light' : 'Dark');
  }
  apply(preference || (system.matches ? 'dark' : 'light'));
  document.addEventListener('DOMContentLoaded', function () {
    apply(root.dataset.theme);
    var button = document.querySelector('.theme-toggle');
    if (button) {
      button.hidden = false;
      button.addEventListener('click', function () {
        preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem(key, preference); } catch (_) {}
        apply(preference);
      });
    }
  });
  system.addEventListener('change', function (event) {
    if (!preference) apply(event.matches ? 'dark' : 'light');
  });
  window.addEventListener('storage', function (event) {
    if (event.key !== key) return;
    preference = event.newValue === 'dark' || event.newValue === 'light' ? event.newValue : null;
    apply(preference || (system.matches ? 'dark' : 'light'));
  });
}());

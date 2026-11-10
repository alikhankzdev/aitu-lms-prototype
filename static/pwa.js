'use strict';
(() => {
  if ('serviceWorker' in navigator && window.isSecureContext) {
    window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js', {scope: '/'}).catch(() => {}));
  }
  let installPrompt = null;
  const button = document.getElementById('install-app');
  window.addEventListener('beforeinstallprompt', event => {
    if (!button) return;
    event.preventDefault();
    installPrompt = event;
    button.hidden = false;
  });
  if (button) button.addEventListener('click', async () => {
    if (!installPrompt) return;
    button.disabled = true;
    try {
      await installPrompt.prompt();
      await installPrompt.userChoice;
    } finally {
      installPrompt = null;
      button.hidden = true;
      button.disabled = false;
    }
  });
  window.addEventListener('appinstalled', () => {
    installPrompt = null;
    if (button) button.hidden = true;
  });
})();

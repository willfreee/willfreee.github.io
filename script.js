/* ==========================================================================
   willfreee — Theme Toggle & Preference Persistence
   ========================================================================== */

(function () {
  'use strict';

  const STORAGE_KEY = 'willfreee-theme';
  const themeToggleBtn = document.getElementById('theme-toggle');
  const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector('.theme-icon') : null;

  /**
   * Safely read stored theme preference from localStorage.
   */
  function getSavedTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null; // Handle privacy modes or blocked storage gracefully
    }
  }

  /**
   * Safely save theme preference to localStorage.
   */
  function saveTheme(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      // Ignore write errors if storage is restricted
    }
  }

  /**
   * Determine starting theme:
   * 1. Saved localStorage value (if any)
   * 2. System / OS prefers-color-scheme
   * 3. Default to 'light'
   */
  function getPreferredTheme() {
    const savedTheme = getSavedTheme();
    if (savedTheme === 'light' || savedTheme === 'dark') {
      return savedTheme;
    }
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  const SUN_SVG = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
  const MOON_SVG = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);

    if (themeIcon) {
      themeIcon.innerHTML = theme === 'dark' ? SUN_SVG : MOON_SVG;
    }

    if (themeToggleBtn) {
      themeToggleBtn.setAttribute(
        'aria-label',
        theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'
      );
    }
  }

  // 1. Initialize theme on script load
  const initialTheme = getPreferredTheme();
  applyTheme(initialTheme);

  // 2. Set up click handler for toggle button
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function () {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

      applyTheme(newTheme);
      saveTheme(newTheme);
    });
  }

  // 3. React to OS preference changes if the user hasn't explicitly saved a choice
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      if (!getSavedTheme()) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
})();
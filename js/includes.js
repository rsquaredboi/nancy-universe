// Nancy Universe — HTML partial loader
// Fetches shared nav/footer/topbar/loader and injects into placeholder elements
// Auto-detects project root from its own <script src> for GitHub Pages compatibility
(function() {
  // Auto-detect base path from this script's own src attribute
  // e.g. "../../js/includes.js" → basePath = "../../"
  // e.g. "js/includes.js" → basePath = ""
  const currentScript = document.currentScript || document.querySelector('script[src*="includes.js"]');
  const scriptSrc = currentScript ? currentScript.getAttribute('src') : '';
  const basePath = scriptSrc.replace('js/includes.js', '');

  const partials = [
    { id: 'loader-placeholder', file: 'includes/loader.html' },
    { id: 'topbar-placeholder', file: 'includes/topbar.html' },
    { id: 'nav-placeholder', file: 'includes/nav.html' },
    { id: 'footer-placeholder', file: 'includes/footer.html' }
  ];

  partials.forEach(({ id, file }) => {
    const el = document.getElementById(id);
    if (!el) return;
    fetch(basePath + file)
      .then(r => r.text())
      .then(html => {
        // Rewrite root-relative paths (/pages/..., /nancy-logo-pink...)
        // to use the detected basePath so links work on GitHub Pages
        html = html.replace(/(href|src)="\//g, '$1="' + basePath);
        el.outerHTML = html;
        // After nav loads, set active link based on current path
        if (id === 'nav-placeholder') setActiveNav();
      })
      .catch(err => console.warn('Partial load failed:', file, err));
  });

  function setActiveNav() {
    const path = window.location.pathname;
    let matched = false;
    document.querySelectorAll('.nav-links a').forEach(link => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      // Match by checking if the path ends with the href's filename portion
      if (href && href !== '/' && !href.startsWith('#')) {
        const hrefPath = href.replace(/^(\.\.\/)+/, '').replace(/^\//, '');
        if (path.includes(hrefPath)) {
          link.classList.add('active');
          matched = true;
        }
      }
    });
    // Product pages → highlight "Shop All"
    if (!matched && path.includes('/products/')) {
      const shopAll = document.querySelector('.nav-links a[href*="shop-all"]');
      if (shopAll) shopAll.classList.add('active');
    }

    // Mobile hamburger toggle
    const hamburger = document.querySelector('.nav-hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (hamburger && navLinks) {
      hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('nav-open');
        hamburger.classList.toggle('is-open');
      });
    }
  }
})();

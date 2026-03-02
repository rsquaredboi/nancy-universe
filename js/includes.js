// Nancy Universe — HTML partial loader
// Fetches shared nav/footer/topbar/loader and injects into placeholder elements
// Auto-detects project root from its own <script src> for GitHub Pages compatibility
(function() {
  const currentScript = document.currentScript || document.querySelector('script[src*="includes.js"]');
  const scriptSrc = currentScript ? currentScript.getAttribute('src') : '';
  const basePath = scriptSrc.replace('js/includes.js', '');

  // Auto-load cart.js on every page
  if (!document.querySelector('script[src*="cart.js"]')) {
    const cartScript = document.createElement('script');
    cartScript.src = basePath + 'js/cart.js';
    cartScript.defer = true;
    document.head.appendChild(cartScript);
  }

  // Wrap topbar + nav placeholders in .site-header for sticky positioning
  const topbarEl = document.getElementById('topbar-placeholder');
  const navEl = document.getElementById('nav-placeholder');
  if (topbarEl && navEl && topbarEl.parentNode === navEl.parentNode) {
    const wrapper = document.createElement('div');
    wrapper.className = 'site-header';
    topbarEl.parentNode.insertBefore(wrapper, topbarEl);
    wrapper.appendChild(topbarEl);
    wrapper.appendChild(navEl);
  }

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
        html = html.replace(/(href|src)="\//g, '$1="' + basePath);
        el.outerHTML = html;
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
      if (href && href !== '/' && !href.startsWith('#')) {
        const hrefPath = href.replace(/^(\.\.\/)+/, '').replace(/^\//, '');
        if (path.includes(hrefPath)) {
          link.classList.add('active');
          matched = true;
        }
      }
    });
    if (!matched && path.includes('/products/')) {
      const shopAll = document.querySelector('.nav-links a[href*="shop-all"]');
      if (shopAll) shopAll.classList.add('active');
    }
    // Mobile nav is handled by main.js initMobileNav()
  }
})();

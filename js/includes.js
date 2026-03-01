// Nancy Universe — HTML partial loader
// Fetches shared nav/footer/topbar/loader and injects into placeholder elements
(function() {
  const basePath = window.NANCY_BASE || '';

  const partials = [
    { id: 'loader-placeholder', file: 'includes/loader.html' },
    { id: 'topbar-placeholder', file: 'includes/topbar.html' },
    { id: 'nav-placeholder', file: 'includes/nav.html' },
    { id: 'footer-placeholder', file: 'includes/footer.html' }
  ];

  partials.forEach(({ id, file }) => {
    const el = document.getElementById(id);
    if (!el) return;
    fetch(basePath + '/' + file)
      .then(r => r.text())
      .then(html => {
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
      if (href && href !== '/' && path.includes(href)) {
        link.classList.add('active');
        matched = true;
      }
    });
    // Product pages → highlight "Shop All"
    if (!matched && path.includes('/pages/products/')) {
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

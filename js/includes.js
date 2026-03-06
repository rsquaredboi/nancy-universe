// Nancy Universe — HTML partial loader
// Fetches shared nav/footer/topbar/loader and injects into placeholder elements
// Auto-detects project root from its own <script src> for GitHub Pages compatibility
(function() {
  // Meta Pixel 911407491817897 — injected globally
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
  document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '911407491817897');
  fbq('track', 'PageView');
  // Also inject noscript fallback
  (function(){var i=document.createElement('img');i.height=1;i.width=1;i.style.display='none';
  i.src='https://www.facebook.com/tr?id=911407491817897&ev=PageView&noscript=1';
  document.body.appendChild(i);})();

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

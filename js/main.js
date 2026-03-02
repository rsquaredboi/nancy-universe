// ═══════════════════════════════════════════════
// Nancy Universe — Main JS
// ═══════════════════════════════════════════════

// Intersection Observer for scroll animations
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: '0px 0px -60px 0px'
});

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// Number counter animation
function animateCounter(el, target) {
  const duration = 2000;
  const start = performance.now();

  function format(n) {
    if (target >= 1000000) return Math.floor(n / 1000000).toLocaleString() + 'M+';
    if (target >= 10000) return Math.floor(n / 1000).toLocaleString() + 'K+';
    if (target >= 1000) return n.toLocaleString() + '+';
    return n + '+';
  }

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);
    el.textContent = format(current);
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

// Counter Observer — trigger counters once the community section scrolls in
const counterSection = document.querySelector('.community');
let countersStarted = false;
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !countersStarted) {
      countersStarted = true;
      setTimeout(() => {
        document.querySelectorAll('[data-count]').forEach(el => {
          const count = parseInt(el.dataset.count);
          if (count) animateCounter(el, count);
        });
      }, 400);
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

if (counterSection) counterObserver.observe(counterSection);

// Countdown Timer
function updateCountdown() {
  const now = new Date();
  const target = new Date('2026-04-15T00:00:00Z');
  const diff = target - now;

  const el = (id) => document.getElementById(id);
  if (!el('cd-days')) return;

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const secs = Math.floor((diff % (1000 * 60)) / 1000);

  el('cd-days').textContent = String(days).padStart(2, '0');
  el('cd-hours').textContent = String(hours).padStart(2, '0');
  el('cd-mins').textContent = String(mins).padStart(2, '0');
  el('cd-secs').textContent = String(secs).padStart(2, '0');
}

updateCountdown();
setInterval(updateCountdown, 1000);

// Subtle parallax on hero (no fade)
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      const scrolled = window.scrollY;
      const hero = document.querySelector('.hero-content');
      if (hero && scrolled < window.innerHeight) {
        hero.style.transform = `translateY(${scrolled * 0.08}px)`;
      }
      ticking = false;
    });
    ticking = true;
  }
});

// Nav scroll behavior — shadow on scroll
let lastScroll = 0;
window.addEventListener('scroll', () => {
  const navEl = document.querySelector('nav');
  if (!navEl) return;
  const currentScroll = window.scrollY;
  if (currentScroll > 100) {
    navEl.style.boxShadow = '0 2px 20px rgba(0,0,0,0.06)';
  } else {
    navEl.style.boxShadow = 'none';
  }
  lastScroll = currentScroll;
});


// ═══════════════════════════════════════════════
// MOBILE NAV — Drawer + Accordion + Body Lock
// ═══════════════════════════════════════════════
(function initMobileNav() {
  // Wait for includes.js to inject the nav (or run immediately if nav exists)
  function setup() {
    const hamburger = document.querySelector('.nav-hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (!hamburger || !navLinks) return false;

    // Create scrim overlay at body level (not inside sticky header)
    let scrim = document.getElementById('nav-scrim');
    if (!scrim) {
      scrim = document.createElement('div');
      scrim.className = 'nav-scrim';
      scrim.id = 'nav-scrim';
      document.body.appendChild(scrim);
    }

    let isOpen = false;

    function openNav() {
      isOpen = true;
      navLinks.style.display = 'flex';
      // Force reflow so transition fires
      navLinks.offsetHeight;
      navLinks.classList.add('nav-open');
      hamburger.classList.add('is-open');
      if (scrim) scrim.classList.add('visible');
      document.body.classList.add('nav-locked');
    }

    function closeNav() {
      isOpen = false;
      navLinks.classList.remove('nav-open');
      hamburger.classList.remove('is-open');
      if (scrim) scrim.classList.remove('visible');
      document.body.classList.remove('nav-locked');
      // Close all accordion dropdowns
      document.querySelectorAll('.nav-dropdown.mobile-open').forEach(d => {
        d.classList.remove('mobile-open');
      });
      // Wait for transition then hide
      setTimeout(() => {
        if (!isOpen && window.innerWidth <= 768) {
          // Don't set display:none — the CSS transform handles hiding
        }
      }, 350);
    }

    // Hamburger toggle
    hamburger.addEventListener('click', (e) => {
      e.stopPropagation();
      if (isOpen) closeNav(); else openNav();
    });

    // Scrim click closes nav
    if (scrim) {
      scrim.addEventListener('click', closeNav);
    }

    // Escape key closes nav
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen) closeNav();
    });

    // Dropdown accordion toggle (mobile only) — bound to the chevron button
    document.querySelectorAll('.nav-dropdown-toggle').forEach(btn => {
      btn.addEventListener('click', (e) => {
        if (window.innerWidth > 768) return;
        e.preventDefault();
        e.stopPropagation();
        const dropdown = btn.closest('.nav-dropdown');
        const wasOpen = dropdown.classList.contains('mobile-open');
        // Close all others
        document.querySelectorAll('.nav-dropdown.mobile-open').forEach(d => {
          if (d !== dropdown) d.classList.remove('mobile-open');
        });
        dropdown.classList.toggle('mobile-open', !wasOpen);
      });
    });

    // Dropdown parent links (e.g. "Plushies") — navigate + close drawer
    document.querySelectorAll('.nav-dropdown > a').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) closeNav();
      });
    });

    // Sub-menu links — close drawer on navigate
    document.querySelectorAll('.nav-dropdown-menu a').forEach(link => {
      link.addEventListener('click', () => {
        if (window.innerWidth <= 768) closeNav();
      });
    });

    // Close nav on window resize to desktop
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768 && isOpen) closeNav();
    });

    return true;
  }

  // Try immediately, then retry after includes.js loads partials
  if (!setup()) {
    // MutationObserver to catch when nav is injected by includes.js
    const observer = new MutationObserver(() => {
      if (document.querySelector('.nav-hamburger')) {
        observer.disconnect();
        setup();
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
})();

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
      // Small delay so reveal animation has time to start
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

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const secs = Math.floor((diff % (1000 * 60)) / 1000);

  document.getElementById('cd-days').textContent = String(days).padStart(2, '0');
  document.getElementById('cd-hours').textContent = String(hours).padStart(2, '0');
  document.getElementById('cd-mins').textContent = String(mins).padStart(2, '0');
  document.getElementById('cd-secs').textContent = String(secs).padStart(2, '0');
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

// Nav scroll behavior
let lastScroll = 0;
const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  const currentScroll = window.scrollY;
  if (currentScroll > 100) {
    nav.style.boxShadow = '0 2px 20px rgba(0,0,0,0.06)';
  } else {
    nav.style.boxShadow = 'none';
  }
  lastScroll = currentScroll;
});


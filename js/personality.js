
// --- Scroll Progress Bar ---
const progressBar = document.getElementById('scroll-progress');
window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const scrollPercent = (scrollTop / docHeight) * 100;
  progressBar.style.width = scrollPercent + '%';
}, { passive: true });

// --- 3D Tilt on Cards ---
document.querySelectorAll('.bs-card, .product-card, .plush-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -6;
    const rotateY = ((x - centerX) / centerX) * 6;
    card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
    card.classList.add('tilt-active');
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    card.classList.remove('tilt-active');
  });
});

// --- Magnetic Buttons ---
document.querySelectorAll('.btn-primary, .btn-outline, .add-to-cart').forEach(btn => {
  btn.addEventListener('mousemove', (e) => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;
    btn.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
  });
});

// --- Confetti on Add to Cart ---
const confettiCanvas = document.getElementById('confetti-canvas');
const confettiCtx = confettiCanvas.getContext('2d');
confettiCanvas.width = window.innerWidth;
confettiCanvas.height = window.innerHeight;
window.addEventListener('resize', () => {
  confettiCanvas.width = window.innerWidth;
  confettiCanvas.height = window.innerHeight;
});

let confettiPieces = [];
const confettiColors = ['#D2006A', '#CCFF00', '#FFE135', '#FF4B6E', '#6BA368', '#f0e6ff'];
const confettiShapes = ['🍋', '🍓', '🥑', '✨', '💛', '🌸'];

function spawnConfetti(x, y) {
  for (let i = 0; i < 35; i++) {
    confettiPieces.push({
      x, y,
      vx: (Math.random() - 0.5) * 12,
      vy: (Math.random() - 0.7) * 14,
      size: Math.random() * 14 + 8,
      shape: confettiShapes[Math.floor(Math.random() * confettiShapes.length)],
      rotation: Math.random() * 360,
      rotSpeed: (Math.random() - 0.5) * 10,
      gravity: 0.25,
      life: 1,
      decay: 0.012 + Math.random() * 0.008
    });
  }
  if (confettiPieces.length === 35) requestAnimationFrame(animateConfetti);
}

function animateConfetti() {
  confettiCtx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
  confettiPieces = confettiPieces.filter(p => p.life > 0);
  confettiPieces.forEach(p => {
    p.x += p.vx;
    p.vy += p.gravity;
    p.y += p.vy;
    p.vx *= 0.98;
    p.rotation += p.rotSpeed;
    p.life -= p.decay;
    confettiCtx.save();
    confettiCtx.translate(p.x, p.y);
    confettiCtx.rotate((p.rotation * Math.PI) / 180);
    confettiCtx.globalAlpha = p.life;
    confettiCtx.font = p.size + 'px serif';
    confettiCtx.textAlign = 'center';
    confettiCtx.fillText(p.shape, 0, 0);
    confettiCtx.restore();
  });
  if (confettiPieces.length > 0) requestAnimationFrame(animateConfetti);
}

// Attach to Add to Cart buttons
document.querySelectorAll('.add-to-cart').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const rect = btn.getBoundingClientRect();
    spawnConfetti(rect.left + rect.width / 2, rect.top);

    // Button success state
    const origText = btn.innerHTML;
    btn.classList.add('added');
    btn.textContent = 'Added';
    setTimeout(() => {
      btn.classList.remove('added');
      btn.innerHTML = origText;
    }, 1800);

    // Bump cart count
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
      cartCount.textContent = parseInt(cartCount.textContent) + 1;
      cartCount.style.transform = 'scale(1.4)';
      setTimeout(() => cartCount.style.transform = '', 300);
    }
  });
});

// --- Floating Fruit Particles in Hero ---
const hero = document.querySelector('.hero');
if (hero) {
  const fruits = ['🍋', '🍓', '🥑', '🍭', '✨', '🌸', '💜', '🫐'];
  function spawnFruitParticle() {
    const p = document.createElement('span');
    p.className = 'fruit-particle';
    p.textContent = fruits[Math.floor(Math.random() * fruits.length)];
    p.style.left = Math.random() * 100 + '%';
    p.style.bottom = '-20px';
    p.style.fontSize = (Math.random() * 0.8 + 0.8) + 'rem';
    p.style.animationDuration = (Math.random() * 5 + 5) + 's';
    p.style.animationDelay = (Math.random() * 2) + 's';
    hero.appendChild(p);
    setTimeout(() => p.remove(), 12000);
  }
  // Spawn a few on load, then periodically
  for (let i = 0; i < 6; i++) setTimeout(() => spawnFruitParticle(), i * 800);
  setInterval(spawnFruitParticle, 2500);
}

// --- Parallax on Hero Floats ---
const heroFloats = document.querySelectorAll('.hero-float');
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  if (scrollY > 800) return; // Only in hero zone
  heroFloats.forEach(float => {
    const speed = parseFloat(getComputedStyle(float).getPropertyValue('--parallax-speed')) || 0.02;
    float.style.transform = `translateY(${scrollY * speed * -30}px) rotate(${scrollY * speed * 2}deg)`;
  });
}, { passive: true });

// --- Enhanced Stat Counter with glow ---
const origCounterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const num = entry.target;
    if (num.dataset.counted) return;
    num.dataset.counted = 'true';
    num.classList.add('counting');
    const target = parseInt(num.dataset.count);
    const duration = 2000;
    const start = Date.now();
    const tick = () => {
      const elapsed = Date.now() - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(eased * target);
      if (target >= 1000000) num.textContent = (current / 1000000).toFixed(1) + 'M+';
      else if (target >= 1000) num.textContent = Math.floor(current / 1000) + 'K+';
      else num.textContent = current + '+';
      if (progress < 1) requestAnimationFrame(tick);
      else setTimeout(() => num.classList.remove('counting'), 500);
    };
    requestAnimationFrame(tick);
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stat-num[data-count]').forEach(el => origCounterObserver.observe(el));

// --- Konami Code Easter Egg ---
const konamiCode = [38,38,40,40,37,39,37,39,66,65];
let konamiIndex = 0;
document.addEventListener('keydown', (e) => {
  if (e.keyCode === konamiCode[konamiIndex]) {
    konamiIndex++;
    if (konamiIndex === konamiCode.length) {
      document.body.classList.add('konami-active');
      // Shower of fruit confetti from top
      for (let i = 0; i < 60; i++) {
        setTimeout(() => {
          spawnConfetti(Math.random() * window.innerWidth, -20);
        }, i * 50);
      }
      // Flash message
      const msg = document.createElement('div');
      msg.textContent = '🍋 You found the secret! 🍓';
      msg.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:var(--black);color:var(--lime);padding:1.5rem 3rem;border-radius:20px;font-size:1.5rem;font-weight:800;z-index:100000;animation:fadeInOut 3s forwards;pointer-events:none;';
      document.body.appendChild(msg);
      setTimeout(() => {
        msg.remove();
        document.body.classList.remove('konami-active');
      }, 3000);
      konamiIndex = 0;
    }
  } else {
    konamiIndex = 0;
  }
});

// --- Typed/Scramble text effect for hero subtitle ---
const heroSub = document.querySelector('.hero-subtitle');
if (heroSub && heroSub.classList.contains('visible')) {
  // Already visible, skip
} else if (heroSub) {
  const subObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      heroSub.style.opacity = '1';
      subObserver.disconnect();
    });
  }, { threshold: 0.5 });
  subObserver.observe(heroSub);
}

// --- Lottie-style bounce on plush cards entering view ---
const plushBounceObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const img = entry.target.querySelector('.plush-image img');
    if (img) {
      img.style.animation = 'plushBounceIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
      img.addEventListener('animationend', () => img.style.animation = '', { once: true });
    }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.plush-card').forEach(c => plushBounceObserver.observe(c));

// Add the bounceIn keyframes dynamically
const bounceStyle = document.createElement('style');
bounceStyle.textContent = `
  @keyframes plushBounceIn {
    0% { transform: scale(0.8) translateY(20px); opacity: 0.5; }
    60% { transform: scale(1.05) translateY(-5px); opacity: 1; }
    100% { transform: scale(1) translateY(0); opacity: 1; }
  }
  @keyframes fadeInOut {
    0% { opacity: 0; transform: translate(-50%,-50%) scale(0.8); }
    15% { opacity: 1; transform: translate(-50%,-50%) scale(1); }
    80% { opacity: 1; transform: translate(-50%,-50%) scale(1); }
    100% { opacity: 0; transform: translate(-50%,-50%) scale(0.8); }
  }
`;
document.head.appendChild(bounceStyle);

// --- Section entry animations (staggered) ---
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.style.opacity = '1';
    entry.target.style.transform = 'translateY(0)';
  });
}, { threshold: 0.1 });

document.querySelectorAll('.section-header').forEach(header => {
  header.style.opacity = '0';
  header.style.transform = 'translateY(30px)';
  header.style.transition = 'opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
  sectionObserver.observe(header);
});

// --- Double-tap Easter egg on product images ---
document.querySelectorAll('.bs-image, .card-image').forEach(img => {
  let lastTap = 0;
  img.addEventListener('touchend', (e) => {
    const now = Date.now();
    if (now - lastTap < 300) {
      // Double tap! Show heart
      const heart = document.createElement('div');
      heart.textContent = '❤️';
      heart.style.cssText = 'position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(0);font-size:4rem;z-index:100;pointer-events:none;transition:all 0.5s cubic-bezier(0.16, 1, 0.3, 1);';
      img.style.position = 'relative';
      img.appendChild(heart);
      requestAnimationFrame(() => {
        heart.style.transform = 'translate(-50%,-50%) scale(1)';
        heart.style.opacity = '1';
      });
      setTimeout(() => {
        heart.style.transform = 'translate(-50%,-50%) scale(1.5)';
        heart.style.opacity = '0';
        setTimeout(() => heart.remove(), 500);
      }, 600);
    }
    lastTap = now;
  });
});

console.log('%c🍋 Nancy Universe — Pleasure deserved its own universe.', 'font-size: 16px; font-weight: bold; color: #D2006A; background: #111; padding: 8px 16px; border-radius: 8px;');
console.log('%cBuilt with love, mischief, and zero apologies.', 'font-size: 12px; color: #CCFF00; background: #111; padding: 4px 16px; border-radius: 4px;');

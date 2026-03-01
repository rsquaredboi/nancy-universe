// Nancy Universe — PDP Image Gallery
// Thumbnail click to swap main image, keyboard nav
(function() {
  const mainImg = document.getElementById('pdp-main-img');
  const thumbs = document.querySelectorAll('.pdp-gallery-thumbs button');

  if (!mainImg || !thumbs.length) return;

  thumbs.forEach((btn, i) => {
    btn.addEventListener('click', () => {
      const src = btn.querySelector('img').getAttribute('data-full') ||
                  btn.querySelector('img').src;
      const alt = btn.querySelector('img').alt || '';

      // Fade transition
      mainImg.style.opacity = '0';
      setTimeout(() => {
        mainImg.src = src;
        mainImg.alt = alt;
        mainImg.style.opacity = '1';
      }, 200);

      // Update active thumb
      thumbs.forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    const active = document.querySelector('.pdp-gallery-thumbs button.active');
    if (!active) return;
    const idx = Array.from(thumbs).indexOf(active);

    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      const next = thumbs[(idx + 1) % thumbs.length];
      next.click();
      next.focus();
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      const prev = thumbs[(idx - 1 + thumbs.length) % thumbs.length];
      prev.click();
      prev.focus();
    }
  });
})();

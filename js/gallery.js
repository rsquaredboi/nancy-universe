// Nancy Universe — PDP Image Gallery
// Thumbnail click to swap main image, keyboard nav
(function() {
  const mainImg = document.getElementById('pdp-main-img');
  const thumbs = document.querySelectorAll('.pdp-gallery-thumbs button');

  if (!mainImg || !thumbs.length) return;

  // Preload all gallery images on page load
  thumbs.forEach(btn => {
    const src = btn.querySelector('img').getAttribute('data-full') ||
                btn.querySelector('img').src;
    if (src) {
      const img = new Image();
      img.src = src;
    }
  });

  thumbs.forEach((btn, i) => {
    btn.addEventListener('click', () => {
      const src = btn.querySelector('img').getAttribute('data-full') ||
                  btn.querySelector('img').src;
      const alt = btn.querySelector('img').alt || '';

      // Skip if already showing this image
      if (mainImg.src.endsWith(src.split('/').pop())) return;

      // Preload then crossfade
      const preload = new Image();
      preload.src = src;

      const doSwap = () => {
        mainImg.style.opacity = '0';
        setTimeout(() => {
          mainImg.src = src;
          mainImg.alt = alt;
          // Wait for paint then fade in
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              mainImg.style.opacity = '1';
            });
          });
        }, 180);
      };

      if (preload.complete) {
        doSwap();
      } else {
        preload.onload = doSwap;
        // Fallback if image takes too long
        setTimeout(() => { if (!preload.complete) doSwap(); }, 500);
      }

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

// Nancy Universe — PDP Color Picker
(function() {
  const options = document.querySelectorAll('.pdp-color-option');
  const label = document.getElementById('color-name');
  if (!options.length) return;

  options.forEach(btn => {
    btn.addEventListener('click', () => {
      options.forEach(o => o.classList.remove('active'));
      btn.classList.add('active');
      if (label) label.textContent = btn.dataset.color || '';
    });
  });
})();

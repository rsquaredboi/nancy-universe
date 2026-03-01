// Loader progress simulation
(function() {
  var progress = 0;
  var startTime = Date.now();
  var MIN_DISPLAY = 1800; // minimum 1.8s so users see the vibe
  var fill = function() { return document.getElementById('loader-bar-fill'); };
  var tick = setInterval(function() {
    if (progress < 70) progress += Math.random() * 8 + 2;
    else if (progress < 90) progress += Math.random() * 1.5;
    progress = Math.min(progress, 92);
    var el = fill();
    if (el) el.style.width = progress + '%';
  }, 100);

  function dismissLoader() {
    var elapsed = Date.now() - startTime;
    var remaining = Math.max(0, MIN_DISPLAY - elapsed);
    setTimeout(function() {
      clearInterval(tick);
      var el = fill();
      if (el) el.style.width = '100%';
      setTimeout(function() {
        var loader = document.getElementById('loader');
        if (loader) {
          loader.classList.add('loader-exit');
          document.body.classList.remove('loading');
          setTimeout(function() { loader.remove(); }, 700);
        }
      }, 350);
    }, remaining);
  }

  window.addEventListener('load', dismissLoader);
  setTimeout(dismissLoader, 5000); // hard max fallback
})();

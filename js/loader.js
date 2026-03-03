// Loader — fast, minimal
(function() {
  var progress = 0;
  var startTime = Date.now();
  var MIN_DISPLAY = 600; // just enough to see the logo
  var fill = function() { return document.getElementById('loader-bar-fill'); };
  var tick = setInterval(function() {
    if (progress < 60) progress += Math.random() * 12 + 4;
    else if (progress < 85) progress += Math.random() * 3;
    progress = Math.min(progress, 90);
    var el = fill();
    if (el) el.style.width = progress + '%';
  }, 80);

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
          setTimeout(function() { loader.remove(); }, 500);
        }
      }, 200);
    }, remaining);
  }

  window.addEventListener('load', dismissLoader);
  setTimeout(dismissLoader, 3500); // hard max fallback
})();

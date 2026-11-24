/**
 * Presenter chrome for 1920×1080 HTML decks.
 * Keys: ←/→ (or Space/Enter) · N notes · F fullscreen · Home/End
 * Deep-link: #3 opens slide 3.
 */
(function () {
  var slides = [].slice.call(document.querySelectorAll(".slide"));
  var i = 0;
  var panel = document.getElementById("notesPanel");

  function fit() {
    var s = Math.min(innerWidth / 1920, innerHeight / 1080);
    document.documentElement.style.setProperty("--s", s);
  }

  function show(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (el, k) {
      el.classList.toggle("active", k === i);
    });
    if (panel) {
      var a = slides[i].querySelector(".notes");
      panel.innerHTML = "<h4>Notes</h4>" + (a ? a.innerHTML : "");
    }
    if (location.hash !== "#" + (i + 1)) {
      history.replaceState(null, "", "#" + (i + 1));
    }
  }

  addEventListener("keydown", function (e) {
    var k = e.key;
    if (
      k === "ArrowRight" ||
      k === "ArrowDown" ||
      k === "PageDown" ||
      (k === " " && !e.shiftKey) ||
      k === "Enter"
    ) {
      e.preventDefault();
      show(i + 1);
    } else if (
      k === "ArrowLeft" ||
      k === "ArrowUp" ||
      k === "PageUp" ||
      (k === " " && e.shiftKey) ||
      k === "Backspace"
    ) {
      e.preventDefault();
      show(i - 1);
    } else if (k === "Home") {
      e.preventDefault();
      show(0);
    } else if (k === "End") {
      e.preventDefault();
      show(slides.length - 1);
    } else if ((k === "n" || k === "N") && panel) {
      panel.classList.toggle("on");
    } else if (k === "f" || k === "F") {
      document.fullscreenElement
        ? document.exitFullscreen()
        : document.documentElement.requestFullscreen();
    }
  });

  addEventListener("hashchange", function () {
    var n = parseInt(location.hash.slice(1), 10);
    if (n) show(n - 1);
  });

  addEventListener("resize", fit);
  fit();
  var n = parseInt(location.hash.slice(1), 10);
  show(n ? n - 1 : 0);
})();

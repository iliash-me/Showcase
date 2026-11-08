/**
 * Nexora — Template Showcase
 * Vanilla JS, no dependencies.
 */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* Sticky header + back-to-top ------------------------------------------ */
  var header = $(".header");
  var toTop = $(".to-top");

  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 24);
    if (toTop) toTop.classList.toggle("is-visible", y > 800);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* Mobile navigation ---------------------------------------------------- */
  var toggle = $(".nav-toggle");

  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    if (toggle) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      setNav(!document.body.classList.contains("nav-open"));
    });
    $$(".nav a").forEach(function (a) {
      a.addEventListener("click", function () { setNav(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setNav(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 991) setNav(false);
    });
  }

  /* Active nav link on scroll -------------------------------------------- */
  var navLinks = $$('.nav a[href^="#"]');
  if ("IntersectionObserver" in window && navLinks.length) {
    var byId = {};
    navLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) { a.classList.remove("is-active"); });
        var link = byId[entry.target.id];
        if (link) link.classList.add("is-active");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });

    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) spy.observe(el);
    });
  }

  /* Demo filter ---------------------------------------------------------- */
  var filterBtns = $$(".filter-btn");
  var cards = $$(".demo-card[data-category]");

  // Fill in the counts so they never drift from the actual markup.
  filterBtns.forEach(function (btn) {
    var f = btn.getAttribute("data-filter");
    var count = f === "all" ? cards.length : cards.filter(function (c) {
      return c.getAttribute("data-category").split(" ").indexOf(f) > -1;
    }).length;
    var small = $("small", btn);
    if (small) small.textContent = count;
  });

  filterBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-filter");
      filterBtns.forEach(function (b) {
        b.classList.toggle("is-active", b === btn);
        b.setAttribute("aria-pressed", String(b === btn));
      });
      cards.forEach(function (card) {
        var show = f === "all" || card.getAttribute("data-category").split(" ").indexOf(f) > -1;
        card.classList.toggle("is-hidden", !show);
        if (show) {
          card.classList.add("is-revealed");
          if (!reduceMotion && card.animate) {
            card.animate(
              [{ opacity: 0, transform: "translateY(16px) scale(0.98)" }, { opacity: 1, transform: "none" }],
              { duration: 450, easing: "cubic-bezier(0.22, 1, 0.36, 1)" }
            );
          }
        }
      });
    });
  });

  /* Count-up numbers ----------------------------------------------------- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var suffix = el.getAttribute("data-suffix") || "";
    var decimals = (el.getAttribute("data-count").split(".")[1] || "").length;
    if (reduceMotion) { el.textContent = target.toFixed(decimals) + suffix; return; }
    var start = null;
    var dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * eased).toFixed(decimals) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* Score rings ---------------------------------------------------------- */
  function fillRing(el) {
    var val = el.getAttribute("data-score");
    el.style.setProperty("--val", val);
    var label = $("b", el);
    if (label) {
      label.setAttribute("data-count", val);
      countUp(label);
    }
  }

  /* Reveal on scroll ----------------------------------------------------- */
  var revealEls = $$("[data-reveal]");
  var counters = $$("[data-count]").filter(function (el) { return !el.closest(".ring"); });
  var rings = $$(".ring[data-score]");

  if (!("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("is-revealed"); });
    counters.forEach(countUp);
    rings.forEach(fillRing);
    return;
  }

  var io = new IntersectionObserver(function (entries, obs) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      if (el.hasAttribute("data-reveal")) el.classList.add("is-revealed");
      if (el.hasAttribute("data-count")) countUp(el);
      if (el.hasAttribute("data-score")) fillRing(el);
      obs.unobserve(el);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

  revealEls.concat(counters, rings).forEach(function (el) { io.observe(el); });

})();

(function () {
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();

/* Copy-to-clipboard buttons (demo credentials) ----------------------------- */
(function () {
  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } catch (e) { /* ignore */ }
    document.body.removeChild(ta);
  }

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    var label = btn.getAttribute("aria-label") || "Copy";
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var done = function () {
        btn.classList.add("is-copied");
        btn.setAttribute("aria-label", "Copied!");
        setTimeout(function () {
          btn.classList.remove("is-copied");
          btn.setAttribute("aria-label", label);
        }, 1600);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
      } else {
        fallbackCopy(text);
        done();
      }
    });
  });
})();

/* Live customizer: swap preview screenshot & tint ------------------------- */
(function () {
  document.querySelectorAll("[data-customizer]").forEach(function (root) {
    var img = root.querySelector("[data-customizer-target]");
    if (!img) return;

    root.querySelectorAll("[data-src]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        root.querySelectorAll("[data-src]").forEach(function (b) {
          b.classList.toggle("is-active", b === btn);
          b.setAttribute("aria-pressed", String(b === btn));
        });
        var src = btn.getAttribute("data-src");
        if (img.getAttribute("src") === src) return;
        img.classList.add("is-swapping");
        var next = new Image();
        next.onload = function () {
          img.src = src;
          img.classList.remove("is-swapping");
        };
        next.src = src;
      });
    });

    root.querySelectorAll("[data-hue]").forEach(function (sw) {
      sw.addEventListener("click", function () {
        root.querySelectorAll("[data-hue]").forEach(function (s) {
          s.classList.toggle("is-active", s === sw);
          s.setAttribute("aria-pressed", String(s === sw));
        });
        var hue = parseInt(sw.getAttribute("data-hue"), 10) || 0;
        img.style.filter = hue ? "hue-rotate(" + hue + "deg)" : "";
      });
    });
  });
})();

/* Variation switcher (preview helper) ------------------------------------- */
(function () {
  var sw = document.querySelector(".switcher");
  if (!sw) return;
  var btn = sw.querySelector(".switcher__toggle");
  function set(open) {
    sw.classList.toggle("is-open", open);
    btn.setAttribute("aria-expanded", String(open));
  }
  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    set(!sw.classList.contains("is-open"));
  });
  document.addEventListener("click", function (e) {
    if (!sw.contains(e.target)) set(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") set(false);
  });
})();

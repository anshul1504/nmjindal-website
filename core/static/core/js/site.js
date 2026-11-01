(function () {
  "use strict";
  document.documentElement.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var nav = document.getElementById("nav");
  var toTop = document.getElementById("toTop");
  var bar = document.getElementById("scrollProgress");
  var parallax = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));

  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    nav.classList.toggle("scrolled", y > 24);
    toTop.classList.toggle("show", y > 700);
    if (bar && h > 0) { bar.style.width = (y / h * 100) + "%"; }
    if (!reduce) {
      parallax.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        if (r.bottom < -100 || r.top > window.innerHeight + 100) { return; }
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.15;
        el.style.transform = "translate3d(0," + (r.top * -speed).toFixed(1) + "px,0)";
      });
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  // Reveal-on-scroll (text + images)
  var items = document.querySelectorAll(".reveal, .reveal-img");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // Animated counters
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduce || isNaN(target)) { el.textContent = target + suffix; return; }
    var start = null, dur = 1600;
    function step(t) {
      if (start === null) { start = t; }
      var p = Math.min((t - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) { requestAnimationFrame(step); }
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { co.observe(el); });
  } else {
    counters.forEach(countUp);
  }

  // Close the mobile menu after choosing a link
  var menu = document.getElementById("menu");
  document.querySelectorAll("#menu a").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (a.classList.contains("dropdown-toggle") && window.innerWidth < 992) {
        e.preventDefault();
        a.parentElement.classList.toggle("open");
        return;
      }
      if (menu.classList.contains("show") && window.bootstrap) {
        window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
      }
    });
  });

  // Enquiry form: prevent double submit
  var form = document.getElementById("enquiryForm");
  if (form) {
    form.addEventListener("submit", function () {
      var btn = document.getElementById("submitBtn");
      if (form.checkValidity && !form.checkValidity()) { return; }
      btn.disabled = true;
      btn.innerHTML = 'Sending&hellip; <span class="spinner-border spinner-border-sm ms-1" aria-hidden="true"></span>';
    });
  }

  // Bring form feedback into view after a reload
  if (form && document.querySelector("#enquiryForm .alert, #enquiryForm .field-error")) {
    form.scrollIntoView({ block: "center" });
  }

  // Product catalogue filter
  var grid = document.getElementById("productGrid");
  if (grid) {
    var chips = document.querySelectorAll(".filter-bar .chip");
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var f = chip.getAttribute("data-filter");
        chips.forEach(function (c) { c.classList.toggle("active", c === chip); });
        grid.querySelectorAll(":scope > div").forEach(function (col) {
          var show = f === "all" || col.getAttribute("data-cat") === f;
          col.classList.toggle("is-hidden", !show);
          if (show) { col.classList.add("in"); }
        });
      });
    });
  }

  // Horizontal product rail: drag + arrows
  var rail = document.getElementById("rail");
  if (rail) {
    var down = false, startX = 0, startLeft = 0, moved = 0;
    rail.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "touch") { return; }
      down = true; moved = 0; startX = e.clientX; startLeft = rail.scrollLeft;
    });
    window.addEventListener("pointermove", function (e) {
      if (!down) { return; }
      var dx = e.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      if (moved > 5) { rail.classList.add("dragging"); }
      rail.scrollLeft = startLeft - dx;
    });
    window.addEventListener("pointerup", function () { down = false; setTimeout(function () { rail.classList.remove("dragging"); }, 0); });
    rail.addEventListener("click", function (e) { if (moved > 5) { e.preventDefault(); } }, true);
    var by = function (dir) { rail.scrollBy({ left: dir * 360, behavior: reduce ? "auto" : "smooth" }); };
    var prev = document.getElementById("railPrev"), next = document.getElementById("railNext");
    if (prev) { prev.addEventListener("click", function () { by(-1); }); }
    if (next) { next.addEventListener("click", function () { by(1); }); }
  }

  // Farm-to-port journey: swap the sticky image with the active step
  var steps = document.querySelectorAll(".jstep");
  if (steps.length && "IntersectionObserver" in window) {
    var media = document.querySelectorAll(".journey-media img");
    var jo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) { return; }
        var n = e.target.getAttribute("data-step");
        steps.forEach(function (s) { s.classList.toggle("active", s === e.target); });
        media.forEach(function (m) { m.classList.toggle("active", m.getAttribute("data-step") === n); });
      });
    }, { threshold: 0.55, rootMargin: "-10% 0px -10% 0px" });
    steps.forEach(function (s) { jo.observe(s); });
    steps[0].classList.add("active");
  } else {
    steps.forEach(function (s) { s.classList.add("active"); });
  }

  // Hero: crossfade the slides and roll the words (counts come from the admin)
  var slides = document.querySelectorAll(".hx-slide");
  if (slides.length > 1 && !reduce) {
    var si = 0;
    setInterval(function () {
      slides[si].classList.remove("on");
      si = (si + 1) % slides.length;
      slides[si].classList.add("on");
    }, 6500);
  }
  var rollIn = document.querySelector(".roll-in");
  if (rollIn && rollIn.children.length > 2 && !reduce) {
    var ri = 0, total = rollIn.children.length - 1;
    rollIn.style.animation = "none";
    rollIn.style.transition = "transform .7s cubic-bezier(.7,0,.2,1)";
    setInterval(function () {
      ri += 1;
      rollIn.style.transform = "translateY(" + (-1.5 * ri) + "em)";
      if (ri === total) {
        setTimeout(function () {
          rollIn.style.transition = "none"; rollIn.style.transform = "translateY(0)"; ri = 0;
          void rollIn.offsetWidth; rollIn.style.transition = "transform .7s cubic-bezier(.7,0,.2,1)";
        }, 750);
      }
    }, 2400);
  } else if (rollIn) { rollIn.style.animation = "none"; }

  // Hero visual: mouse parallax on the floating cards
  var hv = document.getElementById("hv");
  if (hv && !reduce && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    hv.querySelectorAll("[data-depth]").forEach(function (n) { n.style.setProperty("--d", n.getAttribute("data-depth")); });
    var hero = hv.closest(".hero2");
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      hv.style.setProperty("--mx", ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
      hv.style.setProperty("--my", ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
    });
    hero.addEventListener("pointerleave", function () { hv.style.setProperty("--mx", 0); hv.style.setProperty("--my", 0); });
  }

  // Scroll-linked text zoom: headings grow toward the middle of the screen and ease back out.
  // Reads and writes are batched (no layout thrash) and only on-screen headings are touched.
  if (!reduce) {
    var zoomEls = Array.prototype.slice.call(document.querySelectorAll(".section h2, .page-hero h1, .ft-word"));
    zoomEls.forEach(function (el) {
      var al = getComputedStyle(el).textAlign;
      el.style.transformOrigin = (al === "center") ? "50% 50%" : (al === "right" || al === "end") ? "100% 50%" : "0% 50%";
    });
    var zTick = false;
    var zoomRun = function () {
      zTick = false;
      var vh = window.innerHeight, out = [];
      zoomEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -80 || r.top > vh + 80) { return; }
        out.push([el, Math.min(1, Math.abs((r.top + r.height / 2) - vh * 0.5) / (vh * 0.62))]);
      });
      out.forEach(function (o) {
        var big = o[0].classList.contains("ft-word"), p = o[1];
        var lo = big ? 0.78 : 0.92, hi = big ? 1 : 1.03;
        o[0].style.scale = (lo + (hi - lo) * (1 - p * p)).toFixed(3);
      });
    };
    window.addEventListener("scroll", function () { if (!zTick) { zTick = true; requestAnimationFrame(zoomRun); } }, { passive: true });
    window.addEventListener("resize", zoomRun);
    zoomRun();
  }

  // 3D tilt on cards, magnetic buttons and cursor glow (fine pointers only)
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (fine && !reduce) {
    document.querySelectorAll(".tilt").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.classList.add("tilting");
        el.style.transform = "perspective(900px) rotateY(" + (x * 7).toFixed(2) + "deg) rotateX(" + (-y * 7).toFixed(2) + "deg) translateY(-6px)";
      });
      el.addEventListener("pointerleave", function () { el.classList.remove("tilting"); el.style.transform = ""; });
    });
    document.querySelectorAll(".magnetic").forEach(function (b) {
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + "px," + ((e.clientY - r.top - r.height / 2) * 0.28).toFixed(1) + "px)";
      });
      b.addEventListener("pointerleave", function () { b.style.transform = ""; });
    });
    var glow = document.createElement("div");
    glow.className = "cursor-glow";
    document.body.appendChild(glow);
    window.addEventListener("pointermove", function (e) {
      glow.classList.add("on");
      glow.style.transform = "translate(" + e.clientX + "px," + e.clientY + "px)";
    }, { passive: true });
  }
})();

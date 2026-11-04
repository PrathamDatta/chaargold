(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Mobile nav + dropdown
  var burger = $('.burger'), nav = $('#nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      document.body.classList.toggle('nav-open', open);
    });
    $$('#nav a').forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('open'); document.body.classList.remove('nav-open'); burger.setAttribute('aria-expanded', 'false'); }); });
  }
  $$('.dd > button').forEach(function (b) {
    b.addEventListener('click', function () {
      var dd = b.parentNode, open = dd.classList.toggle('open');
      b.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function (e) {
    $$('.dd.open').forEach(function (d) { if (!d.contains(e.target) && window.innerWidth > 1040) d.classList.remove('open'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { $$('.dd.open').forEach(function (d) { d.classList.remove('open'); }); var lb = $('.lightbox.open'); if (lb) lb.classList.remove('open'); }
  });

  // Reveal on scroll
  var rev = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .12 });
    rev.forEach(function (r) { io.observe(r); });
  } else rev.forEach(function (r) { r.classList.add('in'); });

  // Count-up stats
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  $$('[data-count]').forEach(function (el) {
    var end = parseInt(el.getAttribute('data-count'), 10), suf = el.getAttribute('data-suffix') || '';
    if (reduce || !('IntersectionObserver' in window)) { el.textContent = end + suf; return; }
    var o = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; o.disconnect();
      var t0 = performance.now(), d = 1400;
      (function step(t) { var p = Math.min((t - t0) / d, 1), v = Math.round(end * (1 - Math.pow(1 - p, 3))); el.textContent = v + suf; if (p < 1) requestAnimationFrame(step); })(t0);
    }, { threshold: .6 });
    o.observe(el);
  });

  // Tabs
  $$('[data-tabs]').forEach(function (box) {
    var btns = $$('[role="tab"]', box), panels = $$('[role="tabpanel"]', box.parentNode);
    function show(id) {
      btns.forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute('aria-controls') === id); });
      panels.forEach(function (p) { p.hidden = p.id !== id; });
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { show(b.getAttribute('aria-controls')); }); });
    window.showTab = show;
    function fromHash(scroll) { var id = location.hash.slice(1), el = id && document.getElementById(id); if (el && el.getAttribute('role') === 'tabpanel') { show(id); if (scroll) setTimeout(function () { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 30); } }
    fromHash(true);
    window.addEventListener('hashchange', function () { fromHash(true); });
  });

  // Blog accordion
  $$('.art').forEach(function (a) {
    var t = $('.art-toggle', a);
    t.addEventListener('click', function () { var o = a.classList.toggle('open'); t.textContent = o ? 'Read less' : 'Read full article'; t.setAttribute('aria-expanded', o); if (!o) a.scrollIntoView({ block: 'nearest' }); });
    if (location.hash === '#' + a.id) { a.classList.add('open'); t.textContent = 'Read less'; t.setAttribute('aria-expanded', 'true'); }
  });

  // Lightbox
  var lb = $('.lightbox');
  $$('.gimg').forEach(function (b) { b.addEventListener('click', function () { $('img', lb).src = b.getAttribute('data-full'); $('img', lb).alt = $('img', b).alt; lb.classList.add('open'); }); });
  if (lb) lb.addEventListener('click', function () { lb.classList.remove('open'); });

  // Forms: POST to the endpoint in <meta name="form-endpoint"> (Formspree-style, JSON response).
  // If no endpoint is configured, or the request fails, fall back to opening the visitor's mail app.
  var MAIL = 'contact@chaargold.com';
  var epMeta = $('meta[name="form-endpoint"]'), keyMeta = $('meta[name="form-key"]');
  var ENDPOINT = epMeta ? epMeta.content : '', KEY = keyMeta ? keyMeta.content : '';
  function collect(f) {
    var lines = [], seen = {}, data = {};
    $$('input,select,textarea', f).forEach(function (el) {
      if (!el.name || (el.type === 'checkbox' && !el.checked)) return;
      var label = el.getAttribute('data-label') || el.name;
      if (el.type === 'checkbox') { (seen[label] = seen[label] || []).push(el.value); return; }
      if (el.value.trim()) { lines.push(label + ': ' + el.value.trim()); data[label] = el.value.trim(); }
    });
    Object.keys(seen).forEach(function (k) { lines.push(k + ': ' + seen[k].join(', ')); data[k] = seen[k].join(', '); });
    return { lines: lines, data: data };
  }
  $$('form[data-enquiry]').forEach(function (f) {
    var msg = $('.form-msg', f), btn = $('button[type="submit"]', f);
    var okText = msg ? msg.textContent : '';
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var c = collect(f), subject = f.getAttribute('data-subject') || 'Website enquiry';
      function mailto() {
        location.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(c.lines.join(String.fromCharCode(10)));
        if (msg) { msg.textContent = 'Your email app should have opened with your request. If it did not, write to ' + MAIL + '.'; msg.classList.add('show'); }
      }
      if (!ENDPOINT) return mailto();
      var payload = Object.assign({ _subject: subject, page: location.href }, c.data);
      if (KEY) { payload.access_key = KEY; payload.subject = subject; }
      if (btn) { btn.disabled = true; btn.dataset.t = btn.textContent; btn.textContent = 'Sending…'; }
      fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); f.reset(); if (msg) { msg.textContent = okText; msg.classList.add('show'); } })
        .catch(mailto)
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn.dataset.t; } });
    });
  });
})();

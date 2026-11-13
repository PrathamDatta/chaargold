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
    $$('.dd.open').forEach(function (d) { if (!d.contains(e.target) && window.innerWidth > 1279) d.classList.remove('open'); });
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

  // Contact-page enquiry form: posts JSON to the endpoint on the form (data-endpoint) and reports the result in place.
  $$('form[data-enquiry]').forEach(function (f) {
    var ok = $('.form-msg.ok', f), err = $('.form-msg.err', f), btn = $('button[type="submit"]', f);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var data = {};
      $$('input,textarea', f).forEach(function (el) { if (el.name) data[el.name] = el.value.trim(); });
      data._subject = f.getAttribute('data-subject') || 'Website enquiry';
      data._template = 'table';
      ok.hidden = true; err.hidden = true;
      var label = btn.textContent; btn.disabled = true; btn.textContent = 'Sending…';
      fetch(f.getAttribute('data-endpoint'), { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || j.success === 'false' || j.success === false) throw new Error('send failed'); }); })
        .then(function () { f.reset(); ok.hidden = false; })
        .catch(function () { err.hidden = false; })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });
})();

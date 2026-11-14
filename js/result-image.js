/* "Результат вечора": builds a shareable PNG of a finished tournament's results on a canvas.
   Data comes from <script type="application/json" id="result-image-data"> written by scripts/bake_result_image.py.
   Formats: post 4:5 (2160x2700), square 1:1 (2160x2160), story 9:16 (1080x1920). */
(function () {
  var dataEl = document.getElementById('result-image-data');
  var openBtn = document.getElementById('ri-open');
  var modal = document.getElementById('ri-modal');
  if (!dataEl || !openBtn || !modal) return;
  var D;
  try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var T = D.t;
  var FORMATS = {
    post:   { w: 1080, h: 1350, scale: 2, label: T.f_post,   maxRow: 150 },
    square: { w: 1080, h: 1080, scale: 2, label: T.f_square, maxRow: 150 },
    story:  { w: 1080, h: 1920, scale: 1, label: T.f_story,  maxRow: 175 }
  };
  var fmt = 'post';
  var canvas = document.getElementById('ri-canvas');
  var tabs = document.getElementById('ri-tabs');
  var logoImg = null;
  var lastFocus = null;

  function track(action) {
    try { if (window.gtag) gtag('event', 'result_image', { action: action, format: fmt, tournament: D.slug, lang: D.lang }); } catch (e) {}
  }

  function loadLogo() {
    return new Promise(function (res) {
      if (!D.promoter || !D.promoter.confirmed || !D.promoter.logo) return res(null);
      var im = new Image();
      im.onload = function () { res(im); };
      im.onerror = function () { res(null); };
      im.src = D.promoter.logo;
    });
  }
  function fonts() {
    var f = document.fonts;
    if (!f || !f.load) return Promise.resolve();
    var sample = 'АаБбВв Aa 123';
    return Promise.all([
      f.load('800 40px Manrope', sample), f.load('600 40px Manrope', sample), f.load('500 40px Manrope', sample),
      f.load('700 40px Oswald', sample)
    ]).catch(function () {});
  }

  function rr(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function fit(ctx, text, maxW, size, weight, family, min) {
    var s = size;
    while (s > (min || 14)) {
      ctx.font = weight + ' ' + s + 'px ' + family;
      if (ctx.measureText(text).width <= maxW) break;
      s -= 2;
    }
    ctx.font = weight + ' ' + s + 'px ' + family;
    return s;
  }
  function spaced(ctx, text, x, y, sp, align) {
    // canvas letterSpacing is not everywhere yet: draw by hand
    var w = 0, i;
    for (i = 0; i < text.length; i++) w += ctx.measureText(text[i]).width + sp;
    w -= sp;
    var cx = align === 'right' ? x - w : x;
    for (i = 0; i < text.length; i++) { ctx.fillText(text[i], cx, y); cx += ctx.measureText(text[i]).width + sp; }
    return w;
  }

  function drawQR(ctx, x, y, size) {
    var m = D.qr, n = m.length, quiet = 2, cell = size / (n + quiet * 2);
    ctx.fillStyle = '#fff'; rr(ctx, x, y, size, size, 14); ctx.fill();
    ctx.fillStyle = '#111';
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) {
      if (m[r].charAt(c) === '1') ctx.fillRect(x + (c + quiet) * cell, y + (r + quiet) * cell, Math.ceil(cell), Math.ceil(cell));
    }
  }
  function gold(ctx, cx, cy, r) {
    ctx.fillStyle = '#c9a227'; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#111'; ctx.lineWidth = r * 0.16; ctx.stroke();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = r * 0.22; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(cx - r * 0.42, cy + r * 0.02); ctx.lineTo(cx - r * 0.1, cy + r * 0.34); ctx.lineTo(cx + r * 0.45, cy - r * 0.3); ctx.stroke();
  }

  function draw(cv, key) {
    var F = FORMATS[key], W = F.w, H = F.h;
    cv.width = W * F.scale; cv.height = H * F.scale;
    var ctx = cv.getContext('2d');
    ctx.setTransform(F.scale, 0, 0, F.scale, 0, 0);
    ctx.fillStyle = '#111'; ctx.fillRect(0, 0, W, H);
    var P = 64, SANS = 'Manrope, sans-serif', DISP = 'Oswald, sans-serif';
    ctx.textBaseline = 'alphabetic';
    // top bar: promoter logo (only when confirmed) + our wordmark
    var y = P, barH = 84;
    var confirmed = !!(D.promoter && D.promoter.confirmed && logoImg);
    ctx.fillStyle = '#fff';
    if (confirmed) {
      var lw = Math.min(260, barH * logoImg.width / logoImg.height + 28);
      rr(ctx, P, y, lw, barH, 14); ctx.fill();
      var ih = barH - 24, iw = ih * logoImg.width / logoImg.height;
      if (iw > lw - 24) { iw = lw - 24; ih = iw * logoImg.height / logoImg.width; }
      ctx.drawImage(logoImg, P + (lw - iw) / 2, y + (barH - ih) / 2, iw, ih);
      gold(ctx, P + lw - 2, y + 2, 21);
      ctx.fillStyle = '#fff'; ctx.font = '700 44px ' + DISP; spaced(ctx, 'BOXING 12×3', W - P, y + 58, 4, 'right');
    } else {
      ctx.font = '700 48px ' + DISP; spaced(ctx, 'BOXING 12×3', P, y + 58, 5, 'left');
    }
    y += barH + 56;
    // kicker, title, date
    ctx.fillStyle = '#ff8a7a'; ctx.font = '700 24px ' + SANS; spaced(ctx, T.kicker, P, y, 4, 'left');
    y += 16;
    ctx.fillStyle = '#fff'; var ts = fit(ctx, D.title, W - P * 2, 84, 800, SANS, 40); y += ts + 6;
    ctx.fillText(D.title, P, y);
    ctx.fillStyle = '#aaa'; fit(ctx, D.dateLine, W - P * 2, 28, 500, SANS, 18); y += 46;
    ctx.fillText(D.dateLine, P, y);
    y += 34;
    // footer geometry
    var qr = 150, footTop = H - P - qr;
    // rows
    var rows = D.rows, n = rows.length;
    var avail = footTop - y - 30;
    var rowH = Math.min(F.maxRow, avail / Math.max(n, 1));
    var k = Math.min(1, rowH / 150);
    ctx.strokeStyle = '#2c2c2c'; ctx.lineWidth = 2;
    for (var i = 0; i < n; i++) {
      var ry = y + i * rowH;
      ctx.beginPath(); ctx.moveTo(P, ry); ctx.lineTo(W - P, ry); ctx.stroke();
      var r = rows[i], mid = ry + rowH / 2;
      var mw = 0;
      if (r.m) { ctx.font = '700 ' + Math.round(40 * k) + 'px ' + DISP; mw = ctx.measureText(r.m).width; }
      ctx.fillStyle = '#fff';
      fit(ctx, r.w, W - P * 2 - mw - 30, Math.round(48 * k), 800, SANS, 20);
      ctx.fillText(r.w, P, mid - 2 * k);
      if (r.s) { ctx.fillStyle = '#aaa'; fit(ctx, r.s, W - P * 2 - mw - 30, Math.round(30 * k), 500, SANS, 16); ctx.fillText(r.s, P, mid + 40 * k); }
      if (r.m) { ctx.fillStyle = '#7bd88f'; ctx.font = '700 ' + Math.round(40 * k) + 'px ' + DISP; ctx.textAlign = 'right'; ctx.fillText(r.m, W - P, mid + 10 * k); ctx.textAlign = 'left'; }
    }
    // footer
    ctx.fillStyle = '#fff'; ctx.font = '700 40px ' + DISP; spaced(ctx, 'BOXING12X3.COM', P, footTop + 70, 4, 'left');
    ctx.fillStyle = '#aaa'; ctx.font = '500 26px ' + SANS; ctx.fillText(T.foot, P, footTop + 112);
    drawQR(ctx, W - P - qr, footTop, qr);
  }

  function render() {
    draw(canvas, fmt);
    var btns = tabs.querySelectorAll('button');
    for (var i = 0; i < btns.length; i++) btns[i].classList.toggle('on', btns[i].getAttribute('data-f') === fmt);
  }

  function open() {
    lastFocus = document.activeElement;
    Promise.all([fonts(), loadLogo()]).then(function (r) {
      logoImg = r[1];
      modal.hidden = false; document.body.style.overflow = 'hidden';
      render();
      var c = document.getElementById('ri-close'); if (c) c.focus();
      track('open');
    });
  }
  function close() {
    modal.hidden = true; document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function fileName() { return 'boxing12x3-' + D.slug + '-' + fmt + '.png'; }
  function toBlob(cb) { canvas.toBlob(cb, 'image/png'); }
  function save() {
    toBlob(function (b) {
      if (!b) return;
      var a = document.createElement('a');
      a.href = URL.createObjectURL(b); a.download = fileName();
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
      track('save');
    });
  }
  function share() {
    toBlob(function (b) {
      if (!b) return;
      var file = new File([b], fileName(), { type: 'image/png' });
      navigator.share({ files: [file], title: D.title, text: D.title + ' · ' + D.url }).then(function () { track('share'); }).catch(function () {});
    });
  }
  function copy() {
    var done = function () {
      var el = document.getElementById('ri-copy'); if (!el) return;
      var old = el.textContent; el.textContent = T.copied;
      setTimeout(function () { el.textContent = old; }, 1800);
      track('copy_link');
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(D.url).then(done, done);
    else { var ta = document.createElement('textarea'); ta.value = D.url; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} document.body.removeChild(ta); done(); }
  }

  openBtn.addEventListener('click', open);
  document.getElementById('ri-close').addEventListener('click', close);
  modal.addEventListener('click', function (e) { if (e.target === modal) close(); });
  document.addEventListener('keydown', function (e) { if (!modal.hidden && e.key === 'Escape') close(); });
  tabs.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-f]'); if (!b) return;
    fmt = b.getAttribute('data-f'); render(); track('format');
  });
  document.getElementById('ri-save').addEventListener('click', save);
  document.getElementById('ri-copy').addEventListener('click', copy);
  var sh = document.getElementById('ri-share');
  if (sh) {
    try {
      var probe = new File([new Blob(['x'])], 'x.png', { type: 'image/png' });
      if (navigator.canShare && navigator.canShare({ files: [probe] })) { sh.hidden = false; sh.addEventListener('click', share); }
    } catch (e) {}
  }
})();

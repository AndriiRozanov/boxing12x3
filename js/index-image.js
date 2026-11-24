/* "Індекс 12×3": builds a shareable PNG of a finished tournament's results on a canvas.
   Data comes from <script type="application/json" id="index-image-data"> written by scripts/bake_result_image.py.
   Formats: post 4:5 (2160x2700), square 1:1 (2160x2160), story 9:16 (1080x1920). */
(function () {
  var dataEl = document.getElementById('index-image-data');
  var openBtn = document.getElementById('ri-open');
  var modal = document.getElementById('ri-modal');
  if (!dataEl || !openBtn || !modal) return;
  var D;
  try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var T = D.t;
  var FORMATS = {
    post:   { w: 1080, h: 1350, scale: 2, label: T.f_post,   rows: 4, rowH: 78, ring: 150 },
    square: { w: 1080, h: 1080, scale: 2, label: T.f_square, rows: 3, rowH: 64, ring: 120 },
    story:  { w: 1080, h: 1920, scale: 1, label: T.f_story,  rows: 4, rowH: 92, ring: 210 }
  };
  var fmt = 'post';
  var canvas = document.getElementById('ri-canvas');
  var tabs = document.getElementById('ri-tabs');
  var logoImg = null;
  var lastFocus = null;

  function track(action) {
    try { if (window.gtag) gtag('event', 'index_image', { action: action, format: fmt, fight: D.slug, lang: D.lang }); } catch (e) {}
  }

  function loadLogo() { return Promise.resolve(null);
  }
  function _unusedLoadLogo() {
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

  function ring(ctx, cx, cy, r, w, pct, color, DISP, big) {
    ctx.lineWidth = w; ctx.lineCap = 'butt';
    ctx.strokeStyle = '#2c2c2c'; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.stroke();
    ctx.strokeStyle = color; ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * pct / 100); ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.textAlign = 'center';
    ctx.font = '700 ' + big + 'px ' + DISP; ctx.fillText(String(pct), cx - big * 0.08, cy + big * 0.34);
    var nw = ctx.measureText(String(pct)).width;
    ctx.font = '700 ' + Math.round(big * 0.38) + 'px ' + DISP; ctx.textAlign = 'left';
    ctx.fillText('%', cx - big * 0.08 + nw / 2 + 4, cy + big * 0.34);
    ctx.textAlign = 'left';
  }

  function draw(cv, key) {
    var F = FORMATS[key], W = F.w, H = F.h;
    cv.width = W * F.scale; cv.height = H * F.scale;
    var ctx = cv.getContext('2d');
    ctx.setTransform(F.scale, 0, 0, F.scale, 0, 0);
    ctx.fillStyle = '#111'; ctx.fillRect(0, 0, W, H);
    var P = 64, SANS = 'Manrope, sans-serif', DISP = 'Oswald, sans-serif';
    var RED = '#e0574a', BLUE = '#4a90c2';
    ctx.textBaseline = 'alphabetic';
    var y = P, barH = 84;
    ctx.fillStyle = '#fff'; ctx.font = '700 48px ' + DISP; spaced(ctx, 'BOXING 12×3', P, y + 58, 5, 'left');
    y += barH + 40;
    ctx.fillStyle = '#ff8a7a'; ctx.font = '700 24px ' + SANS; spaced(ctx, T.kicker, P, y, 4, 'left');
    y += 16;
    ctx.fillStyle = '#fff'; var ts = fit(ctx, D.title, W - P * 2, 92, 800, SANS, 40); y += ts + 6;
    ctx.fillText(D.title, P, y);
    ctx.fillStyle = '#aaa'; fit(ctx, D.dateLine, W - P * 2, 28, 500, SANS, 18); y += 46;
    ctx.fillText(D.dateLine, P, y);
    // footer geometry
    var qr = 150, footTop = H - P - qr;
    var rows = D.rows.slice(0, F.rows), n = rows.length;
    var top0 = y + 24, avail = footTop - top0 - 64;           // room for rings + table (note sits under the table)
    var rowH = F.rowH;
    var R = Math.min(F.ring, (avail - n * rowH - 40) / 2.5);
    var lw = Math.round(R * 0.16);
    var blockH = 2 * R + lw + R * 0.34 + 14 + 36 + n * rowH;
    var yy = top0 + Math.max(0, (avail - blockH) / 2);
    var cxs = [W * 0.27, W * 0.73], cy = yy + R + lw / 2;
    ring(ctx, cxs[0], cy, R, lw, D.pa, RED, DISP, Math.round(R * 0.8));
    ring(ctx, cxs[1], cy, R, lw, D.pb, BLUE, DISP, Math.round(R * 0.8));
    ctx.textAlign = 'center'; ctx.font = '700 ' + Math.round(Math.max(R * 0.19, 22)) + 'px ' + SANS;
    var ny = cy + R + lw / 2 + Math.round(R * 0.30) + 8;
    ctx.fillStyle = RED; spacedC(ctx, D.names[0].toUpperCase(), cxs[0], ny, 3);
    ctx.fillStyle = BLUE; spacedC(ctx, D.names[1].toUpperCase(), cxs[1], ny, 3);
    ctx.textAlign = 'left';
    var ty = ny + 36, k = Math.min(1, rowH / 76);
    ctx.strokeStyle = '#2c2c2c'; ctx.lineWidth = 2;
    for (var i = 0; i < n; i++) {
      var ry = ty + i * rowH, r = rows[i], mid = ry + rowH / 2 + 10 * k;
      ctx.beginPath(); ctx.moveTo(P, ry); ctx.lineTo(W - P, ry); ctx.stroke();
      ctx.font = '700 ' + Math.round(38 * k) + 'px ' + DISP; ctx.fillStyle = '#fff';
      ctx.textAlign = 'left'; ctx.fillText(r.l, P, mid);
      ctx.textAlign = 'right'; ctx.fillText(r.r, W - P, mid);
      ctx.textAlign = 'center'; ctx.fillStyle = '#9a9a9a'; ctx.font = '600 ' + Math.round(26 * k) + 'px ' + SANS;
      ctx.fillText(r.label.toUpperCase(), W / 2, mid - 2);
    }
    // footer
    ctx.textAlign = 'left';
    ctx.fillStyle = '#fff'; ctx.font = '700 40px ' + DISP; spaced(ctx, 'BOXING12X3.COM', P, footTop + 70, 4, 'left');
    ctx.fillStyle = '#aaa'; ctx.font = '500 26px ' + SANS; ctx.fillText(T.foot, P, footTop + 112);
    // watermark where the QR used to be: big faint mark, hard to crop out
    ctx.save(); ctx.globalAlpha = 0.14; ctx.fillStyle = '#fff'; ctx.textAlign = 'right';
    ctx.font = '700 170px ' + DISP; ctx.fillText('12×3', W - P, footTop + qr - 8); ctx.restore();
  }
  function spacedC(ctx, text, cx, y, sp) {
    var w = 0, i; for (i = 0; i < text.length; i++) w += ctx.measureText(text[i]).width + sp; w -= sp;
    ctx.textAlign = 'left'; var x = cx - w / 2;
    for (i = 0; i < text.length; i++) { ctx.fillText(text[i], x, y); x += ctx.measureText(text[i]).width + sp; }
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
  function fileName() { return 'boxing12x3-index-' + D.slug + '-' + fmt + '.png'; }
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

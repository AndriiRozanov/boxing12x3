/* Boxing 12x3: "Your time" line under broadcast times.
   Reads [data-utc] on .broadcast-time, adds a second line in the visitor's own time zone.
   Static ET/PT/GMT (EN) and Kyiv (UA) text stays in the HTML for search engines.
   The line is skipped when the visitor's clock already equals one of the listed zones. */
(function () {
  var tz;
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) { return; }
  if (!tz) return;
  var uk = (document.documentElement.lang || '').toLowerCase().indexOf('uk') === 0;

  function parts(d, z) {
    var p = {};
    new Intl.DateTimeFormat('en-US', {
      timeZone: z, year: 'numeric', month: 'numeric', day: 'numeric',
      hour: 'numeric', minute: 'numeric', hourCycle: 'h23'
    }).formatToParts(d).forEach(function (x) { p[x.type] = +x.value; });
    return p;
  }
  function off(d, z) {
    var p = parts(d, z);
    return Math.round((Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute) - d.getTime()) / 60000);
  }

  var ZONES = { ET: 'America/New_York', PT: 'America/Los_Angeles', GMT: 'Europe/London', BST: 'Europe/London', CET: 'Europe/Berlin', JST: 'Asia/Tokyo' };
  var MON = {
    en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    uk: ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']
  };
  var LBL = {
    en: { '': 'Your time:', approx: 'Your time (approx.):', notbefore: 'Your time (not before):' },
    uk: { '': 'Ваш час:', approx: 'Ваш час (приблизно):', notbefore: 'Ваш час (не раніше):' }
  };

  var st = document.createElement('style');
  st.textContent = '.broadcast-local{display:block;font-size:12px;font-weight:600;color:var(--text);margin-top:2px;}' +
    '.broadcast-local .bl-lbl{font-weight:400;color:var(--muted);}';
  document.head.appendChild(st);

  var nodes = document.querySelectorAll('.broadcast-time[data-utc]');
  for (var n = 0; n < nodes.length; n++) {
    var el = nodes[n];
    var d = new Date(el.getAttribute('data-utc'));
    if (isNaN(d.getTime())) continue;
    var o = off(d, tz);

    // zones already listed in the row text
    var txt = el.textContent, listed = [];
    if (uk) listed.push('Europe/Kyiv');
    else Object.keys(ZONES).forEach(function (k) { if (new RegExp('\\b' + k + '\\b').test(txt)) listed.push(ZONES[k]); });
    var dup = false;
    for (var i = 0; i < listed.length; i++) { if (off(d, listed[i]) === o) { dup = true; break; } }
    if (dup) continue;

    var p = parts(d, tz), mm = ('0' + p.minute).slice(-2), a = Math.abs(o);
    var u = 'UTC' + (o < 0 ? '-' : '+') + Math.floor(a / 60) + (a % 60 ? ':' + ('0' + (a % 60)).slice(-2) : '');
    var q = el.getAttribute('data-q') || '';
    var lang = uk ? 'uk' : 'en', t, day;
    if (uk) { t = ('0' + p.hour).slice(-2) + ':' + mm; day = p.day + ' ' + MON.uk[p.month - 1]; }
    else { t = (p.hour % 12 || 12) + ':' + mm + ' ' + (p.hour < 12 ? 'AM' : 'PM'); day = MON.en[p.month - 1] + ' ' + p.day; }

    var span = document.createElement('span');
    span.className = 'broadcast-local';
    span.innerHTML = '<span class="bl-lbl">' + (LBL[lang][q] || LBL[lang]['']) + '</span> ' + day + ' · ' + t + ' <span class="bl-lbl">(' + u + ')</span>';
    el.parentNode.insertBefore(span, el.nextSibling);
  }
})();

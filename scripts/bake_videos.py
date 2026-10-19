#!/usr/bin/env python3
"""Insert 'watch the fight' buttons (with click-to-load YouTube embed) into key-fight rows of boxer cards.

Data: scripts/fight_videos.csv (slug,date,video_id,row,fight). Idempotent: removes old baked
blocks first. Usage: python3 scripts/bake_videos.py [slug ...]   (no args = all cards)
"""
import csv, re, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
T = {'ua': dict(w='Дивитись бій', h='Сховати відео', y='Відкрити на YouTube ↗'),
     'en': dict(w='Watch the fight', h='Hide video', y='Open on YouTube ↗')}
CSS = '''/*kfv*/.vbtn{display:inline-flex;align-items:center;gap:7px;margin-top:10px;padding:7px 12px;border:1px solid #e6a49c;background:#fdf2f2;color:#c0392b;border-radius:20px;font:600 12px 'DM Sans',sans-serif;text-decoration:none;cursor:pointer;}
.vbtn:hover{background:#fbe5e3;}
.vbtn.on{background:#fff;border-color:#ddd;color:#555;}
.vwrap{margin-top:10px;}
.vplayer{position:relative;aspect-ratio:16/9;border-radius:8px;overflow:hidden;background:#000;}
.vplayer iframe{position:absolute;inset:0;width:100%;height:100%;border:0;}
.vcap{display:flex;justify-content:flex-end;font-size:11px;margin-top:6px;}
.vcap a{color:var(--muted);text-decoration:none;border-bottom:0.5px solid #bbb;}
/*/kfv*/
'''
JS = '''<script>/*kfv*/
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.vbtn');if(!b)return;e.preventDefault();
var card=b.closest('.card'),was=b.classList.contains('on');
card.querySelectorAll('.vbtn.on').forEach(function(x){x.classList.remove('on');x.querySelector('.vt').textContent=x.dataset.w;var w=x.parentNode.querySelector('.vwrap');if(w)w.remove();});
if(was)return;
var id=b.dataset.vid,w=document.createElement('div');w.className='vwrap';
w.innerHTML='<div class="vplayer"><iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1" title="YouTube" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div><div class="vcap"><a href="https://www.youtube.com/watch?v='+id+'" target="_blank" rel="noopener">'+b.dataset.y+'</a></div>';
b.after(w);b.classList.add('on');b.querySelector('.vt').textContent=b.dataset.h;
if(typeof gtag!=='undefined')gtag('event','video_play',{video_id:id,page:location.pathname});
});/*/kfv*/</script>
'''
PLAY = '<svg width="11" height="11" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1l9 5-9 5z" fill="currentColor"/></svg>'
ITEM = re.compile(r'<div class="kf-item[^"]*"[^>]*>.*?</div></div></div>', re.S)
DATE = re.compile(r'<div class="kf-year">(\d{4})</div><div class="kf-day">([^<]*)</div>')

def clean(s):
    s = re.sub(r'<!--kfv-->.*?<!--/kfv-->', '', s, flags=re.S)
    s = re.sub(r'<script>/\*kfv\*/.*?/\*/kfv\*/</script>\n?', '', s, flags=re.S)
    s = re.sub(r'/\*kfv\*/.*?/\*/kfv\*/\n?', '', s, flags=re.S)
    return s

def button(lang, vid):
    t = T[lang]
    return ('<!--kfv--><a class="vbtn" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" data-vid="%s" '
            'data-w="%s" data-h="%s" data-y="%s">%s<span class="vt">%s</span></a><!--/kfv-->') % (vid, vid, t['w'], t['h'], t['y'], PLAY, t['w'])

def main(only):
    vids = {}
    with open(R/'scripts'/'fight_videos.csv', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            vids.setdefault(r['slug'], {})[r['date']] = r['video_id']
    n = 0
    for slug, byd in sorted(vids.items()):
        if only and slug not in only: continue
        pages = {l: (R/l/'boxers'/(slug+'.html')) for l in ('ua', 'en')}
        html = {l: clean(p.read_text(encoding='utf-8')) for l, p in pages.items()}
        items = {l: list(ITEM.finditer(html[l])) for l in html}
        assert len(items['ua']) == len(items['en']), slug
        # decide per index using UA dates (dd.mm)
        todo = {}
        for i, m in enumerate(items['ua']):
            y, dm = DATE.search(m.group(0)).groups()
            d, mo = dm.split('.')
            vid = byd.get('%s-%s-%s' % (y, mo, d))
            if vid:
                assert DATE.search(items['en'][i].group(0)).group(1) == y, (slug, i)
                todo[i] = vid
        assert len(todo) == len(byd), (slug, len(todo), len(byd), set(byd))
        for l in ('ua', 'en'):
            s = html[l]
            for i in sorted(todo, reverse=True):
                m = items[l][i]; blk = m.group(0)
                s = s[:m.start()] + blk[:-12] + button(l, todo[i]) + blk[-12:] + s[m.end():]
            assert s.count('</style>') >= 1
            s = s.replace('</style>', CSS + '</style>', 1)
            k = s.rindex('</body>')
            s = s[:k] + JS + s[k:]
            pages[l].write_text(s, encoding='utf-8')
        n += len(todo)
    print('buttons:', n)

if __name__ == '__main__':
    main(set(sys.argv[1:]))

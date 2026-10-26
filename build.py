# -*- coding: utf-8 -*-
"""parts/*.html 을 합쳐 index.html, 학습지모음.html 을 만든다.
   실행:  python build.py
"""
import os, re, sys, io

ROOT = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(ROOT, 'parts')
ORDER = ['00_head.html','01_home.html','02_s1_s3.html','03_s4_s6.html','04_s7_s10.html','05_guide.html','06_script.html']

def read(p):
    with io.open(p, 'r', encoding='utf-8') as f: return f.read()
def write(p, s):
    with io.open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)

html = ''.join(read(os.path.join(PARTS, n)) for n in ORDER)
write(os.path.join(ROOT, 'index.html'), html)

# ---------- 학습지모음 ----------
def extract_ws(src):
    out = []
    for m in re.finditer(r'<div class="ws" data-ws="(s\d+)">', src):
        start = m.start(); i = m.end(); depth = 1
        tag = re.compile(r'<div\b|</div>')
        while depth:
            t = tag.search(src, i)
            if not t: raise SystemExit('unbalanced div in ' + m.group(1))
            depth += 1 if t.group(0).startswith('<div') else -1
            i = t.end()
        out.append((m.group(1), src[start:i]))
    return out

style = re.search(r'<style>.*?</style>', html, re.S).group(0)
oxdata = re.search(r'<!-- OX_DATA:start -->.*?<!-- OX_DATA:end -->', html, re.S).group(0)
ws_blocks = extract_ws(html)

ws_html = u'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>청소년 노동인권 10차시 학습지 모음</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@500;700;800&family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap">
''' + style + u'''
<style>
.wsmain{max-width:860px;margin:0 auto;padding:1.5rem 16px 4rem;display:flex;flex-direction:column;gap:2rem}
.wsmain .ws{padding:1.4rem 1.6rem}
.wsbar{position:sticky;top:0;z-index:5;background:var(--bg);padding:.6rem 0;border-bottom:1px solid var(--line)}
body.show-ans .ws .blank .a{opacity:1}
body.show-ans .ws .wsox .box span.k{background:var(--primary);color:var(--primary-ink);border-color:var(--primary)}
.ws .wsox .box span.k{background:transparent;color:inherit;border-color:var(--fg)}
.wsmain h1{font-size:1.6rem}
@media print{.wsmain{padding:0;max-width:none;gap:0}.wsmain>h1,.wsmain>p{display:none}.ws{break-before:page;border:0;padding:0}.ws:first-of-type{break-before:auto}}
</style>
</head>
<body>
<main class="wsmain">
  <h1>청소년 노동인권 10차시 · 학습지 모음</h1>
  <p class="muted">차시별 학습지 10장입니다. 인쇄하면 차시마다 새 페이지에서 시작합니다. 교사용으로 정답을 표시한 채 인쇄할 수 있습니다.</p>
  <div class="wsbar">
    <button type="button" class="btn pri" id="printAll">전체 인쇄</button>
    <label class="btn"><input type="checkbox" id="ansToggle"> 정답 표시 (교사용)</label>
    <span class="muted" style="font-size:.85rem">특정 차시만 인쇄하려면 브라우저 인쇄 창에서 페이지 범위를 지정하세요.</span>
  </div>
''' + u'\n'.join(b for _, b in ws_blocks) + u'''
</main>
''' + oxdata + u'''
<script>
(function(){
  Object.keys(OX_DATA).forEach(function(set){
    var ol = document.querySelector('.wsox[data-set="'+set+'"]'); if(!ol) return;
    ol.innerHTML = OX_DATA[set].map(function(it,i){
      return '<li><span><span class="i">'+(i+1)+'.</span>'+it.q+'</span><span class="box"><span class="'+(it.a?'k':'')+'">O</span><span class="'+(it.a?'':'k')+'">X</span></span></li>';
    }).join('');
  });
  document.getElementById('ansToggle').addEventListener('change', function(e){ document.body.classList.toggle('show-ans', e.target.checked); });
  document.getElementById('printAll').addEventListener('click', function(){ window.print(); });
})();
</script>
</body>
</html>
'''
write(os.path.join(ROOT, u'학습지모음.html'), ws_html)

# ---------- 아티팩트용(래퍼 제거) ----------
art = html
for pat in [r'<!doctype html>\s*', r'<html lang="ko">\s*', r'<head>\s*', r'<meta charset="utf-8">\s*',
            r'<meta name="viewport"[^>]*>\s*', r'</head>\s*', r'<body>\s*', r'</body>\s*', r'</html>\s*']:
    art = re.sub(pat, '', art, count=1)
artdir = sys.argv[1] if len(sys.argv) > 1 else ROOT
write(os.path.join(artdir, 'artifact.html'), art)

print('index.html: %d bytes' % len(html.encode('utf-8')))
print('학습지모음.html: %d bytes, %d worksheets' % (len(ws_html.encode('utf-8')), len(ws_blocks)))
print('artifact.html -> ' + artdir)

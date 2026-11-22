#!/usr/bin/env python3
"""홈페이지 HTML 페이지를 한 번에 만든다 — 한글(/) · 영문(/en/) 소개 · 논문 · 수업 · 과목별 페이지.
머리글 · 꼬리말 · 글꼴 링크가 모든 페이지에서 같도록 이 스크립트로만 고친다(페이지 파일을 손으로 고치지 말 것).
과목 목록은 teaching/sims.json 의 courses 에서 읽으므로, 새 과목은 sims.json 에 넣고 이 스크립트를 다시 돌리면
teaching/<id>/index.html 과 en/teaching/<id>/index.html 이 생긴다.
사용 : python3 tools/build_pages.py   (저장소 맨 위에서)
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
SITE = 'https://sangookmoon.github.io'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400'
         '&family=Noto+Sans+KR:wght@400;500;700&display=swap">')

T = {
    'ko': dict(name='문상국', about='소개', pubs='논문', teach='수업', lang='English', other='en',
               updated='마지막 수정', copy='© 2026 문상국',
               lic='시뮬레이터 © 2026 문상국. 수업·학습에 그대로 쓰는 것은 자유이며, 고치거나 다른 곳에 다시 올리려면 먼저 허락을 받아 주세요. '
                   '(<a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ko" rel="license">CC BY-NC-ND 4.0</a>)'),
    'en': dict(name='Sangook Moon', about='About', pubs='Publications', teach='Teaching', lang='한국어', other='ko',
               updated='Last updated', copy='© 2026 Sangook Moon',
               lic='Simulators © 2026 Sangook Moon. Free to use as-is for teaching and learning; please ask for permission before modifying or re-hosting them. '
                   '(<a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" rel="license">CC BY-NC-ND 4.0</a>)'),
}


def url(lang, path):
    return ('/en' if lang == 'en' else '') + path


def page(lang, path, title, active, body, desc='', lic=False, script=''):
    t = T[lang]
    o = 'en' if lang == 'ko' else 'ko'
    nav = ''.join('<a%s href="%s">%s</a>' % (' class="on"' if k == active else '', url(lang, p), t[k])
                  for k, p in (('about', '/'), ('pubs', '/publications.html'), ('teach', '/teaching/')))
    nav += '<a class="lang" href="%s" hreflang="%s" lang="%s">%s</a>' % (url(o, path), o, o, t['lang'])
    logos = ('<img class="lg-l" src="/assets/logo.svg" alt="%s" width="130" height="33">'
             '<img class="lg-d" src="/assets/logo-dark.svg" alt="" width="130" height="33">') % ('목원대학교' if lang == 'ko' else 'Mokwon University')
    foot = '<span>%s</span><span>%s %s</span>' % (t['copy'], t['updated'], TODAY)
    if lic:
        foot += '<span class="lic">%s</span>' % t['lic']
    d = desc or ('문상국, 목원대학교 전기전자공학과 교수. 하드웨어 보안, FPGA, 암호 하드웨어, 산업 IoT.' if lang == 'ko' else
                 'Sangook Moon, Professor of Electrical and Electronic Engineering, Mokwon University. Hardware security, FPGA, cryptographic hardware, industrial IoT.')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{d}">
<link rel="alternate" hreflang="{o}" href="{SITE}{url(o, path)}">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="{url(lang, '/')}">{logos}<span class="nm">{t['name']}</span></a>
  <nav class="menu">{nav}</nav>
</div></header>

<main><div class="wrap">
{body}
</div></main>

<footer><div class="wrap">{logos}{foot}</div></footer>
{script}</body>
</html>
'''


def write(rel, html):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(html)
    print('wrote', rel)


# ---------- 소개 ----------
ABOUT = {
 'ko': '''  <section class="hero">
    <img class="photo" src="/assets/photo.jpg" width="160" height="200" alt="문상국 사진">
    <div>
      <h1>문상국<span class="alt">Sangook Moon</span></h1>
      <p class="sub">목원대학교 전기전자공학과 교수</p>
      <div class="links"><a href="https://scholar.google.com/citations?user=AWfixSwAAAAJ">Google Scholar</a><a href="https://orcid.org/0000-0002-0290-1887">ORCID</a><a href="/cv/Sangook_Moon_CV.pdf">CV</a><a href="mailto:smoon@mokwon.ac.kr">이메일</a></div>
    </div>
  </section>

  <h2>연구 분야</h2>
  <p class="kw">하드웨어 보안 · FPGA · 암호 하드웨어 · 산업 IoT · 컴퓨터 산술</p>
  <p>자원이 제한된 SoC-FPGA 위에서 동작하는 암호·보안 하드웨어와 산업 IoT용 실시간 신호처리 하드웨어를 연구합니다. 경량 암호(ASCON), 준동형 암호, 실시간 이상 탐지 엔진, 초음파 누설 감시 시스템의 하드웨어 구현이 최근 주제입니다.</p>

  <h2>학력</h2>
  <table class="cv">
    <tr><td>2002</td><td>공학박사, 전기전자공학, 연세대학교</td></tr>
    <tr><td>1997</td><td>공학석사, 전자공학, 연세대학교</td></tr>
    <tr><td>1995</td><td>공학사, 전자공학, 연세대학교</td></tr>
  </table>

  <h2>경력</h2>
  <table class="cv">
    <tr><td>2004 – 현재</td><td>목원대학교 전기전자공학과 교수</td></tr>
    <tr><td>2002 – 2004</td><td>SK하이닉스 선임연구원(무선통신 칩 설계)</td></tr>
  </table>

  <h2>수업</h2>
  <p>수업에서 쓰는 웹 시뮬레이터를 과목별로 모아 둡니다. 설치 없이 브라우저에서 바로 열립니다. <a class="nw" href="/teaching/">수업·시뮬레이터 보기 →</a></p>

  <h2>연락처</h2>
  <ul class="plain">
    <li>35349 대전광역시 서구 도안북로 88 목원대학교 전기전자공학과</li>
    <li>전화 <a href="tel:+82428297637">042-829-7637</a> · 이메일 <a href="mailto:smoon@mokwon.ac.kr">smoon@mokwon.ac.kr</a></li>
  </ul>''',
 'en': '''  <section class="hero">
    <img class="photo" src="/assets/photo.jpg" width="160" height="200" alt="Photo of Sangook Moon">
    <div>
      <h1>Sangook Moon</h1>
      <p class="sub">Professor, Department of Electrical and Electronic Engineering<br>Mokwon University, Daejeon, Korea</p>
      <div class="links"><a href="https://scholar.google.com/citations?user=AWfixSwAAAAJ">Google Scholar</a><a href="https://orcid.org/0000-0002-0290-1887">ORCID</a><a href="/cv/Sangook_Moon_CV.pdf">CV</a><a href="mailto:smoon@mokwon.ac.kr">Email</a></div>
    </div>
  </section>

  <h2>Research</h2>
  <p class="kw">Hardware security · FPGA · Cryptographic hardware · Industrial IoT · Computer arithmetic</p>
  <p>I work on cryptographic and security hardware for resource-constrained SoC-FPGAs, and on real-time signal-processing hardware for the industrial Internet of Things. Recent topics include lightweight cryptography (ASCON), homomorphic encryption, real-time anomaly-detection engines, and hardware for ultrasonic leak monitoring.</p>

  <h2>Education</h2>
  <table class="cv">
    <tr><td>2002</td><td>Ph.D. in Electrical and Electronic Engineering, Yonsei University</td></tr>
    <tr><td>1997</td><td>M.S. in Electronic Engineering, Yonsei University</td></tr>
    <tr><td>1995</td><td>B.S. in Electronic Engineering, Yonsei University</td></tr>
  </table>

  <h2>Experience</h2>
  <table class="cv">
    <tr><td>2004 – present</td><td>Professor, Department of Electrical and Electronic Engineering, Mokwon University</td></tr>
    <tr><td>2002 – 2004</td><td>Senior Research Engineer, SK hynix (wireless communication IC design)</td></tr>
  </table>

  <h2>Teaching</h2>
  <p>Interactive web simulators from my courses, organized by course. They run in the browser with no installation. <a class="nw" href="/en/teaching/">Teaching →</a></p>

  <h2>Contact</h2>
  <ul class="plain">
    <li>Department of Electrical and Electronic Engineering, Mokwon University<br>88 Doanbuk-ro, Seo-gu, Daejeon 35349, Republic of Korea</li>
    <li>Phone <a href="tel:+82428297637">+82-42-829-7637</a> · Email <a href="mailto:smoon@mokwon.ac.kr">smoon@mokwon.ac.kr</a></li>
  </ul>''',
}

# ---------- 논문 ----------
PUB_JS = '''<script>
const L10N=%s;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let all=[];
function render(){
  const q=document.getElementById('q').value.trim().toLowerCase();
  const k=document.querySelector('input[name=kind]:checked').value;
  const L=all.filter(p=>!p.hidden&&(k==='all'||p.kind===k)&&(!q||(p.title+' '+p.authors+' '+(p.venue_full||p.venue)).toLowerCase().includes(q)));
  document.getElementById('cnt').textContent=L10N.count(L.length);
  let html='',y=null;
  for(const p of L){
    const yr=p.year||L10N.noyear;
    if(yr!==y){html+='<div class="pubyear">'+esc(yr)+'</div>';y=yr;}
    const a=esc(p.authors).replace(/S Moon|SG Moon|S-G Moon|SangGook Moon|Sangook Moon|S\\. Moon/g,m=>'<b>'+m+'</b>');
    const t=p.url?'<a href="'+esc(p.url)+'">'+esc(p.title)+'</a>':esc(p.title);
    html+='<div class="pub"><div class="t">'+t+'</div><div class="a">'+a+'</div><div class="v">'+esc(p.venue_full||p.venue)+(p.cites?' <span class="c">· '+L10N.cited(p.cites)+'</span>':'')+'</div></div>';
  }
  document.getElementById('list').innerHTML=html;
}
fetch('/assets/publications.json').then(r=>r.json()).then(d=>{
  all=d.pubs; document.getElementById('meta').innerHTML=L10N.meta(d);
  render();
});
document.getElementById('q').addEventListener('input',render);
document.querySelectorAll('input[name=kind]').forEach(e=>e.addEventListener('change',render));
</script>
'''
PUB_L10N = {
 'ko': "{count:n=>n+'편',noyear:'연도 미상',cited:n=>'인용 '+n,meta:d=>'Google Scholar 기준 · <span class=\"nw\">인용 '+d.citations+'</span> · <span class=\"nw\">h-index '+d.h+'</span> · <span class=\"nw\">i10-index '+d.i10+'</span> · '+d.updated+' 갱신'}",
 'en': "{count:n=>n+(n===1?' paper':' papers'),noyear:'Year unknown',cited:n=>'cited by '+n,meta:d=>'From Google Scholar · <span class=\"nw\">'+d.citations+' citations</span> · <span class=\"nw\">h-index '+d.h+'</span> · <span class=\"nw\">i10-index '+d.i10+'</span> · updated '+d.updated}",
}
PUBS = {
 'ko': '''  <h1>논문</h1>
  <p class="sub" id="meta">Google Scholar 기준</p>
  <div class="filter"><input id="q" type="search" placeholder="제목·저자·학술지로 찾기" aria-label="논문 찾기"><span class="seg" role="radiogroup"><label><input type="radio" name="kind" value="all" checked>전체</label><label><input type="radio" name="kind" value="journal">학술지</label><label><input type="radio" name="kind" value="conference">학술대회</label></span><span class="note" id="cnt"></span></div>
  <div id="list"></div>
  <p class="note" style="margin-top:28px">전체 목록과 인용 정보는 <a href="https://scholar.google.com/citations?user=AWfixSwAAAAJ">Google Scholar</a>에서 볼 수 있습니다.</p>''',
 'en': '''  <h1>Publications</h1>
  <p class="sub" id="meta">From Google Scholar</p>
  <div class="filter"><input id="q" type="search" placeholder="Search title, author, or venue" aria-label="Search publications"><span class="seg" role="radiogroup"><label><input type="radio" name="kind" value="all" checked>All</label><label><input type="radio" name="kind" value="journal">Journals</label><label><input type="radio" name="kind" value="conference">Conferences</label></span><span class="note" id="cnt"></span></div>
  <div id="list"></div>
  <p class="note" style="margin-top:28px">The full list with citation details is on <a href="https://scholar.google.com/citations?user=AWfixSwAAAAJ">Google Scholar</a>.</p>''',
}

# ---------- 수업 ----------
TEACH = {
 'ko': ('  <h1>수업·시뮬레이터</h1>\n  <p class="sub">목원대학교 전기전자공학과 수업에서 쓰는 웹 시뮬레이터입니다. 설치 없이 브라우저에서 바로 열립니다.</p>\n  <div id="courses"></div>'),
 'en': ('  <h1>Teaching</h1>\n  <p class="sub">Interactive web simulators I use in courses at the Department of Electrical and Electronic Engineering, Mokwon University. They open in the browser with no installation; the simulators themselves currently have a Korean interface.</p>\n  <div id="courses"></div>'),
}


def main():
    sims = json.load(open(os.path.join(ROOT, 'teaching', 'sims.json'), encoding='utf-8'))
    for lang in ('ko', 'en'):
        pre = 'en/' if lang == 'en' else ''
        t = T[lang]
        write(pre + 'index.html', page(lang, '/', (t['name'] + (' | 목원대학교 전기전자공학과' if lang == 'ko' else ' | Mokwon University')),
                                       'about', ABOUT[lang]))
        write(pre + 'publications.html', page(lang, '/publications.html', t['pubs'] + ' | ' + t['name'], 'pubs', PUBS[lang],
                                              script=PUB_JS % PUB_L10N[lang]))
        js = '<script src="/teaching/teaching.js"></script>\n'
        write(pre + 'teaching/index.html', page(lang, '/teaching/', ('수업·시뮬레이터' if lang == 'ko' else 'Teaching') + ' | ' + t['name'], 'teach',
                                                TEACH[lang], lic=True, script=js + "<script>renderTeaching(null,'%s');</script>\n" % lang))
        for c in sims['courses']:
            cname = c['name'] if lang == 'ko' else c['en']
            alt = '<span class="alt">%s</span>' % c['en'] if lang == 'ko' else ''
            crumb = '<p class="crumb"><a href="%s">%s</a> ›</p>' % (url(lang, '/teaching/'), '수업·시뮬레이터' if lang == 'ko' else 'Teaching')
            desc = c['desc'] if lang == 'ko' else c.get('desc_en', c['desc'])
            body = '  %s\n  <h1>%s%s</h1>\n  <p class="sub">%s</p>\n  <div id="courses"></div>' % (crumb, cname, alt, desc)
            write(pre + 'teaching/%s/index.html' % c['id'],
                  page(lang, '/teaching/%s/' % c['id'], cname + ' | ' + t['name'], 'teach', body, lic=True,
                       script=js + "<script>renderTeaching('%s','%s');</script>\n" % (c['id'], lang)))


if __name__ == '__main__':
    main()

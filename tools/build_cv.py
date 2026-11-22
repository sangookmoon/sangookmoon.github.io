#!/usr/bin/env python3
"""영문 CV 를 만든다 : cv/Sangook_Moon_CV.html → (크롬 CDP 로) cv/Sangook_Moon_CV.pdf
논문은 assets/publications.json 에서 읽어 학술지 / 학술대회로 나눈다(hidden 항목 제외).
사용 : python3 tools/build_cv.py        (PDF 는 9222 디버그 크롬이 떠 있을 때 만든다)
"""
import json, os, re, datetime, html, base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today()
E = html.escape


def ieee_author(a):
    """스칼라 'YR Choi' → 'Y. R. Choi', 'S Moon' → 'S. Moon'. 본인은 굵게."""
    out = []
    for name in [x.strip() for x in a.split(',') if x.strip()]:
        parts = name.split()
        if len(parts) >= 2 and re.fullmatch(r'[A-Z]{1,3}', parts[0]):
            name = ' '.join(c + '.' for c in parts[0]) + ' ' + ' '.join(parts[1:])
        out.append('<b>%s</b>' % E(name) if re.search(r'\bMoon\b', name) and name.startswith('S') else E(name))
    if len(out) > 2:
        return ', '.join(out[:-1]) + ', and ' + out[-1]
    return ' and '.join(out)


def pub_items(pubs):
    li = []
    for p in pubs:
        venue = p.get('venue_full') or p.get('venue', '')
        venue = venue.replace(' …', '').replace('…', '')
        if p.get('year') and p['year'] not in venue:
            venue += ', ' + p['year']
        doi = ' <a href="%s">%s</a>' % (E(p['url']), E(p['url'].replace('https://doi.org/', 'doi:'))) if p.get('url') else ''
        li.append('<li>%s, “%s,” <i>%s</i>.%s</li>' % (ieee_author(p.get('authors', '')), E(p['title']), E(venue), doi))
    return '\n'.join(li)


def main():
    d = json.load(open(os.path.join(ROOT, 'assets', 'publications.json'), encoding='utf-8'))
    pubs = [p for p in d['pubs'] if not p.get('hidden')]
    key = lambda p: (p.get('year') or '0000')
    J = sorted([p for p in pubs if p.get('kind') == 'journal'], key=key, reverse=True)
    C = sorted([p for p in pubs if p.get('kind') == 'conference'], key=key, reverse=True)
    logo = base64.b64encode(open(os.path.join(ROOT, 'assets', 'logo.svg'), 'rb').read()).decode()
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Sangook Moon — Curriculum Vitae</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
@page{{size:A4;margin:18mm 18mm 18mm 18mm}}
body{{font-family:"Source Serif 4",Georgia,serif;font-size:10.5pt;line-height:1.42;color:#111;margin:0}}
header{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2pt solid #111;padding-bottom:6pt;margin-bottom:10pt}}
h1{{font-size:22pt;font-weight:600;margin:0;letter-spacing:.01em}}
.ct{{text-align:right;font-size:9.5pt;line-height:1.45;white-space:nowrap;margin-left:10mm}}
h2{{font-size:11.5pt;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin:14pt 0 5pt;border-bottom:.5pt solid #999;padding-bottom:2pt}}
table{{border-collapse:collapse;width:100%}} td{{vertical-align:top;padding:1.5pt 0}} td.y{{width:30mm;white-space:nowrap;color:#333}}
ol{{margin:0;padding-left:7mm}} ol li{{margin:0 0 4pt;padding-left:1mm}}
a{{color:#1F4E9A;text-decoration:none}} .sub{{color:#333}} img.logo{{height:22pt}}
.foot{{margin-top:14pt;font-size:8.5pt;color:#666;border-top:.5pt solid #bbb;padding-top:4pt}}
</style></head><body>
<header><div><h1>Sangook Moon</h1><div class="sub">Professor, Department of Electrical and Electronic Engineering, Mokwon University</div></div>
<div class="ct">88 Doanbuk-ro, Seo-gu, Daejeon 35349, Korea<br>+82-42-829-7637 · <a href="mailto:smoon@mokwon.ac.kr">smoon@mokwon.ac.kr</a><br><a href="https://sangookmoon.github.io">sangookmoon.github.io</a> · ORCID 0000-0002-0290-1887</div></header>

<h2>Research Interests</h2>
<p style="margin:0">Hardware security; cryptographic hardware on resource-constrained SoC-FPGAs (lightweight cryptography, homomorphic encryption); real-time signal-processing hardware for the industrial Internet of Things; computer arithmetic.</p>

<h2>Education</h2>
<table>
<tr><td class="y">2002</td><td>Ph.D., Electrical and Electronic Engineering, Yonsei University, Seoul, Korea</td></tr>
<tr><td class="y">1997</td><td>M.S., Electronic Engineering, Yonsei University, Seoul, Korea</td></tr>
<tr><td class="y">1995</td><td>B.S., Electronic Engineering, Yonsei University, Seoul, Korea</td></tr>
</table>

<h2>Professional Experience</h2>
<table>
<tr><td class="y">2004 – present</td><td>Professor, Department of Electrical and Electronic Engineering, Mokwon University, Daejeon, Korea</td></tr>
<tr><td class="y">2002 – 2004</td><td>Senior Research Engineer, SK hynix, Korea — wireless communication IC design</td></tr>
</table>

<h2>Professional Service</h2>
<table>
<tr><td class="y">2027</td><td>Senior Vice President (elected), Korean Institute of Information Technology (KIIT)</td></tr>
<tr><td class="y">current</td><td>Vice President and Chair of Domestic Academic Affairs, KIIT</td></tr>
<tr><td class="y">2021 – present</td><td>Reviewer, <i>The Journal of Korean Institute of Information Technology</i></td></tr>
</table>

<h2>Teaching</h2>
<p style="margin:0">AI Robotics; FPGA Design; Digital Circuit Design; Linux Systems. Interactive course simulators: <a href="https://sangookmoon.github.io/en/teaching/">sangookmoon.github.io/en/teaching</a></p>

<h2>Journal Articles</h2>
<ol>
{pub_items(J)}
</ol>

<h2>Conference Papers</h2>
<ol>
{pub_items(C)}
</ol>

<div class="foot">Updated {TODAY.strftime('%B %Y')}. Citation metrics (Google Scholar): {d['citations']} citations, h-index {d['h']}.</div>
</body></html>
'''
    os.makedirs(os.path.join(ROOT, 'cv'), exist_ok=True)
    hp = os.path.join(ROOT, 'cv', 'Sangook_Moon_CV.html')
    open(hp, 'w', encoding='utf-8').write(doc)
    print('wrote cv/Sangook_Moon_CV.html', len(J), 'journal', len(C), 'conference')
    try:
        from playwright.sync_api import sync_playwright
        import time
        p = sync_playwright().start()
        ctx = p.chromium.connect_over_cdp('http://localhost:9222').contexts[0]
        pg = ctx.new_page()
        pg.goto('file://' + hp, wait_until='networkidle')
        time.sleep(1.5)
        c = ctx.new_cdp_session(pg)
        r = c.send('Page.printToPDF', {'paperWidth': 8.27, 'paperHeight': 11.69, 'preferCSSPageSize': True, 'printBackground': True,
                                       'displayHeaderFooter': True, 'headerTemplate': '<span></span>',
                                       'footerTemplate': '<div style="font-size:8px;width:100%;text-align:center;color:#888">Sangook Moon — CV — <span class="pageNumber"></span>/<span class="totalPages"></span></div>',
                                       'marginTop': 0.7, 'marginBottom': 0.7, 'marginLeft': 0.7, 'marginRight': 0.7})
        open(os.path.join(ROOT, 'cv', 'Sangook_Moon_CV.pdf'), 'wb').write(base64.b64decode(r['data']))
        pg.close(); p.stop()
        print('wrote cv/Sangook_Moon_CV.pdf')
    except Exception as e:
        print('PDF 를 못 만들었습니다(9222 크롬 확인):', e)


if __name__ == '__main__':
    main()

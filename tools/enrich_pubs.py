#!/usr/bin/env python3
"""assets/publications.json 의 논문마다 Crossref 에서 제목으로 찾아 DOI · 정식 학술지명 · 권호쪽을 채운다.
제목 유사도 0.92 이상만 받아들인다(틀린 논문을 붙이지 않도록). 결과는 같은 파일에 url · venue_full · kind 로 넣는다.
kind = journal | conference (Crossref type 기준, 없으면 학술지명 낱말로 추정). 원래 venue 는 그대로 둔다.
사용 : python3 tools/enrich_pubs.py
"""
import json, os, re, time, difflib, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'assets', 'publications.json')
UA = 'sangookmoon.github.io (mailto:smoon@mokwon.ac.kr)'
norm = lambda s: re.sub(r'[^a-z0-9가-힣]', '', (s or '').lower())

def crossref(title):
    q = urllib.parse.urlencode({'query.bibliographic': title, 'rows': 3, 'select': 'DOI,title,container-title,type,volume,issue,page,published,author'})
    req = urllib.request.Request('https://api.crossref.org/works?' + q, headers={'User-Agent': UA})
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(req, timeout=30))['message']['items']
        except Exception:
            time.sleep(3)
    return []

CONF_WORDS = ('proceedings', 'conference', 'symposium', 'workshop', 'icce', 'icvc', 'ccnc', 'iccce', 'iciit', 'icfice')

d = json.load(open(P, encoding='utf-8'))
hit = 0
for p in d['pubs']:
    if p.get('url'):
        continue
    best, score = None, 0
    for it in crossref(p['title']):
        t = (it.get('title') or [''])[0]
        r = difflib.SequenceMatcher(None, norm(t), norm(p['title'])).ratio()
        if r > score:
            best, score = it, r
    time.sleep(0.4)
    if best and score >= 0.92:
        hit += 1
        p['url'] = 'https://doi.org/' + best['DOI']
        ct = (best.get('container-title') or [''])[0]
        vip = ', '.join(x for x in [('vol. ' + best['volume']) if best.get('volume') else '', ('no. ' + best['issue']) if best.get('issue') else '',
                                    ('pp. ' + best['page']) if best.get('page') else ''] if x)
        yr = (best.get('published') or {}).get('date-parts', [[None]])[0][0]
        p['venue_full'] = ', '.join(x for x in [ct, vip, str(yr or p.get('year') or '')] if x)
        p['kind'] = 'conference' if best.get('type') in ('proceedings-article', 'book-chapter') or any(w in ct.lower() for w in CONF_WORDS) else 'journal'
        p['match'] = round(score, 3)
    else:
        v = (p.get('venue') or '').lower()
        p['kind'] = 'conference' if any(w in v for w in CONF_WORDS) else 'journal'
    print(('OK ' if p.get('url') else '-- ') + p['title'][:70], '|', p.get('venue_full', '')[:60])
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('DOI 찾음', hit, '/', len(d['pubs']))

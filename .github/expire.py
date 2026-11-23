"""수업자료 기간 끝 처리 : .github/expire.json 의 날짜(한국 시간)가 지난 항목의 폴더를 지우고,
<!--expire:ID--> ... <!--/expire:ID--> 로 감싼 링크 블록을 모든 html 에서 뺀다. 시뮬레이터(sim/)는 손대지 않는다.
쓰는 법 : python .github/expire.py [--dry-run] [--today YYYY-MM-DD]"""
import json, os, re, shutil, sys, datetime
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dry = '--dry-run' in sys.argv
today = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)).date()
if '--today' in sys.argv: today = datetime.date.fromisoformat(sys.argv[sys.argv.index('--today') + 1])
items = json.load(open(os.path.join(root, '.github', 'expire.json'), encoding='utf-8'))
done = []
for it in items:
    due = datetime.date.fromisoformat(it['date'])
    if today < due:
        print('wait  %s  (%s, %d일 남음)' % (it['id'], it['date'], (due - today).days)); continue
    for p in it['paths']:
        if '/sim' in p or p.startswith('sim'): print('skip sim path', p); continue
        full = os.path.join(root, p)
        if os.path.exists(full):
            print(('would remove ' if dry else 'remove ') + p)
            if not dry: shutil.rmtree(full)
    pat = re.compile(r'[ \t]*<!--expire:%s-->.*?<!--/expire:%s-->[ \t]*\n?' % (re.escape(it['id']), re.escape(it['id'])), re.S)
    for d, _, fs in os.walk(root):
        if '/.git' in d: continue
        for f in fs:
            if not f.endswith('.html'): continue
            fp = os.path.join(d, f); s = open(fp, encoding='utf-8').read(); n = pat.sub('', s)
            if n != s:
                print(('would unlink ' if dry else 'unlink ') + os.path.relpath(fp, root))
                if not dry: open(fp, 'w', encoding='utf-8').write(n)
    done.append(it['id'])
if done and not dry:
    left = [it for it in items if it['id'] not in done]
    json.dump(left, open(os.path.join(root, '.github', 'expire.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('expired', done)

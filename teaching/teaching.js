// 수업·시뮬레이터 목록을 /teaching/sims.json 에서 그린다. 시뮬레이터를 추가할 때는
//   ① HTML 파일을 teaching/<과목>/sim/ 에 넣고  ② sims.json 의 "sims" 에 한 줄 더하면 된다.
//      영문 페이지용으로 title_en · week_en · desc_en 도 넣는다(없으면 한글을 대신 보여 준다).
// courseId 가 null 이면 전체(과목별 묶음), 있으면 그 과목만. lang 은 'ko'(기본) 또는 'en'.
// 시뮬레이터 파일은 한 곳(/teaching/<과목>/sim/)에만 두고 한글·영문 페이지가 같이 가리킨다.
function renderTeaching(courseId, lang) {
  lang = lang || 'ko';
  const en = lang === 'en';
  const pick = (o, k) => (en && o[k + '_en']) ? o[k + '_en'] : o[k];
  const esc = s => String(s || '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const T = en ? {open: 'Open →', none: 'No simulators yet.', ko: ' (Korean interface)'} : {open: '열기 →', none: '아직 올린 시뮬레이터가 없습니다.', ko: ''};
  fetch('/teaching/sims.json').then(r => r.json()).then(d => {
    const box = document.getElementById('courses');
    const courses = d.courses.filter(c => !courseId || c.id === courseId);
    let html = '';
    for (const c of courses) {
      const sims = d.sims.filter(s => s.course === c.id).sort((a, b) => (b.added || '').localeCompare(a.added || ''));
      const title = en ? esc(c.en) : esc(c.name) + ' <span style="font-weight:500;color:var(--muted);font-size:15px">' + esc(c.en) + '</span>';
      const head = courseId ? '' : '<h2><a href="' + c.id + '/" style="color:inherit;text-decoration:none">' + title +
        '</a></h2><p class="note">' + esc(pick(c, 'desc')) + '</p>';
      html += head + '<div class="cards">';
      for (const s of sims) {
        const href = '/teaching/' + c.id + '/sim/' + s.file;
        html += '<a class="card" href="' + href + '"><b>' + esc(pick(s, 'title')) + '</b><span>' + esc(pick(s, 'week')) + T.ko +
          '</span><span style="margin-top:6px">' + esc(pick(s, 'desc')) + '</span><div class="go">' + T.open + '</div></a>';
      }
      if (!sims.length) html += '<p class="note">' + T.none + '</p>';
      html += '</div>';
    }
    box.innerHTML = html;
  });
}

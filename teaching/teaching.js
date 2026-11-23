// 수업·시뮬레이터 목록을 /teaching/sims.json 에서 그린다. 시뮬레이터를 추가할 때는
//   ① HTML 파일을 teaching/<과목>/sim/ 에 넣고  ② sims.json 의 "sims" 에 한 줄 더하면 된다.
//      영문 페이지용으로 title_en · week_en · desc_en 도 넣는다(없으면 한글을 대신 보여 준다).
//      고치는 중이면 "status": "수정 중", "status_en": "Being revised" 를 넣으면 제목 옆에 꼬리표가 붙는다.
//      미리보기 그림은 같은 폴더의 <파일이름>-og.png (1200×630) 를 쓴다. 없으면 그림 칸만 빠진다.
// courseId 가 null 이면 전체(과목별 묶음), 있으면 그 과목만. lang 은 'ko'(기본) 또는 'en'.
// 시뮬레이터 파일은 한 곳(/teaching/<과목>/sim/)에만 두고 한글·영문 페이지가 같이 가리킨다.
function renderTeaching(courseId, lang) {
  lang = lang || 'ko';
  const en = lang === 'en';
  const pick = (o, k) => (en && o[k + '_en']) ? o[k + '_en'] : o[k];
  const esc = s => String(s || '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const T = en ? {none: 'No simulators yet.', ko: ' · Korean interface'} : {none: '아직 올린 시뮬레이터가 없습니다.', ko: ''};
  const coursePage = id => (en ? '/en' : '') + '/teaching/' + id + '/';
  fetch('/teaching/sims.json').then(r => r.json()).then(d => {
    const box = document.getElementById('courses');
    const courses = d.courses.filter(c => !courseId || c.id === courseId);
    let html = '';
    for (const c of courses) {
      const sims = d.sims.filter(s => s.course === c.id).sort((a, b) => (b.added || '').localeCompare(a.added || ''));
      if (!courseId) {
        const title = en ? esc(c.en) : esc(c.name);
        html += '<h2><a href="' + coursePage(c.id) + '" style="color:inherit;text-decoration:none">' + title + '</a></h2><p class="note">' + esc(pick(c, 'desc')) + '</p>';
      }
      html += '<div class="sims">';
      for (const s of sims) {
        const href = '/teaching/' + c.id + '/sim/' + s.file;
        const img = href.replace(/\.html$/, '-og.png');
        const title = pick(s, 'title'), week = pick(s, 'week');
        const wk = (week && week !== title) ? esc(week) + T.ko : T.ko.replace(/^ · /, '');
        html += '<a class="sim" href="' + href + '"><img src="' + img + '" alt="" loading="lazy" onerror="this.remove()">' +
          '<span><b>' + esc(title) + (s.status ? ' <i class="st">' + esc(pick(s, 'status')) + '</i>' : '') + '</b>' + (wk ? '<span class="wk">' + wk + '</span>' : '') +
          '<span class="ds">' + esc(pick(s, 'desc')) + '</span></span></a>';
      }
      if (!sims.length) html += '<p class="note">' + T.none + '</p>';
      html += '</div>';
    }
    box.innerHTML = html;
  });
}

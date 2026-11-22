// 수업·시뮬레이터 목록을 sims.json 에서 그린다. 시뮬레이터를 추가할 때는
//   ① HTML 파일을 teaching/<과목>/sim/ 에 넣고  ② sims.json 의 "sims" 에 한 줄 더하면 된다.
// courseId 가 null 이면 전체(과목별 묶음), 있으면 그 과목만.
function renderTeaching(courseId) {
  const base = courseId ? '../' : './';
  const esc = s => String(s || '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  fetch(base + 'sims.json').then(r => r.json()).then(d => {
    const box = document.getElementById('courses');
    const courses = d.courses.filter(c => !courseId || c.id === courseId);
    let html = '';
    for (const c of courses) {
      const sims = d.sims.filter(s => s.course === c.id).sort((a, b) => (b.added || '').localeCompare(a.added || ''));
      const head = courseId ? '' : '<h2><a href="' + c.id + '/" style="color:inherit;text-decoration:none">' + esc(c.name) +
        ' <span style="font-weight:500;color:var(--muted);font-size:15px">' + esc(c.en) + '</span></a></h2><p class="note">' + esc(c.desc) + '</p>';
      html += head + '<div class="cards">';
      for (const s of sims) {
        const href = (courseId ? '' : c.id + '/') + 'sim/' + s.file;
        html += '<a class="card" href="' + href + '"><b>' + esc(s.title) + '</b><span>' + esc(s.week) + '</span><span style="margin-top:6px">' +
          esc(s.desc) + '</span><div class="go">열기 →</div></a>';
      }
      if (!sims.length) html += '<p class="note">아직 올린 시뮬레이터가 없습니다.</p>';
      html += '</div>';
    }
    box.innerHTML = html;
  });
}

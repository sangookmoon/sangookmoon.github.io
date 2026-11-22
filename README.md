# sangookmoon.github.io

문상국(Sangook Moon), 목원대학교 전기전자공학과 홈페이지.

- 시뮬레이터 추가: HTML 파일을 `teaching/<과목>/sim/` 에 넣고 `teaching/sims.json` 의 `sims` 에 한 줄 추가. 영문 페이지용 `title_en`·`week_en`·`desc_en` 도 함께(없으면 영문 페이지에 한글이 보임).
- 영문본: `en/` 아래(소개·논문·수업). 시뮬레이터 파일은 한 곳(`teaching/<과목>/sim/`)만 두고 한글·영문 페이지가 같이 가리킨다.
- 새 과목은 한글 `teaching/<id>/index.html` 과 영문 `en/teaching/<id>/index.html` 둘 다 만들고, `sims.json` 의 `courses` 에 `desc_en` 도 넣는다.
- 논문 목록: `assets/publications.json` (Google Scholar 에서 갱신).

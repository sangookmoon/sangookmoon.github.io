# sangookmoon.github.io

문상국(Sangook Moon), 목원대학교 전기전자공학과 홈페이지.

- 시뮬레이터 추가: HTML 파일을 `teaching/<과목>/sim/` 에 넣고 `teaching/sims.json` 의 `sims` 에 한 줄 추가. 영문 페이지용 `title_en`·`week_en`·`desc_en` 도 함께(없으면 영문 페이지에 한글이 보임).
- 영문본: `en/` 아래(소개·논문·수업). 시뮬레이터 파일은 한 곳(`teaching/<과목>/sim/`)만 두고 한글·영문 페이지가 같이 가리킨다.
- 새 과목은 한글 `teaching/<id>/index.html` 과 영문 `en/teaching/<id>/index.html` 둘 다 만들고, `sims.json` 의 `courses` 에 `desc_en` 도 넣는다.
- 논문 목록: `assets/publications.json` (Google Scholar 에서 갱신).
- **페이지는 손으로 고치지 않는다** : `python3 tools/build_pages.py` 가 한·영 10개 페이지(머리글·꼬리말·글꼴 공통)를 만든다. 문구를 바꾸려면 이 스크립트를 고친 뒤 다시 돌린다.
- CV : `python3 tools/build_cv.py` → 영문 `cv/Sangook_Moon_CV.pdf` · 한글 `cv/Sangook_Moon_CV_ko.pdf` (9222 디버그 크롬 필요). 논문은 `assets/publications.json` 에서.
- 논문 DOI·정식 학술지명 : `python3 tools/enrich_pubs.py` (Crossref, 제목 유사도 0.92 이상만).
- 시뮬레이터 이용 조건 : CC BY-NC-ND 4.0 (그대로 쓰는 것은 자유, 고치거나 다시 올리려면 허락).

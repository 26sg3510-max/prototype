import streamlit as st
import random
import math
import json

st.set_page_config(
    page_title="학급 자리 배치기",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────────────────────
# CSS
# ────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&family=JetBrains+Mono:wght@700&display=swap');

/* ══ 전체 폰트 ══════════════════════════════════════════════════════════════ */
*, *::before, *::after {
    font-family: 'Noto Sans KR', sans-serif !important;
    box-sizing: border-box;
}

/* ══ keyboard hint / tooltip 완전 제거 ════════════════════════════════════
   number_input 하단에 나타나는 "Use keyboard arrows" 회색 텍스트 숨김     */
[data-testid="stNumberInput"] ~ small,
[data-testid="stNumberInput"] + div > small,
[data-testid="InputInstructions"],
[data-testid="stTooltipHoverTarget"],
[data-testid="stTooltipContent"],
.st-emotion-cache-1gulkj5,   /* 버전별 동적 클래스 대응 */
small.st-emotion-cache-1gulkj5 {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}
/* stNumberInput 컨테이너 직하위 small 태그 전부 숨김 */
[data-testid="stNumberInput"] small,
[data-testid="stNumberInput"] > div > small,
[data-testid="stNumberInput"] > div > div > small {
    display: none !important;
}

/* ══ 위젯 라벨 ════════════════════════════════════════════════════════════ */
[data-testid="stWidgetLabel"] {
    min-height: 0 !important;
    margin-bottom: 4px !important;
}
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    font-size: 13px !important;
    font-weight: 700 !important;
    line-height: 1.3 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: block !important;
}

/* ══ number_input ═════════════════════════════════════════════════════════ */
[data-testid="stNumberInput"] {
    margin-bottom: 2px !important;
}
[data-testid="stNumberInput"] > div {
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
    gap: 4px !important;
    height: 42px !important;
}
[data-testid="stNumberInput"] input {
    flex: 1 1 0% !important;
    min-width: 0 !important;
    height: 42px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border-width: 2px !important;
    padding: 0 8px !important;
    text-align: center !important;
}
[data-testid="stNumberInput"] button {
    flex-shrink: 0 !important;
    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;
    border-radius: 8px !important;
    border-width: 2px !important;
    font-size: 22px !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: all .12s ease !important;
}
[data-testid="stNumberInput"] button svg {
    width: 16px !important;
    height: 16px !important;
    stroke-width: 3 !important;
    display: block !important;
}

/* ══ text_input ═══════════════════════════════════════════════════════════ */
[data-testid="stTextInput"] input {
    height: 44px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border-width: 2px !important;
    padding: 0 12px !important;
}

/* ══ 섹션 헤더 ════════════════════════════════════════════════════════════ */
.sec-head {
    display: block;
    font-size: 10px !important;
    font-weight: 800 !important;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin: 8px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1.5px solid currentColor;
    opacity: .5;
}

/* ══ 배지 ═════════════════════════════════════════════════════════════════ */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 12px !important;
    font-weight: 800 !important;
    margin-right: 3px;
    border: 1.5px solid;
    line-height: 1.7;
    white-space: nowrap;
}

/* ══ 태그 ═════════════════════════════════════════════════════════════════ */
.tag-wrap { display: flex; flex-wrap: wrap; gap: 5px; margin: 7px 0 4px; }
.tag {
    display: inline-flex; align-items: center;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px !important; font-weight: 800 !important;
    border: 1.5px solid;
    white-space: nowrap;
    line-height: 1.4;
}

/* ══ 자리 그리드 공통 ═══════════════════════════════════════════════════ */
.classroom-wrap {
    display: flex; flex-direction: column; align-items: center;
    padding: 20px 8px;
    overflow-x: auto;           /* 모바일: 가로 스크롤 */
    width: 100%;
}
.blackboard {
    border-width: 2.5px; border-style: solid; border-radius: 12px;
    text-align: center; padding: 10px 56px;
    font-size: 13px; font-weight: 800; letter-spacing: .18em;
    margin-bottom: 24px; width: fit-content; white-space: nowrap;
}
.seat-grid { display: flex; flex-direction: column; gap: 8px; }
.seat-row  { display: flex; gap: 8px; justify-content: center; flex-wrap: nowrap; }
.seat {
    width: 64px; height: 64px; border-radius: 11px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 21px; font-weight: 700;
    border: 2px solid transparent;
    position: relative; flex-shrink: 0;
    transition: transform .12s ease, box-shadow .12s ease;
    cursor: default; user-select: none;
    -webkit-tap-highlight-color: transparent;
}
.seat:hover { transform: translateY(-3px); z-index: 1; }
.seat-label {
    position: absolute; bottom: 4px;
    font-size: 8.5px; font-weight: 700;
    font-family: 'Noto Sans KR', sans-serif;
    line-height: 1; letter-spacing: .03em; white-space: nowrap;
}

/* ══ 번호순 목록: 단일 테이블 (겹침 완전 제거) ══════════════════════════ */
.list-wrap {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}
.list-table {
    width: 100%; border-collapse: collapse;
    font-size: 13px; line-height: 1.6;
}
.list-table th {
    padding: 5px 10px 7px;
    font-size: 11px !important; font-weight: 800 !important;
    letter-spacing: .07em; text-align: left;
    border-bottom: 1.5px solid currentColor;
    opacity: .5; white-space: nowrap;
}
.list-table td {
    padding: 6px 10px;
    font-size: 13px !important;
    white-space: nowrap;
    border-bottom: 1px solid transparent;
}
.list-table tbody tr:last-child td { border-bottom: none; }
.num-cell   { font-weight: 700 !important; }
.loc-cell   { opacity: .65; }
.pin-badge  {
    display: inline-block;
    font-size: 11px !important; font-weight: 800 !important;
    padding: 1px 7px; border-radius: 5px;
}

/* ══ 안내화면 ════════════════════════════════════════════════════════════ */
.empty-state {
    text-align: center; padding: 60px 24px;
    border: 2px dashed; border-radius: 18px;
}
.e-icon  { font-size: 46px; margin-bottom: 12px; }
.e-title { font-size: 1.05rem; font-weight: 800; margin-bottom: 8px; }
.e-sub   { font-size: .86rem; line-height: 1.85; opacity: .6; }

/* ══ 헬프 카드 ═══════════════════════════════════════════════════════════ */
.help-card { border: 1.5px solid; border-radius: 14px; padding: 18px; }
.h-icon    { font-size: 1.6rem; margin-bottom: 7px; }
.h-title   { font-size: .9rem; font-weight: 800; margin-bottom: 5px; }
.h-desc    { font-size: .8rem; line-height: 1.6; opacity: .6; }

/* ══ 모바일 특화 ═══════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .seat { width: 52px; height: 52px; font-size: 17px; border-radius: 9px; }
    .seat-label { font-size: 7.5px; }
    .blackboard { padding: 8px 24px; font-size: 12px; }
    .list-table td, .list-table th { padding: 5px 7px; }
}

/* ══════════════════════════════════════════════════════════════════════════
   라이트 모드
══════════════════════════════════════════════════════════════════════════ */
@media (prefers-color-scheme: light) {
    .badge.b-blue   { background:#dbeafe; color:#1d4ed8; border-color:#93c5fd; }
    .badge.b-purple { background:#ede9fe; color:#5b21b6; border-color:#c4b5fd; }
    .badge.b-green  { background:#dcfce7; color:#15803d; border-color:#86efac; }
    .tag-excl  { background:#fee2e2; border-color:#fca5a5; color:#991b1b; }
    .tag-fixed { background:#dbeafe; border-color:#93c5fd; color:#1e40af; }
    .blackboard { background:linear-gradient(135deg,#14532d,#166534); border-color:#16a34a; color:#bbf7d0; }
    .seat-normal { background:#fff; border-color:#c8d3e0; color:#1e293b;
                   box-shadow:0 1px 4px rgba(0,0,0,.09); }
    .seat-fixed  { background:#dbeafe; border-color:#2563eb; color:#1d4ed8;
                   box-shadow:0 0 0 3px rgba(37,99,235,.12); }
    .seat-empty  { background:#f8fafc; border-color:#dde3ec; border-style:dashed; color:#dde3ec; }
    .seat-label  { color:rgba(15,23,42,.3); }
    .seat-fixed .seat-label { color:rgba(29,78,216,.45); }
    .pin-badge   { background:#dbeafe; color:#1d4ed8; }
    .list-table tbody tr:hover td { background: #f8fafc; }
    .empty-state { border-color:#c8d3e0; background:#fff; }
    .help-card   { background:#fff; border-color:#dde3ec;
                   box-shadow:0 1px 4px rgba(0,0,0,.06); }
    .list-table td { color: #1e293b; }
    .list-table th { color: #475569; }
}

/* ══════════════════════════════════════════════════════════════════════════
   다크 모드  — 대비 대폭 강화
══════════════════════════════════════════════════════════════════════════ */
@media (prefers-color-scheme: dark) {
    /* 배지 */
    .badge.b-blue   { background:#1a3560; color:#93c5fd; border-color:#2d5a9e; }
    .badge.b-purple { background:#2a1854; color:#d8b4fe; border-color:#5b3a9e; }
    .badge.b-green  { background:#052e16; color:#6ee7b7; border-color:#065f46; }
    /* 태그 */
    .tag-excl  { background:#4a0a0a; border-color:#f87171; color:#fca5a5; }
    .tag-fixed { background:#1a3560; border-color:#60a5fa; color:#bfdbfe; }
    /* 칠판 */
    .blackboard { background:linear-gradient(135deg,#14532d,#0a2e18);
                  border-color:#22c55e; color:#86efac; }
    /* 자리 */
    .seat-normal { background:#1e2d45; border-color:#3a5070; color:#e8eef6;
                   box-shadow:0 2px 8px rgba(0,0,0,.5); }
    .seat-fixed  { background:#12305e; border-color:#60a5fa; color:#bfdbfe;
                   box-shadow:0 0 0 3px rgba(96,165,250,.25); }
    .seat-empty  { background:#0f1825; border-color:#1e2d3d; border-style:dashed; color:#1e2d3d; }
    .seat-label  { color:rgba(232,238,246,.3); }
    .seat-fixed .seat-label { color:rgba(191,219,254,.45); }
    /* 목록 */
    .pin-badge  { background:#1a3560; color:#93c5fd; }
    .list-table td   { color: #e2e8f0 !important; }
    .list-table th   { color: #94a3b8 !important; border-bottom-color: #334155; }
    .list-table tbody tr:hover td { background: #1e2d45; }
    .list-table tbody tr td { border-bottom-color: #1e2836; }
    /* 안내화면 */
    .empty-state { border-color:#2a3f5a; background:#131e30; }
    .e-title { color: #e2e8f0; }
    /* 헬프 카드 */
    .help-card { background:#131e30; border-color:#2a3f5a;
                 box-shadow:0 2px 10px rgba(0,0,0,.4); }
    .h-title { color: #e2e8f0; }
    .h-desc  { color: #94a3b8; opacity: 1 !important; }
}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# 상태 초기화
# ────────────────────────────────────────────────────────────────────────────
for _k, _v in {
    "total": 30, "cols": 6,
    "excluded": [], "fixed": {},
    "result": None, "history": [],
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v
S = st.session_state


# ────────────────────────────────────────────────────────────────────────────
# 헬퍼
# ────────────────────────────────────────────────────────────────────────────
def parse_numbers(text: str, max_n: int) -> list:
    nums = []
    for tok in text.replace(",", " ").replace("\n", " ").split():
        try:
            n = int(tok)
            if 1 <= n <= max_n:
                nums.append(n)
        except ValueError:
            pass
    return sorted(set(nums))


def arrange():
    n_total = S["total"]; cols = S["cols"]
    rows = math.ceil(n_total / cols); seats = rows * cols
    excluded = set(S["excluded"]); fixed = dict(S["fixed"])
    active = [i for i in range(1, n_total + 1) if i not in excluded]
    for num in list(fixed.keys()):
        if num not in active or fixed[num] >= seats:
            del fixed[num]
    S["fixed"] = fixed
    assigned   = {sidx: num for num, sidx in fixed.items()}
    free_nums  = [n for n in active if n not in fixed]
    free_seats = [s for s in range(seats) if s not in assigned]
    random.shuffle(free_nums)
    for i, num in enumerate(free_nums):
        if i < len(free_seats):
            assigned[free_seats[i]] = num
    S["result"] = assigned
    S["history"].insert(0, dict(assigned))
    if len(S["history"]) > 5:
        S["history"] = S["history"][:5]


# ────────────────────────────────────────────────────────────────────────────
# 사이드바
# ────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    st.markdown("---")

    # ── 기본 설정 ──
    st.markdown('<span class="sec-head">기본 설정</span>', unsafe_allow_html=True)

    # 모바일 대응: 한 줄에 두 위젯 배치
    c1, c2 = st.columns(2)
    with c1:
        S["total"] = st.number_input(
            "학생 수", min_value=1, max_value=60,
            value=S["total"], step=1, key="ni_total",
        )
    with c2:
        S["cols"] = st.number_input(
            "열 수", min_value=1, max_value=12,
            value=S["cols"], step=1, key="ni_cols",
        )

    rows_calc = math.ceil(S["total"] / S["cols"])
    st.markdown(
        f'<div style="margin:8px 0 4px">'
        f'<span class="badge b-blue">{S["cols"]}열</span>'
        f'<span class="badge b-purple">{rows_calc}행</span>'
        f'<span class="badge b-green">{S["total"]}명</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── 제외 번호 ──
    st.markdown('<span class="sec-head">🚫 제외할 번호</span>', unsafe_allow_html=True)
    excl_input = st.text_input(
        "제외 번호",
        key="excl_input",
        placeholder="예: 1, 5, 12  (콤마·공백 구분)",
        label_visibility="collapsed",
    )
    if st.button("➕ 추가", key="btn_excl", use_container_width=True):
        for n in parse_numbers(excl_input, S["total"]):
            if n not in S["excluded"]:
                S["excluded"].append(n)
            S["fixed"].pop(n, None)
        S["excluded"].sort()
        st.rerun()

    if S["excluded"]:
        tags = "".join(
            f'<span class="tag tag-excl">✕ {n}번</span>' for n in S["excluded"]
        )
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("🗑 전체 초기화", key="btn_excl_clr", use_container_width=True):
            S["excluded"] = []
            st.rerun()
    st.markdown("---")

    # ── 자리 고정 ──
    st.markdown('<span class="sec-head">📌 자리 고정</span>', unsafe_allow_html=True)

    # 모바일 대응: 한 줄 2열 + 아래 1열
    g1, g2 = st.columns(2)
    with g1:
        fix_num = st.number_input("번호", 1, S["total"], 1, key="fix_num")
    with g2:
        fix_row = st.number_input("행", 1, rows_calc, 1, key="fix_row")
    fix_col = st.number_input("열", 1, S["cols"], 1, key="fix_col")

    if st.button("📌 고정 추가", key="btn_fix", use_container_width=True):
        sidx = (fix_row - 1) * S["cols"] + (fix_col - 1)
        S["fixed"] = {k: v for k, v in S["fixed"].items() if v != sidx}
        S["fixed"][fix_num] = sidx
        if fix_num in S["excluded"]:
            S["excluded"].remove(fix_num)
        st.rerun()

    if S["fixed"]:
        tags = "".join(
            f'<span class="tag tag-fixed">'
            f'📌 {num}번→{sidx//S["cols"]+1}행{sidx%S["cols"]+1}열'
            f'</span>'
            for num, sidx in sorted(S["fixed"].items())
        )
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("🗑 고정 전체 초기화", key="btn_fix_clr", use_container_width=True):
            S["fixed"] = {}
            st.rerun()
    st.markdown("---")

    # ── JSON 저장 ──
    if S["result"]:
        cfg_data = {
            "total": S["total"], "cols": S["cols"],
            "excluded": S["excluded"],
            "fixed": {str(k): v for k, v in S["fixed"].items()},
        }
        st.download_button(
            "⬇ 설정 저장 (JSON)",
            data=json.dumps(cfg_data, ensure_ascii=False, indent=2),
            file_name="seating_config.json",
            mime="application/json",
            use_container_width=True,
        )


# ────────────────────────────────────────────────────────────────────────────
# 메인
# ────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;font-size:1.85rem;font-weight:900;"
    "letter-spacing:-.02em;margin-bottom:3px'>🏫 학급 자리 배치기</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;font-size:.86rem;margin-bottom:16px;opacity:.5'>"
    "무작위 배치 · 번호 고정 · 제외 설정</p>",
    unsafe_allow_html=True,
)

b1, b2, b3 = st.columns([3, 2, 2])
with b1:
    if st.button("🎲 자리 배치하기", type="primary", use_container_width=True):
        arrange(); st.rerun()
with b2:
    if st.button("🔄 결과 초기화", use_container_width=True):
        S["result"] = None; st.rerun()
with b3:
    if st.button("↩ 이전 결과", use_container_width=True,
                 disabled=len(S["history"]) <= 1):
        S["history"].pop(0)
        S["result"] = S["history"][0] if S["history"] else None
        st.rerun()

st.markdown("---")


# ────────────────────────────────────────────────────────────────────────────
# 자리 그리드
# ────────────────────────────────────────────────────────────────────────────
if S["result"] is not None:
    result      = S["result"]
    cols_n      = S["cols"]
    rows_n      = math.ceil(S["total"] / cols_n)
    fixed_seats = set(S["fixed"].values())

    grid = '<div class="classroom-wrap">'
    grid += '<div class="blackboard">📋 &nbsp; 칠 판 &nbsp; ( 앞 )</div>'
    grid += '<div class="seat-grid">'
    for r in range(rows_n):
        grid += '<div class="seat-row">'
        for c in range(cols_n):
            idx = r * cols_n + c
            num = result.get(idx)
            if num is None:
                grid += (
                    f'<div class="seat seat-empty">'
                    f'<span style="opacity:.25;font-size:15px">—</span>'
                    f'<span class="seat-label">{r+1}행{c+1}열</span></div>'
                )
            elif idx in fixed_seats:
                grid += (
                    f'<div class="seat seat-fixed" title="{num}번 고정">'
                    f'{num}<span class="seat-label">📌고정</span></div>'
                )
            else:
                grid += (
                    f'<div class="seat seat-normal" title="{num}번 | {r+1}행{c+1}열">'
                    f'{num}<span class="seat-label">{r+1}행{c+1}열</span></div>'
                )
        grid += '</div>'
    grid += '</div></div>'

    st.markdown(
        f'<div style="display:flex;justify-content:center;overflow-x:auto">{grid}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── 통계 ──
    active_cnt = sum(1 for v in result.values() if v is not None)
    for col, label, val in zip(
        st.columns(4),
        ["총 학생 수", "배치된 학생", "제외된 학생", "고정된 자리"],
        [f"{S['total']}명", f"{active_cnt}명",
         f"{len(S['excluded'])}명", f"{len(S['fixed'])}개"],
    ):
        col.metric(label, val)

    # ── 번호순 목록 ──
    # st.columns + st.markdown 반복을 완전히 없애고
    # 단일 HTML 블록으로 렌더링 → 글자 겹침 원천 제거
    with st.expander("📋 번호순 자리 목록 보기"):
        table = sorted(
            [(num, sidx // cols_n + 1, sidx % cols_n + 1, sidx in fixed_seats)
             for sidx, num in result.items()],
            key=lambda x: x[0],
        )

        # 3열 HTML 테이블을 하나의 <table>로 합침
        chunk = math.ceil(len(table) / 3)
        g = [table[i*chunk:(i+1)*chunk] for i in range(3)]
        # 행 수 통일
        max_rows = max(len(x) for x in g)
        for x in g:
            while len(x) < max_rows:
                x.append(None)

        def cell(item):
            if item is None:
                return "<td></td><td></td><td></td>"
            num, r, c, is_fixed = item
            pin = '<span class="pin-badge">📌</span>' if is_fixed else ""
            return (
                f'<td class="num-cell">{num}번</td>'
                f'<td class="loc-cell">{r}행 {c}열</td>'
                f'<td>{pin}</td>'
            )

        header = (
            "<thead><tr>"
            "<th>번호</th><th>위치</th><th></th>"
            "<th style='width:24px'></th>"   # 열 구분 여백
            "<th>번호</th><th>위치</th><th></th>"
            "<th style='width:24px'></th>"
            "<th>번호</th><th>위치</th><th></th>"
            "</tr></thead>"
        )
        rows_html = ""
        for i in range(max_rows):
            sep = "<td style='width:24px'></td>"
            rows_html += (
                f"<tr>{cell(g[0][i])}{sep}{cell(g[1][i])}{sep}{cell(g[2][i])}</tr>"
            )

        st.markdown(
            f'<div class="list-wrap">'
            f'<table class="list-table">{header}'
            f'<tbody>{rows_html}</tbody></table>'
            f'</div>',
            unsafe_allow_html=True,
        )

else:
    # ── 안내 화면 ──
    st.markdown("""
    <div class="empty-state">
        <div class="e-icon">🪑</div>
        <div class="e-title">아직 자리가 배치되지 않았습니다</div>
        <div class="e-sub">왼쪽 사이드바에서 설정을 마친 후<br>
        <b>🎲 자리 배치하기</b> 버튼을 눌러주세요</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    for col_ui, (icon, title, desc) in zip(st.columns(3), [
        ("🔢", "인원 설정",  "학생 수와 가로 열 수를 입력하면 행 수가 자동 계산됩니다."),
        ("🚫", "번호 제외",  "결석·전학 등 배치에서 빠져야 할 번호를 추가합니다."),
        ("📌", "자리 고정",  "특정 번호를 원하는 행·열 위치에 고정 배치합니다."),
    ]):
        with col_ui:
            st.markdown(
                f'<div class="help-card">'
                f'<div class="h-icon">{icon}</div>'
                f'<div class="h-title">{title}</div>'
                f'<div class="h-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

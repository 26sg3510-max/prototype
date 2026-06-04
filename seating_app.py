import streamlit as st
import random
import math
import json

st.set_page_config(page_title="학급 자리 배치기", page_icon="🏫", layout="wide")

# ────────────────────────────────────────────────────────────────────────────
# CSS
# ────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&family=JetBrains+Mono:wght@700&display=swap');

html, body, [class*="st-"], button, input, select, textarea {
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* ── number_input 래퍼: 높이 고정으로 겹침 방지 ── */
[data-testid="stNumberInput"] {
    min-height: 0 !important;
}
[data-testid="stNumberInput"] > div {
    display: flex !important;
    align-items: center !important;
    gap: 4px !important;
}
[data-testid="stNumberInput"] input {
    font-size: 15px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border-width: 2px !important;
    height: 40px !important;
    padding: 0 10px !important;
    min-width: 0 !important;
    flex: 1 !important;
}
/* +/- 버튼 */
[data-testid="stNumberInput"] button {
    font-family: 'Noto Sans KR', Arial, sans-serif !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    flex-shrink: 0 !important;
    border-radius: 8px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background .12s, color .12s !important;
}
[data-testid="stNumberInput"] button svg {
    width: 16px !important;
    height: 16px !important;
    stroke-width: 3px !important;
    pointer-events: none !important;
}

/* ── 텍스트 입력 ── */
[data-testid="stTextInput"] input {
    font-size: 14px !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border-width: 2px !important;
    height: 40px !important;
}

/* ── 위젯 라벨 — 정확한 크기 지정으로 겹침 방지 ── */
[data-testid="stWidgetLabel"] {
    line-height: 1.4 !important;
    margin-bottom: 4px !important;
    display: block !important;
}
[data-testid="stWidgetLabel"] p {
    font-size: 13px !important;
    font-weight: 700 !important;
    line-height: 1.4 !important;
    margin: 0 0 4px 0 !important;
    padding: 0 !important;
}

/* ── 섹션 헤더 ── */
.sec-head {
    display: block;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
    opacity: .55;
    margin: 4px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1.5px solid currentColor;
}

/* ── 배지 ── */
.badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    margin-right: 4px;
    border: 1.5px solid;
    line-height: 1.6;
}

/* ── 태그 ── */
.tag-wrap { display: flex; flex-wrap: wrap; gap: 5px; margin: 6px 0; }
.tag {
    display: inline-flex;
    align-items: center;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    border: 1.5px solid;
    line-height: 1.5;
    white-space: nowrap;
}

/* ── 자리 그리드 ── */
.classroom-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 12px;
}
.blackboard {
    border-width: 2.5px;
    border-style: solid;
    border-radius: 12px;
    text-align: center;
    padding: 10px 64px;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: .18em;
    margin-bottom: 28px;
    width: fit-content;
}
.seat-grid { display: flex; flex-direction: column; gap: 9px; }
.seat-row  { display: flex; gap: 9px; justify-content: center; }
.seat {
    width: 66px; height: 66px;
    border-radius: 12px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px; font-weight: 700;
    border: 2px solid transparent;
    position: relative;
    transition: transform .13s ease, box-shadow .13s ease;
    cursor: default; user-select: none;
}
.seat:hover { transform: translateY(-3px); z-index: 1; }
.seat-label {
    position: absolute; bottom: 4px;
    font-size: 9px; font-weight: 700;
    font-family: 'Noto Sans KR', sans-serif;
    line-height: 1; letter-spacing: .03em;
    white-space: nowrap;
}

/* ── 목록 테이블 ── */
.list-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    line-height: 1.5;
    table-layout: fixed;
}
.list-table th {
    padding: 4px 8px 6px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .06em;
    text-align: left;
    opacity: .5;
    border-bottom: 1.5px solid currentColor;
}
.list-table td {
    padding: 5px 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.list-table tr:hover td { opacity: .8; }
.pin-badge {
    display: inline-block;
    font-size: 10px; font-weight: 800;
    padding: 1px 6px; border-radius: 4px;
}

/* ── 안내화면 ── */
.empty-state {
    text-align: center;
    padding: 64px 28px;
    border: 2px dashed;
    border-radius: 20px;
}
.empty-state .e-icon  { font-size: 48px; margin-bottom: 12px; }
.empty-state .e-title { font-size: 1.1rem; font-weight: 800; margin-bottom: 8px; }
.empty-state .e-sub   { font-size: .88rem; line-height: 1.8; opacity: .65; }

/* ── 헬프 카드 ── */
.help-card {
    border: 1.5px solid;
    border-radius: 14px;
    padding: 20px;
    height: 100%;
}
.help-card .h-icon  { font-size: 1.7rem; margin-bottom: 8px; }
.help-card .h-title { font-size: .93rem; font-weight: 800; margin-bottom: 6px; }
.help-card .h-desc  { font-size: .82rem; line-height: 1.65; opacity: .65; }

/* ══════════════ 라이트 모드 ══════════════ */
@media (prefers-color-scheme: light) {
    .badge.b-blue   { background:#dbeafe; color:#1d4ed8; border-color:#93c5fd; }
    .badge.b-purple { background:#ede9fe; color:#5b21b6; border-color:#c4b5fd; }
    .badge.b-green  { background:#dcfce7; color:#15803d; border-color:#86efac; }
    .tag-excl       { background:#fee2e2; border-color:#fca5a5; color:#991b1b; }
    .tag-fixed      { background:#dbeafe; border-color:#93c5fd; color:#1e40af; }
    .blackboard     { background:linear-gradient(135deg,#14532d,#166534); border-color:#16a34a; color:#bbf7d0; }
    .seat-normal    { background:#fff;    border-color:#cbd5e1; color:#1e293b; box-shadow:0 1px 4px rgba(0,0,0,.08); }
    .seat-fixed     { background:#dbeafe; border-color:#2563eb; color:#1d4ed8; box-shadow:0 0 0 3px #dbeafe80; }
    .seat-empty     { background:#f8fafc; border-color:#e2e8f0; border-style:dashed; color:#e2e8f0; }
    .seat-label     { color:rgba(15,23,42,.32); }
    .pin-badge      { background:#dbeafe; color:#1d4ed8; }
    .empty-state    { border-color:#cbd5e1; background:#fff; }
    .help-card      { background:#fff; border-color:#e2e8f0; box-shadow:0 1px 4px rgba(0,0,0,.07); }
}

/* ══════════════ 다크 모드 ══════════════ */
@media (prefers-color-scheme: dark) {
    .badge.b-blue   { background:#1e3a5f; color:#93c5fd; border-color:#3b6ea8; }
    .badge.b-purple { background:#2e1f5e; color:#d8b4fe; border-color:#6d4fc4; }
    .badge.b-green  { background:#052e16; color:#86efac; border-color:#166534; }
    .tag-excl       { background:#450a0a; border-color:#f87171; color:#fca5a5; }
    .tag-fixed      { background:#1e3a5f; border-color:#60a5fa; color:#93c5fd; }
    .blackboard     { background:linear-gradient(135deg,#14532d,#0f3d22); border-color:#22c55e; color:#86efac; }
    .seat-normal    { background:#1e2636; border-color:#3b4a63; color:#e2e8f0; box-shadow:0 2px 6px rgba(0,0,0,.4); }
    .seat-fixed     { background:#1a3460; border-color:#60a5fa; color:#93c5fd; box-shadow:0 0 0 3px rgba(96,165,250,.2); }
    .seat-empty     { background:#111827; border-color:#1f2937; border-style:dashed; color:#1f2937; }
    .seat-label     { color:rgba(241,245,249,.28); }
    .pin-badge      { background:#1e3a5f; color:#93c5fd; }
    .empty-state    { border-color:#2e3548; background:#1a1f2e; }
    .help-card      { background:#1a1f2e; border-color:#2e3548; box-shadow:0 2px 8px rgba(0,0,0,.3); }
}

/* ── 반응형 ── */
@media (max-width: 640px) {
    .seat { width: 50px; height: 50px; font-size: 17px; border-radius: 9px; }
    .seat-label { font-size: 8px; }
    .blackboard { padding: 9px 24px; font-size: 12px; }
}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# 상태 초기화
# ────────────────────────────────────────────────────────────────────────────
for _k, _v in {
    "total": 30, "cols": 6,
    "excluded": [], "fixed": {},
    "result": None, "history": []
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
    n_total  = S["total"]
    cols     = S["cols"]
    rows     = math.ceil(n_total / cols)
    seats    = rows * cols
    excluded = set(S["excluded"])
    fixed    = dict(S["fixed"])

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
# 사이드바  — number_input 단독 사용 (슬라이더 제거 → 라벨 겹침 원천 차단)
# ────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    st.markdown("---")

    # ── 기본 설정 ──
    st.markdown('<span class="sec-head">기본 설정</span>', unsafe_allow_html=True)

    S["total"] = st.number_input(
        "총 학생 수 (1–60)",
        min_value=1, max_value=60,
        value=S["total"], step=1,
        key="ni_total",
    )
    S["cols"] = st.number_input(
        "가로 열 수 (1–12)",
        min_value=1, max_value=12,
        value=S["cols"], step=1,
        key="ni_cols",
    )

    rows_calc = math.ceil(S["total"] / S["cols"])
    st.markdown(
        f'<div style="margin:10px 0 4px">'
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
    if st.button("추가", key="btn_excl", use_container_width=True):
        for n in parse_numbers(excl_input, S["total"]):
            if n not in S["excluded"]:
                S["excluded"].append(n)
            S["fixed"].pop(n, None)
        S["excluded"].sort()
        st.rerun()

    if S["excluded"]:
        tags = "".join(
            f'<span class="tag tag-excl">✕ {n}번</span>'
            for n in S["excluded"]
        )
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("전체 초기화", key="btn_excl_clr", use_container_width=True):
            S["excluded"] = []
            st.rerun()

    st.markdown("---")

    # ── 자리 고정 ──
    st.markdown('<span class="sec-head">📌 자리 고정</span>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        fix_num = st.number_input("번호", 1, S["total"], 1, key="fix_num")
    with fc2:
        fix_row = st.number_input("행", 1, rows_calc, 1, key="fix_row")
    with fc3:
        fix_col = st.number_input("열", 1, S["cols"], 1, key="fix_col")

    if st.button("고정 추가", key="btn_fix", use_container_width=True):
        sidx = (fix_row - 1) * S["cols"] + (fix_col - 1)
        S["fixed"] = {k: v for k, v in S["fixed"].items() if v != sidx}
        S["fixed"][fix_num] = sidx
        if fix_num in S["excluded"]:
            S["excluded"].remove(fix_num)
        st.rerun()

    if S["fixed"]:
        tags = "".join(
            f'<span class="tag tag-fixed">'
            f'📌 {num}번 → {sidx // S["cols"]+1}행 {sidx % S["cols"]+1}열'
            f'</span>'
            for num, sidx in sorted(S["fixed"].items())
        )
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("고정 전체 초기화", key="btn_fix_clr", use_container_width=True):
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
    "<h1 style='text-align:center;font-size:1.9rem;font-weight:900;"
    "letter-spacing:-.02em;margin-bottom:4px'>🏫 학급 자리 배치기</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;font-size:.88rem;margin-bottom:18px;opacity:.55'>"
    "무작위 배치 &nbsp;·&nbsp; 번호 고정 &nbsp;·&nbsp; 제외 설정</p>",
    unsafe_allow_html=True,
)

b1, b2, b3 = st.columns([3, 2, 2])
with b1:
    if st.button("🎲 자리 배치하기", type="primary", use_container_width=True):
        arrange()
        st.rerun()
with b2:
    if st.button("🔄 결과 초기화", use_container_width=True):
        S["result"] = None
        st.rerun()
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

    # 칠판 + 자리 그리드
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
                    f'<span style="opacity:.3;font-size:16px">—</span>'
                    f'<span class="seat-label">{r+1}행{c+1}열</span></div>'
                )
            elif idx in fixed_seats:
                grid += (
                    f'<div class="seat seat-fixed" title="{num}번 고정">'
                    f'{num}<span class="seat-label">📌 고정</span></div>'
                )
            else:
                grid += (
                    f'<div class="seat seat-normal" title="{num}번 | {r+1}행 {c+1}열">'
                    f'{num}<span class="seat-label">{r+1}행 {c+1}열</span></div>'
                )
        grid += '</div>'
    grid += '</div></div>'

    st.markdown(
        f'<div style="display:flex;justify-content:center">{grid}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # 통계
    active_cnt = sum(1 for v in result.values() if v is not None)
    for col, label, val in zip(
        st.columns(4),
        ["총 학생 수", "배치된 학생", "제외된 학생", "고정된 자리"],
        [f"{S['total']}명", f"{active_cnt}명",
         f"{len(S['excluded'])}명", f"{len(S['fixed'])}개"],
    ):
        col.metric(label, val)

    # 번호순 목록 — HTML 테이블 단일 렌더링으로 겹침 완전 제거
    with st.expander("📋 번호순 자리 목록 보기"):
        table = sorted(
            [
                (num,
                 sidx // cols_n + 1,
                 sidx  % cols_n + 1,
                 sidx in fixed_seats)
                for sidx, num in result.items()
            ],
            key=lambda x: x[0],
        )

        chunk  = math.ceil(len(table) / 3)
        groups = [table[:chunk], table[chunk:2*chunk], table[2*chunk:]]

        cols_list = st.columns(3)
        for col_ui, group in zip(cols_list, groups):
            if not group:
                continue
            rows_html = ""
            for num, r, c, is_fixed in group:
                pin = (
                    '<span class="pin-badge">📌 고정</span>'
                    if is_fixed else ""
                )
                rows_html += (
                    f"<tr>"
                    f"<td style='padding:5px 8px;font-weight:700'>{num}번</td>"
                    f"<td style='padding:5px 8px;opacity:.65'>{r}행 {c}열</td>"
                    f"<td style='padding:5px 6px'>{pin}</td>"
                    f"</tr>"
                )
            with col_ui:
                st.markdown(
                    f"<table class='list-table'>"
                    f"<thead><tr>"
                    f"<th>번호</th><th>위치</th><th></th>"
                    f"</tr></thead>"
                    f"<tbody>{rows_html}</tbody>"
                    f"</table>",
                    unsafe_allow_html=True,
                )

else:
    # 안내 화면
    st.markdown("""
    <div class="empty-state">
        <div class="e-icon">🪑</div>
        <div class="e-title">아직 자리가 배치되지 않았습니다</div>
        <div class="e-sub">
            왼쪽 사이드바에서 설정을 마친 후<br>
            <b>🎲 자리 배치하기</b> 버튼을 눌러주세요
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    for col_ui, (icon, title, desc) in zip(st.columns(3), [
        ("🔢", "인원 설정",  "학생 수와 가로 열 수를 입력하면 행 수가 자동으로 계산됩니다."),
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

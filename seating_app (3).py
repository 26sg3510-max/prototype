import streamlit as st
import random
import math
import json

st.set_page_config(page_title="학급 자리 배치기", page_icon="🏫", layout="wide")

# ────────────────────────────────────────────────────────────────────────────
# CSS — Streamlit 네이티브 테마 변수 위에 커스텀 요소만 덧씌움
#  · 배경/텍스트/버튼/입력 → config.toml [theme.light/dark] 가 담당
#  · 자리 그리드, 태그, 칠판 등 순수 커스텀 HTML → 여기서 담당
#  · @media prefers-color-scheme 은 커스텀 HTML 색상에만 사용
# ────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&family=JetBrains+Mono:wght@700&display=swap');

/* ── 전체 폰트 ─────────────────────────────────────── */
html, body, [class*="st-"], button, input {
    font-family: 'Noto Sans KR', sans-serif !important;
}

/* ── number_input +/- 버튼 폰트·크기 명시적 고정 ─────
   Streamlit이 SVG 아이콘 대신 텍스트 +/- 를 쓰는 경우
   브라우저 기본 폰트로 fallback되어 깨져 보이는 문제 방지 */
[data-testid="stNumberInput"] button {
    font-family: 'Noto Sans KR', Arial, sans-serif !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    line-height: 1 !important;
    min-width: 36px !important;
    min-height: 36px !important;
    border-radius: 7px !important;
    transition: background .12s, color .12s, border-color .12s !important;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--primary-color, #2563eb) !important;
    color: #fff !important;
}
/* SVG 아이콘이 있을 때도 크기 보장 */
[data-testid="stNumberInput"] button svg {
    width: 14px !important;
    height: 14px !important;
    stroke-width: 3px !important;
}

/* ── 입력 필드 테두리 가시성 ──────────────────────────── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"]   input {
    font-size: 15px !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border-width: 2px !important;
}

/* ── 슬라이더 핸들 크기 ──────────────────────────────── */
[data-testid="stSlider"] [role="slider"] {
    width: 20px !important;
    height: 20px !important;
}

/* ── 섹션 헤더 ───────────────────────────────────────── */
.sec-head {
    display: block;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
    opacity: .6;
    margin: 6px 0 10px 0;
    padding-bottom: 7px;
    border-bottom: 1.5px solid currentColor;
}

/* ── 배지 ────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    margin-right: 4px;
    border: 1.5px solid;
}

/* ─────────────────────────────────────────────────────
   라이트 모드 커스텀 색상
───────────────────────────────────────────────────── */
@media (prefers-color-scheme: light) {
    .badge.b-blue   { background:#dbeafe; color:#1d4ed8; border-color:#93c5fd; }
    .badge.b-purple { background:#ede9fe; color:#5b21b6; border-color:#c4b5fd; }
    .badge.b-green  { background:#dcfce7; color:#15803d; border-color:#86efac; }

    .tag-excl  { background:#fee2e2; border-color:#fca5a5; color:#991b1b; }
    .tag-fixed { background:#dbeafe; border-color:#93c5fd; color:#1e40af; }

    .blackboard { background: linear-gradient(135deg,#14532d,#166534); border-color:#16a34a; color:#bbf7d0; }

    .seat-normal { background:#ffffff;   border-color:#cbd5e1; color:#1e293b; box-shadow:0 1px 4px rgba(0,0,0,.08); }
    .seat-fixed  { background:#dbeafe;   border-color:#2563eb; color:#1d4ed8; box-shadow:0 0 0 3px #dbeafe; }
    .seat-empty  { background:#f8fafc;   border-color:#e2e8f0; color:#e2e8f0; }
    .seat-label  { color: rgba(15,23,42,.35); }

    .empty-state { border-color:#cbd5e1; background:#ffffff; }
    .help-card   { background:#ffffff;   border-color:#e2e8f0; box-shadow:0 1px 4px rgba(0,0,0,.07); }
}

/* ─────────────────────────────────────────────────────
   다크 모드 커스텀 색상
───────────────────────────────────────────────────── */
@media (prefers-color-scheme: dark) {
    .badge.b-blue   { background:#1e3a5f; color:#93c5fd; border-color:#3b6ea8; }
    .badge.b-purple { background:#2e1f5e; color:#d8b4fe; border-color:#6d4fc4; }
    .badge.b-green  { background:#052e16; color:#86efac; border-color:#166534; }

    .tag-excl  { background:#450a0a; border-color:#f87171; color:#fca5a5; }
    .tag-fixed { background:#1e3a5f; border-color:#60a5fa; color:#93c5fd; }

    .blackboard { background: linear-gradient(135deg,#14532d,#0f3d22); border-color:#22c55e; color:#86efac; }

    .seat-normal { background:#1e2636; border-color:#3b4a63; color:#e2e8f0; box-shadow:0 2px 6px rgba(0,0,0,.35); }
    .seat-fixed  { background:#1a3460; border-color:#60a5fa; color:#93c5fd; box-shadow:0 0 0 3px rgba(96,165,250,.18); }
    .seat-empty  { background:#111827; border-color:#1f2937; color:#1f2937; }
    .seat-label  { color: rgba(241,245,249,.3); }

    .empty-state { border-color:#2e3548; background:#1a1f2e; }
    .help-card   { background:#1a1f2e;   border-color:#2e3548; box-shadow:0 2px 8px rgba(0,0,0,.3); }
}

/* ── 태그 공통 ────────────────────────────────────────── */
.tag-wrap { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0 4px; }
.tag {
    display:inline-flex; align-items:center;
    padding:4px 13px; border-radius:999px;
    font-size:12px; font-weight:800; border:1.5px solid;
}

/* ── 자리 그리드 공통 ─────────────────────────────────── */
.classroom-wrap {
    display:flex; flex-direction:column; align-items:center;
    padding:24px 12px;
}
.blackboard {
    border-width:2.5px; border-style:solid; border-radius:12px;
    text-align:center; padding:11px 72px;
    font-size:14px; font-weight:800; letter-spacing:.18em;
    margin-bottom:32px; width:fit-content;
}
.seat-grid { display:flex; flex-direction:column; gap:10px; }
.seat-row  { display:flex; gap:10px; justify-content:center; }
.seat {
    width:68px; height:68px; border-radius:12px;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    font-family:'JetBrains Mono', monospace;
    font-size:22px; font-weight:700;
    border:2px solid transparent;
    position:relative;
    transition:transform .13s ease, box-shadow .13s ease;
    cursor:default; user-select:none;
}
.seat:hover { transform:translateY(-3px); z-index:1; }
.seat-label {
    position:absolute; bottom:5px;
    font-size:9px; font-weight:700; letter-spacing:.04em;
    font-family:'Noto Sans KR', sans-serif; line-height:1;
}

/* ── 안내화면 & 헬프카드 공통 ─────────────────────────── */
.empty-state {
    text-align:center; padding:72px 28px;
    border:2px dashed; border-radius:20px;
}
.empty-state .e-icon  { font-size:52px; margin-bottom:14px; }
.empty-state .e-title { font-size:1.15rem; font-weight:800; margin-bottom:8px; }
.empty-state .e-sub   { font-size:.88rem; line-height:1.8; opacity:.7; }

.help-card {
    border:1.5px solid; border-radius:16px;
    padding:22px; height:100%;
}
.help-card .h-icon  { font-size:1.9rem; margin-bottom:10px; }
.help-card .h-title { font-size:.95rem; font-weight:800; margin-bottom:7px; }
.help-card .h-desc  { font-size:.83rem; line-height:1.65; opacity:.7; }

/* ── 반응형 ───────────────────────────────────────────── */
@media (max-width:640px) {
    .seat { width:50px; height:50px; font-size:17px; border-radius:9px; }
    .seat-label { font-size:8px; }
    .blackboard { padding:9px 28px; font-size:13px; }
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
# 사이드바
# ────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    st.markdown("---")

    # ── 기본 설정 ──────────────────────────────────────────────────
    st.markdown('<span class="sec-head">기본 설정</span>', unsafe_allow_html=True)

    S["total"] = st.slider("총 학생 수", 1, 60, S["total"], 1)
    S["total"] = st.number_input(
        "학생 수 직접 입력 (1–60)",
        min_value=1, max_value=60, value=S["total"], step=1,
        key="total_direct",
    )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    S["cols"] = st.slider("가로 열 수", 1, 12, S["cols"], 1)
    S["cols"] = st.number_input(
        "열 수 직접 입력 (1–12)",
        min_value=1, max_value=12, value=S["cols"], step=1,
        key="cols_direct",
    )

    rows_calc = math.ceil(S["total"] / S["cols"])
    st.markdown(
        f'<div style="margin:12px 0 4px">'
        f'<span class="badge b-blue">{S["cols"]}열</span>'
        f'<span class="badge b-purple">{rows_calc}행</span>'
        f'<span class="badge b-green">{S["total"]}명</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── 제외 번호 ──────────────────────────────────────────────────
    st.markdown('<span class="sec-head">🚫 제외할 번호</span>', unsafe_allow_html=True)
    excl_input = st.text_input(
        "제외 번호 입력",
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
        tags = "".join(f'<span class="tag tag-excl">✕ {n}번</span>' for n in S["excluded"])
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("제외 전체 초기화", key="btn_excl_clr", use_container_width=True):
            S["excluded"] = []
            st.rerun()

    st.markdown("---")

    # ── 자리 고정 ──────────────────────────────────────────────────
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
            f'<span class="tag tag-fixed">📌 {num}번 → {sidx // S["cols"]+1}행 {sidx % S["cols"]+1}열</span>'
            for num, sidx in sorted(S["fixed"].items())
        )
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("고정 전체 초기화", key="btn_fix_clr", use_container_width=True):
            S["fixed"] = {}
            st.rerun()

    st.markdown("---")

    # ── JSON 저장 ──────────────────────────────────────────────────
    if S["result"]:
        cfg = {
            "total": S["total"], "cols": S["cols"],
            "excluded": S["excluded"],
            "fixed": {str(k): v for k, v in S["fixed"].items()},
        }
        st.download_button(
            "⬇ 설정 저장 (JSON)",
            data=json.dumps(cfg, ensure_ascii=False, indent=2),
            file_name="seating_config.json",
            mime="application/json",
            use_container_width=True,
        )


# ────────────────────────────────────────────────────────────────────────────
# 메인
# ────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;font-size:2rem;font-weight:900;"
    "letter-spacing:-.02em;margin-bottom:4px'>🏫 학급 자리 배치기</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;font-size:.9rem;margin-bottom:20px;opacity:.6'>"
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

    html = '<div class="classroom-wrap">'
    html += '<div class="blackboard">📋 &nbsp; 칠 판 &nbsp; ( 앞 )</div>'
    html += '<div class="seat-grid">'

    for r in range(rows_n):
        html += '<div class="seat-row">'
        for c in range(cols_n):
            idx = r * cols_n + c
            num = result.get(idx)
            if num is None:
                html += (
                    f'<div class="seat seat-empty">'
                    f'<span style="font-size:18px;opacity:.3">—</span>'
                    f'<span class="seat-label">{r+1}행{c+1}열</span></div>'
                )
            elif idx in fixed_seats:
                html += (
                    f'<div class="seat seat-fixed" title="{num}번 (고정)">'
                    f'{num}<span class="seat-label">📌 고정</span></div>'
                )
            else:
                html += (
                    f'<div class="seat seat-normal" title="{num}번 | {r+1}행 {c+1}열">'
                    f'{num}<span class="seat-label">{r+1}행 {c+1}열</span></div>'
                )
        html += '</div>'

    html += '</div></div>'
    st.markdown(
        f'<div style="display:flex;justify-content:center">{html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    active_cnt = sum(1 for v in result.values() if v is not None)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("총 학생 수",  f"{S['total']}명")
    s2.metric("배치된 학생", f"{active_cnt}명")
    s3.metric("제외된 학생", f"{len(S['excluded'])}명")
    s4.metric("고정된 자리", f"{len(S['fixed'])}개")

    with st.expander("📋 번호순 자리 목록 보기"):
        table = sorted(
            [
                (num, sidx // cols_n + 1, sidx % cols_n + 1,
                 "📌 고정" if sidx in fixed_seats else "")
                for sidx, num in result.items()
            ],
            key=lambda x: x[0],
        )
        chunk = math.ceil(len(table) / 3)
        for col_ui, rows_data in zip(
            st.columns(3),
            [table[:chunk], table[chunk:2*chunk], table[2*chunk:]],
        ):
            with col_ui:
                for num, r, c, pin in rows_data:
                    dot = "🔵" if pin else "⚪"
                    st.markdown(f"{dot} **{num}번** &nbsp; {r}행 {c}열 &nbsp; {pin}")

else:
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
        ("🔢", "인원 설정",  "슬라이더 또는 직접 입력으로 학생 수와 열 수를 설정합니다."),
        ("🚫", "번호 제외",  "결석·전학 등 배치에서 빠져야 할 번호를 추가합니다."),
        ("📌", "자리 고정",  "특정 번호를 원하는 행·열 위치에 고정 배치합니다."),
    ]):
        with col_ui:
            st.markdown(f"""
            <div class="help-card">
                <div class="h-icon">{icon}</div>
                <div class="h-title">{title}</div>
                <div class="h-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

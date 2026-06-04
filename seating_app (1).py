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

/* ── 전역 ── */
:root {
    --bg:       #0d1117;
    --surface:  #161b22;
    --surface2: #1f2937;
    --surface3: #243044;
    --accent:   #58a6ff;
    --accent2:  #bc8cff;
    --success:  #3fb950;
    --danger:   #f85149;
    --warn:     #d29922;
    --text:     #e6edf3;
    --text2:    #8b949e;
    --border:   #30363d;
    --border2:  #3d4f6b;
}
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── 라벨 가시성 ── */
label, .stSlider label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] {
    color: var(--text) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: .03em;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
}
/* 캡션 */
[data-testid="stCaptionContainer"] p { color: var(--text2) !important; font-size: 12px !important; }

/* ── 입력 필드 ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px #58a6ff28 !important;
}
/* +/- 버튼 가시성 */
[data-testid="stNumberInput"] button {
    background: var(--surface3) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    min-width: 36px !important;
    min-height: 36px !important;
    transition: background .12s, border-color .12s !important;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
}
[data-testid="stNumberInput"] button svg { stroke: currentColor !important; }

/* ── 슬라이더 ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--accent) !important;
    border: 2px solid var(--accent) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[data-testid^="stThumb"] {
    background: var(--accent) !important;
}
/* track fill */
[data-testid="stSlider"] [data-baseweb="slider"] div:first-child > div:nth-child(3) {
    background: var(--accent) !important;
}

/* ── 주요 버튼 ── */
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 10px 0 !important;
    transition: filter .15s, transform .12s !important;
}
[data-testid="baseButton-primary"]:hover {
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}
[data-testid="baseButton-secondary"] {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    transition: border-color .12s, background .12s !important;
}
[data-testid="baseButton-secondary"]:hover {
    border-color: var(--accent) !important;
    background: var(--surface3) !important;
}

/* ── 메트릭 ── */
[data-testid="stMetric"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
}
[data-testid="stMetricLabel"] p { color: var(--text2) !important; font-size: 12px !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-size: 1.6rem !important; font-weight: 900 !important; }

/* ── 익스팬더 ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary { color: var(--text) !important; font-weight: 700 !important; }

/* ── 구분선 ── */
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* ── 자리 그리드 ── */
.classroom-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0;
    padding: 20px 0;
}
.blackboard {
    background: linear-gradient(135deg, #1a4731, #0f3320);
    border: 2px solid #2ea043;
    border-radius: 10px;
    text-align: center;
    padding: 10px 60px;
    color: #7ee787;
    font-size: 14px; font-weight: 700;
    letter-spacing: .12em;
    box-shadow: 0 4px 20px #0005;
    margin-bottom: 28px;
    width: fit-content;
}
.seat-grid { display: flex; flex-direction: column; gap: 10px; }
.seat-row  { display: flex; gap: 10px; justify-content: center; }
.seat {
    width: 70px; height: 70px;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    border: 2px solid transparent;
    position: relative;
    transition: transform .13s, box-shadow .13s;
    cursor: default;
    user-select: none;
}
.seat:hover { transform: translateY(-3px); box-shadow: 0 10px 24px #00000055; }

/* 일반 자리 */
.seat-normal {
    background: var(--surface2);
    border-color: var(--border2);
    color: var(--text);
}
.seat-normal:hover { border-color: var(--accent); }

/* 고정 자리 */
.seat-fixed {
    background: linear-gradient(135deg, #0d2a4a, #1a3a63);
    border-color: var(--accent);
    color: #93c5fd;
    box-shadow: 0 0 0 1px #58a6ff33, inset 0 1px 0 #ffffff12;
}

/* 빈 자리 */
.seat-empty {
    background: #0d1117;
    border-color: #21262d;
    border-style: dashed;
    color: #21262d;
}

/* 자리 하단 라벨 */
.seat-label {
    position: absolute;
    bottom: 5px;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: .04em;
    color: rgba(255,255,255,.25);
    font-family: 'Noto Sans KR', sans-serif;
    line-height: 1;
}
.seat-fixed .seat-label { color: #58a6ff66; }

/* ── 태그 ── */
.tag-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0; }
.tag {
    display: inline-flex; align-items: center;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 13px; font-weight: 700;
}
.tag-excl  { background: #2d1414; border: 1.5px solid var(--danger);  color: var(--danger); }
.tag-fixed { background: #0d2240; border: 1.5px solid var(--accent);  color: var(--accent); }

/* ── 배지 ── */
.badge {
    display: inline-block; padding: 3px 12px; border-radius: 999px;
    font-size: 12px; font-weight: 700; margin-right: 4px;
}
.b-blue   { background: #0d2240; color: var(--accent); border: 1px solid #1d3d6b; }
.b-purple { background: #1f133a; color: var(--accent2); border: 1px solid #3d2570; }
.b-green  { background: #0d2a1a; color: var(--success); border: 1px solid #1a4a2a; }

/* ── 섹션 헤더 ── */
.sec-head {
    font-size: 11px; font-weight: 700; letter-spacing: .1em;
    text-transform: uppercase; color: var(--text2);
    margin: 4px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
}

/* ── 안내 영역 ── */
.empty-state {
    text-align: center; padding: 72px 24px;
    border: 2px dashed var(--border);
    border-radius: 20px; color: var(--text2);
}
.empty-state .icon { font-size: 56px; margin-bottom: 14px; }
.empty-state .title { font-size: 1.2rem; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.empty-state .sub   { font-size: .88rem; line-height: 1.7; }

/* ── 사용법 카드 ── */
.help-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
}
.help-card .hicon { font-size: 1.8rem; margin-bottom: 10px; }
.help-card .htitle { font-size: .95rem; font-weight: 700; margin-bottom: 6px; color: var(--text); }
.help-card .hdesc  { font-size: .83rem; color: var(--text2); line-height: 1.6; }

/* ── 모바일 ── */
@media (max-width: 640px) {
    .seat { width: 52px; height: 52px; font-size: 17px; border-radius: 9px; }
    .seat-label { font-size: 8px; }
}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# 상태 초기화
# ────────────────────────────────────────────────────────────────────────────
_defaults = {
    "total": 30,
    "cols": 6,
    "excluded": [],
    "fixed": {},
    "result": None,
    "history": [],
}
for _k, _v in _defaults.items():
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
    n_total = S["total"]
    cols    = S["cols"]
    rows    = math.ceil(n_total / cols)
    seats   = rows * cols

    excluded = set(S["excluded"])
    fixed    = dict(S["fixed"])

    active = [i for i in range(1, n_total + 1) if i not in excluded]

    # 유효하지 않은 고정 제거
    for num in list(fixed.keys()):
        if num not in active or fixed[num] >= seats:
            del fixed[num]
    S["fixed"] = fixed

    assigned = {sidx: num for num, sidx in fixed.items()}

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
    st.markdown('<div class="sec-head">기본 설정</div>', unsafe_allow_html=True)

    # 슬라이더 + number_input 조합 → 즉시 반응 & 직접 입력 모두 지원
    S["total"] = st.slider(
        "총 학생 수",
        min_value=1, max_value=60,
        value=S["total"], step=1,
        help="슬라이더로 빠르게, 또는 아래에서 직접 입력"
    )
    S["total"] = st.number_input(
        "직접 입력 (1–60)",
        min_value=1, max_value=60,
        value=S["total"], step=1,
        key="total_direct",
        label_visibility="visible",
    )

    S["cols"] = st.slider(
        "가로 열 수",
        min_value=1, max_value=12,
        value=S["cols"], step=1,
    )
    S["cols"] = st.number_input(
        "직접 입력 (1–12)",
        min_value=1, max_value=12,
        value=S["cols"], step=1,
        key="cols_direct",
        label_visibility="visible",
    )

    rows_calc = math.ceil(S["total"] / S["cols"])
    st.markdown(
        f'<div style="margin:10px 0 4px 0;">'
        f'<span class="badge b-blue">{S["cols"]}열</span>'
        f'<span class="badge b-purple">{rows_calc}행</span>'
        f'<span class="badge b-green">{S["total"]}명</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── 제외 번호 ──
    st.markdown('<div class="sec-head">🚫 제외할 번호</div>', unsafe_allow_html=True)
    excl_input = st.text_input(
        "번호 입력",
        key="excl_input",
        placeholder="예: 1, 5, 12   (콤마·공백 구분)",
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
        html = '<div class="tag-wrap">' + \
               "".join(f'<span class="tag tag-excl">✕ {n}번</span>' for n in S["excluded"]) + \
               '</div>'
        st.markdown(html, unsafe_allow_html=True)
        if st.button("제외 전체 초기화", key="btn_excl_clr", use_container_width=True):
            S["excluded"] = []
            st.rerun()

    st.markdown("---")

    # ── 자리 고정 ──
    st.markdown('<div class="sec-head">📌 자리 고정</div>', unsafe_allow_html=True)

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
        html = '<div class="tag-wrap">'
        for num, sidx in sorted(S["fixed"].items()):
            r = sidx // S["cols"] + 1
            c = sidx  % S["cols"] + 1
            html += f'<span class="tag tag-fixed">📌 {num}번 → {r}행{c}열</span>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
        if st.button("고정 전체 초기화", key="btn_fix_clr", use_container_width=True):
            S["fixed"] = {}
            st.rerun()

    st.markdown("---")

    # ── JSON 저장 ──
    if S["result"]:
        cfg = {
            "total": S["total"],
            "cols":  S["cols"],
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
    "letter-spacing:-.02em;margin-bottom:4px;'>🏫 학급 자리 배치기</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#8b949e;font-size:.9rem;margin-bottom:20px;'>"
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
    disabled = len(S["history"]) <= 1
    if st.button("↩ 이전 결과", use_container_width=True, disabled=disabled):
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
    html += '<div class="blackboard">📋 &nbsp; 칠 판 &nbsp; (앞)</div>'
    html += '<div class="seat-grid">'

    for r in range(rows_n):
        html += '<div class="seat-row">'
        for c in range(cols_n):
            idx = r * cols_n + c
            num = result.get(idx)

            if num is None:
                html += (
                    f'<div class="seat seat-empty">'
                    f'<span style="font-size:20px">—</span>'
                    f'<span class="seat-label">{r+1}행{c+1}열</span></div>'
                )
            elif idx in fixed_seats:
                html += (
                    f'<div class="seat seat-fixed" title="{num}번 (고정 자리)">'
                    f'{num}'
                    f'<span class="seat-label">📌 고정</span></div>'
                )
            else:
                html += (
                    f'<div class="seat seat-normal" title="{num}번 | {r+1}행 {c+1}열">'
                    f'{num}'
                    f'<span class="seat-label">{r+1}행 {c+1}열</span></div>'
                )
        html += '</div>'

    html += '</div></div>'
    st.markdown(f'<div style="display:flex;justify-content:center;">{html}</div>',
                unsafe_allow_html=True)

    st.markdown("---")

    # ── 통계 ──
    active_cnt = sum(1 for v in result.values() if v is not None)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("총 학생 수",   f"{S['total']}명")
    s2.metric("배치된 학생",  f"{active_cnt}명")
    s3.metric("제외된 학생",  f"{len(S['excluded'])}명")
    s4.metric("고정된 자리",  f"{len(S['fixed'])}개")

    # ── 번호순 목록 ──
    with st.expander("📋 번호순 자리 목록 보기"):
        table = []
        for sidx, num in result.items():
            r = sidx // cols_n + 1
            c = sidx  % cols_n + 1
            pin = "📌 고정" if sidx in fixed_seats else ""
            table.append((num, r, c, pin))
        table.sort(key=lambda x: x[0])

        chunk = math.ceil(len(table) / 3)
        tc1, tc2, tc3 = st.columns(3)
        for col_ui, chunk_data in zip(
            [tc1, tc2, tc3],
            [table[:chunk], table[chunk:2*chunk], table[2*chunk:]]
        ):
            with col_ui:
                for num, r, c, pin in chunk_data:
                    dot = "🔵" if pin else "⚪"
                    st.markdown(f"{dot} **{num}번** &nbsp; {r}행 {c}열 &nbsp; {pin}")

else:
    # ── 안내 화면 ──
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🪑</div>
        <div class="title">아직 자리가 배치되지 않았습니다</div>
        <div class="sub">왼쪽 사이드바에서 설정을 마친 후<br>
        <b style="color:#58a6ff">🎲 자리 배치하기</b> 버튼을 눌러주세요</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    u1, u2, u3 = st.columns(3)
    for col_ui, (icon, title, desc) in zip([u1, u2, u3], [
        ("🔢", "인원 설정",  "슬라이더 또는 직접 입력으로 학생 수와 열 수를 설정합니다."),
        ("🚫", "번호 제외",  "결석·전학 등 배치에서 빠져야 할 번호를 추가합니다."),
        ("📌", "자리 고정",  "특정 번호를 원하는 행·열 위치에 고정 배치합니다."),
    ]):
        with col_ui:
            st.markdown(f"""
            <div class="help-card">
                <div class="hicon">{icon}</div>
                <div class="htitle">{title}</div>
                <div class="hdesc">{desc}</div>
            </div>""", unsafe_allow_html=True)

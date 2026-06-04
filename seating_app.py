import streamlit as st
import random
import math
import json

st.set_page_config(page_title="학급 자리 배치기", page_icon="🏫", layout="wide")

# ────────────────────────────────────────────────────────────────────────────
# CSS  — prefers-color-scheme 기반 라이트/다크 자동 전환
# ────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&family=JetBrains+Mono:wght@700&display=swap');

/* ══════════════════════════════════════════
   라이트 모드 변수 (기본)
══════════════════════════════════════════ */
:root {
    --bg:        #f5f7fa;
    --surface:   #ffffff;
    --surface2:  #f0f4f8;
    --surface3:  #e2e8f0;
    --accent:    #2563eb;
    --accent-bg: #dbeafe;
    --accent2:   #7c3aed;
    --success:   #16a34a;
    --success-bg:#dcfce7;
    --danger:    #dc2626;
    --danger-bg: #fee2e2;
    --warn:      #d97706;
    --text:      #0f172a;
    --text2:     #475569;
    --text3:     #94a3b8;
    --border:    #cbd5e1;
    --border2:   #94a3b8;
    --shadow:    0 1px 3px rgba(0,0,0,.08), 0 4px 12px rgba(0,0,0,.06);
    --shadow-lg: 0 4px 16px rgba(0,0,0,.10), 0 8px 32px rgba(0,0,0,.08);
    /* 자리 */
    --seat-normal-bg:     #ffffff;
    --seat-normal-border: #cbd5e1;
    --seat-normal-text:   #1e293b;
    --seat-fixed-bg:      #dbeafe;
    --seat-fixed-border:  #2563eb;
    --seat-fixed-text:    #1d4ed8;
    --seat-empty-bg:      #f8fafc;
    --seat-empty-border:  #e2e8f0;
    --seat-empty-text:    #cbd5e1;
    --seat-label-color:   rgba(15,23,42,.35);
    /* 칠판 */
    --bb-bg:     linear-gradient(135deg,#14532d,#166534);
    --bb-border: #16a34a;
    --bb-text:   #bbf7d0;
    /* 태그 */
    --tag-excl-bg:  #fee2e2;
    --tag-excl-bd:  #fca5a5;
    --tag-excl-tx:  #991b1b;
    --tag-fix-bg:   #dbeafe;
    --tag-fix-bd:   #93c5fd;
    --tag-fix-tx:   #1e40af;
    /* 배지 */
    --badge-blue-bg:   #dbeafe; --badge-blue-tx:   #1d4ed8;
    --badge-purple-bg: #ede9fe; --badge-purple-tx: #5b21b6;
    --badge-green-bg:  #dcfce7; --badge-green-tx:  #15803d;
    /* 헬프카드 */
    --card-bg:     #ffffff;
    --card-border: #e2e8f0;
    /* 메트릭 */
    --metric-bg:    #ffffff;
    --metric-border:#e2e8f0;
    /* 안내 */
    --empty-border: #cbd5e1;
    --empty-text:   #64748b;
}

/* ══════════════════════════════════════════
   다크 모드 변수
══════════════════════════════════════════ */
@media (prefers-color-scheme: dark) {
  :root {
    --bg:        #0f1117;
    --surface:   #1a1f2e;
    --surface2:  #242938;
    --surface3:  #2e3548;
    --accent:    #60a5fa;
    --accent-bg: #1e3a5f;
    --accent2:   #c084fc;
    --success:   #4ade80;
    --success-bg:#052e16;
    --danger:    #f87171;
    --danger-bg: #450a0a;
    --warn:      #fbbf24;
    --text:      #f1f5f9;
    --text2:     #94a3b8;
    --text3:     #475569;
    --border:    #334155;
    --border2:   #4a5568;
    --shadow:    0 1px 3px rgba(0,0,0,.4), 0 4px 12px rgba(0,0,0,.3);
    --shadow-lg: 0 4px 16px rgba(0,0,0,.5), 0 8px 32px rgba(0,0,0,.4);
    --seat-normal-bg:     #1e2636;
    --seat-normal-border: #3b4a63;
    --seat-normal-text:   #e2e8f0;
    --seat-fixed-bg:      #1a3460;
    --seat-fixed-border:  #60a5fa;
    --seat-fixed-text:    #93c5fd;
    --seat-empty-bg:      #111827;
    --seat-empty-border:  #1f2937;
    --seat-empty-text:    #1f2937;
    --seat-label-color:   rgba(241,245,249,.25);
    --bb-bg:     linear-gradient(135deg,#14532d,#0f3d22);
    --bb-border: #22c55e;
    --bb-text:   #86efac;
    --tag-excl-bg:  #450a0a;
    --tag-excl-bd:  #f87171;
    --tag-excl-tx:  #fca5a5;
    --tag-fix-bg:   #1e3a5f;
    --tag-fix-bd:   #60a5fa;
    --tag-fix-tx:   #93c5fd;
    --badge-blue-bg:   #1e3a5f; --badge-blue-tx:   #93c5fd;
    --badge-purple-bg: #3b1f6e; --badge-purple-tx: #d8b4fe;
    --badge-green-bg:  #052e16; --badge-green-tx:  #86efac;
    --card-bg:     #1a1f2e;
    --card-border: #2e3548;
    --metric-bg:    #1a1f2e;
    --metric-border:#2e3548;
    --empty-border: #2e3548;
    --empty-text:   #64748b;
  }
}

/* ══════════════════════════════════════════
   Streamlit 컨테이너 배경 오버라이드
══════════════════════════════════════════ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section[data-testid="stSidebar"] > div:first-child,
.main .block-container {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1.5px solid var(--border) !important;
}
/* 사이드바 내 모든 텍스트 */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div { color: var(--text) !important; }

/* ══════════════════════════════════════════
   라벨 / 캡션
══════════════════════════════════════════ */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] {
    color: var(--text) !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: .02em;
}
[data-testid="stCaptionContainer"] p {
    color: var(--text2) !important;
    font-size: 12px !important;
}
p, span, li, td, th {
    color: var(--text) !important;
}

/* ══════════════════════════════════════════
   입력 필드 — 라이트/다크 모두 선명하게
══════════════════════════════════════════ */
[data-testid="stNumberInput"] > div,
[data-testid="stTextInput"]   > div {
    background: var(--surface) !important;
    border-radius: 9px !important;
}
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"]   input {
    background: var(--surface) !important;
    border: 2px solid var(--border2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    padding: 8px 12px !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"]   input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent) !important;
    outline: none !important;
}

/* +/- 버튼 — 크고 선명하게 */
[data-testid="stNumberInput"] button {
    background: var(--surface2) !important;
    border: 2px solid var(--border2) !important;
    border-radius: 7px !important;
    color: var(--text) !important;
    font-size: 20px !important;
    font-weight: 900 !important;
    min-width: 38px !important;
    min-height: 38px !important;
    line-height: 1 !important;
    transition: all .12s ease !important;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
    transform: scale(1.08) !important;
}
[data-testid="stNumberInput"] button:active {
    transform: scale(.96) !important;
}
[data-testid="stNumberInput"] button svg {
    stroke: currentColor !important;
    stroke-width: 2.5px !important;
    width: 16px !important; height: 16px !important;
}

/* ══════════════════════════════════════════
   슬라이더
══════════════════════════════════════════ */
[data-testid="stSlider"] [data-baseweb="slider"] {
    padding: 4px 0 !important;
}
[data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
    border: 3px solid var(--accent) !important;
    width: 22px !important; height: 22px !important;
    box-shadow: 0 2px 8px color-mix(in srgb, var(--accent) 40%, transparent) !important;
}
/* filled track */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(3) {
    background: var(--accent) !important;
    height: 5px !important;
}
/* empty track */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
    background: var(--surface3) !important;
    height: 5px !important;
}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    color: var(--text2) !important;
    font-size: 11px !important;
}

/* ══════════════════════════════════════════
   버튼
══════════════════════════════════════════ */
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 10px 0 !important;
    letter-spacing: .02em;
    box-shadow: 0 2px 12px color-mix(in srgb, var(--accent) 35%, transparent) !important;
    transition: filter .15s, transform .12s, box-shadow .15s !important;
}
[data-testid="baseButton-primary"]:hover {
    filter: brightness(1.12) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px color-mix(in srgb, var(--accent) 45%, transparent) !important;
}
[data-testid="baseButton-primary"]:active { transform: translateY(0) !important; }

[data-testid="baseButton-secondary"] {
    background: var(--surface2) !important;
    border: 2px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    transition: all .13s ease !important;
}
[data-testid="baseButton-secondary"]:hover {
    border-color: var(--accent) !important;
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
}
[data-testid="baseButton-secondary"]:disabled {
    opacity: .38 !important;
    cursor: not-allowed !important;
}

/* ══════════════════════════════════════════
   메트릭
══════════════════════════════════════════ */
[data-testid="stMetric"] {
    background: var(--metric-bg) !important;
    border: 1.5px solid var(--metric-border) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stMetricLabel"] p {
    color: var(--text2) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: .06em;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 1.7rem !important;
    font-weight: 900 !important;
}

/* ══════════════════════════════════════════
   익스팬더
══════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stExpander"] summary {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}
[data-testid="stExpander"] summary:hover { color: var(--accent) !important; }

/* ══════════════════════════════════════════
   구분선
══════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1.5px solid var(--border) !important;
    margin: 18px 0 !important;
    opacity: 1 !important;
}

/* ══════════════════════════════════════════
   섹션 헤더
══════════════════════════════════════════ */
.sec-head {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--text2);
    margin: 6px 0 10px 0;
    padding-bottom: 7px;
    border-bottom: 1.5px solid var(--border);
    display: block;
}

/* ══════════════════════════════════════════
   배지
══════════════════════════════════════════ */
.badge {
    display: inline-block;
    padding: 4px 13px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    margin-right: 4px;
}
.b-blue   { background: var(--badge-blue-bg);   color: var(--badge-blue-tx);   border: 1px solid var(--badge-blue-tx); }
.b-purple { background: var(--badge-purple-bg); color: var(--badge-purple-tx); border: 1px solid var(--badge-purple-tx); }
.b-green  { background: var(--badge-green-bg);  color: var(--badge-green-tx);  border: 1px solid var(--badge-green-tx); }

/* ══════════════════════════════════════════
   태그
══════════════════════════════════════════ */
.tag-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin: 8px 0 4px 0; }
.tag {
    display: inline-flex; align-items: center;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 12px; font-weight: 800;
    border: 1.5px solid;
}
.tag-excl {
    background: var(--tag-excl-bg);
    border-color: var(--tag-excl-bd);
    color: var(--tag-excl-tx);
}
.tag-fixed {
    background: var(--tag-fix-bg);
    border-color: var(--tag-fix-bd);
    color: var(--tag-fix-tx);
}

/* ══════════════════════════════════════════
   자리 그리드
══════════════════════════════════════════ */
.classroom-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 12px;
    gap: 0;
}
.blackboard {
    background: var(--bb-bg);
    border: 2.5px solid var(--bb-border);
    border-radius: 12px;
    text-align: center;
    padding: 11px 72px;
    color: var(--bb-text);
    font-size: 14px; font-weight: 800;
    letter-spacing: .18em;
    margin-bottom: 32px;
    width: fit-content;
    box-shadow: 0 4px 24px rgba(0,0,0,.15);
}
.seat-grid { display: flex; flex-direction: column; gap: 10px; }
.seat-row  { display: flex; gap: 10px; justify-content: center; }
.seat {
    width: 68px; height: 68px;
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
.seat:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
    z-index: 1;
}
.seat-normal {
    background: var(--seat-normal-bg);
    border-color: var(--seat-normal-border);
    color: var(--seat-normal-text);
    box-shadow: var(--shadow);
}
.seat-normal:hover { border-color: var(--accent); }
.seat-fixed {
    background: var(--seat-fixed-bg);
    border-color: var(--seat-fixed-border);
    color: var(--seat-fixed-text);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 20%, transparent), var(--shadow);
}
.seat-empty {
    background: var(--seat-empty-bg);
    border-color: var(--seat-empty-border);
    border-style: dashed;
    color: var(--seat-empty-text);
    box-shadow: none;
}
.seat-label {
    position: absolute; bottom: 5px;
    font-size: 9px; font-weight: 700;
    letter-spacing: .04em;
    color: var(--seat-label-color);
    font-family: 'Noto Sans KR', sans-serif;
    line-height: 1;
}

/* ══════════════════════════════════════════
   안내 화면 & 헬프 카드
══════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: 72px 28px;
    border: 2px dashed var(--empty-border);
    border-radius: 20px;
    color: var(--empty-text);
    background: var(--surface);
}
.empty-state .e-icon  { font-size: 52px; margin-bottom: 14px; }
.empty-state .e-title { font-size: 1.15rem; font-weight: 800; color: var(--text); margin-bottom: 8px; }
.empty-state .e-sub   { font-size: .88rem; line-height: 1.8; color: var(--text2); }

.help-card {
    background: var(--card-bg);
    border: 1.5px solid var(--card-border);
    border-radius: 16px;
    padding: 22px;
    box-shadow: var(--shadow);
    height: 100%;
}
.help-card .h-icon  { font-size: 1.9rem; margin-bottom: 10px; }
.help-card .h-title { font-size: .95rem; font-weight: 800; margin-bottom: 7px; color: var(--text); }
.help-card .h-desc  { font-size: .83rem; color: var(--text2); line-height: 1.65; }

/* ══════════════════════════════════════════
   반응형
══════════════════════════════════════════ */
@media (max-width: 640px) {
    .seat { width: 52px; height: 52px; font-size: 17px; border-radius: 9px; }
    .seat-label { font-size: 8px; }
    .blackboard { padding: 9px 32px; font-size: 13px; }
}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
# 상태 초기화
# ────────────────────────────────────────────────────────────────────────────
for _k, _v in {"total": 30, "cols": 6, "excluded": [], "fixed": {}, "result": None, "history": []}.items():
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

    # ── 기본 설정 ──────────────────────────────────────────────
    st.markdown('<span class="sec-head">기본 설정</span>', unsafe_allow_html=True)

    S["total"] = st.slider("총 학생 수", 1, 60, S["total"], 1)
    S["total"] = st.number_input(
        "직접 입력 (1–60)",
        min_value=1, max_value=60,
        value=S["total"], step=1,
        key="total_direct",
    )
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    S["cols"] = st.slider("가로 열 수", 1, 12, S["cols"], 1)
    S["cols"] = st.number_input(
        "직접 입력 (1–12)",
        min_value=1, max_value=12,
        value=S["cols"], step=1,
        key="cols_direct",
    )

    rows_calc = math.ceil(S["total"] / S["cols"])
    st.markdown(
        f'<div style="margin:12px 0 4px;">'
        f'<span class="badge b-blue">{S["cols"]}열</span>'
        f'<span class="badge b-purple">{rows_calc}행</span>'
        f'<span class="badge b-green">{S["total"]}명</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── 제외 번호 ───────────────────────────────────────────────
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
        tags = "".join(f'<span class="tag tag-excl">✕ {n}번</span>' for n in S["excluded"])
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("제외 전체 초기화", key="btn_excl_clr", use_container_width=True):
            S["excluded"] = []
            st.rerun()

    st.markdown("---")

    # ── 자리 고정 ───────────────────────────────────────────────
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
            f'<span class="tag tag-fixed">📌 {num}번→{sidx // S["cols"]+1}행{sidx % S["cols"]+1}열</span>'
            for num, sidx in sorted(S["fixed"].items())
        )
        st.markdown(f'<div class="tag-wrap">{tags}</div>', unsafe_allow_html=True)
        if st.button("고정 전체 초기화", key="btn_fix_clr", use_container_width=True):
            S["fixed"] = {}
            st.rerun()

    st.markdown("---")

    # ── JSON 저장 ───────────────────────────────────────────────
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
# 메인 영역
# ────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;font-size:2rem;font-weight:900;"
    "letter-spacing:-.02em;margin-bottom:4px;color:var(--text)'>🏫 학급 자리 배치기</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;font-size:.9rem;margin-bottom:20px;"
    "color:var(--text2)'>무작위 배치 &nbsp;·&nbsp; 번호 고정 &nbsp;·&nbsp; 제외 설정</p>",
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
    if st.button("↩ 이전 결과", use_container_width=True, disabled=len(S["history"]) <= 1):
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

    html = '<div class="classroom-wrap"><div class="blackboard">📋 &nbsp; 칠 판 &nbsp; ( 앞 )</div><div class="seat-grid">'

    for r in range(rows_n):
        html += '<div class="seat-row">'
        for c in range(cols_n):
            idx = r * cols_n + c
            num = result.get(idx)
            if num is None:
                html += (
                    f'<div class="seat seat-empty">'
                    f'<span style="font-size:18px;opacity:.4">—</span>'
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
    st.markdown(f'<div style="display:flex;justify-content:center">{html}</div>', unsafe_allow_html=True)

    st.markdown("---")

    active_cnt = sum(1 for v in result.values() if v is not None)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("총 학생 수",  f"{S['total']}명")
    s2.metric("배치된 학생", f"{active_cnt}명")
    s3.metric("제외된 학생", f"{len(S['excluded'])}명")
    s4.metric("고정된 자리", f"{len(S['fixed'])}개")

    with st.expander("📋 번호순 자리 목록 보기"):
        table = sorted(
            [(num, sidx // cols_n + 1, sidx % cols_n + 1, "📌 고정" if sidx in fixed_seats else "")
             for sidx, num in result.items()],
            key=lambda x: x[0]
        )
        chunk = math.ceil(len(table) / 3)
        for col_ui, rows_data in zip(
            st.columns(3),
            [table[:chunk], table[chunk:2*chunk], table[2*chunk:]]
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
        <b style="color:var(--accent)">🎲 자리 배치하기</b> 버튼을 눌러주세요</div>
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

import streamlit as st
import random
import math
import json

# ── 페이지 설정 ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="학급 자리 배치기",
    page_icon="🏫",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #22263a;
    --accent: #4f8ef7;
    --accent2: #a78bfa;
    --warn: #f59e0b;
    --danger: #ef4444;
    --success: #10b981;
    --text: #e2e8f0;
    --muted: #64748b;
    --border: #2d3452;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Noto Sans KR', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

h1, h2, h3 { font-family: 'Noto Sans KR', sans-serif !important; }

/* 번호 입력 태그 스타일 */
.tag-container {
    display: flex; flex-wrap: wrap; gap: 6px; margin: 6px 0 10px 0;
}
.tag {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px 3px 12px; border-radius: 999px;
    font-size: 13px; font-weight: 600; cursor: pointer;
    transition: all .15s;
}
.tag-fixed  { background: #1e3a5f; border: 1px solid var(--accent); color: var(--accent); }
.tag-excl   { background: #3b1f1f; border: 1px solid var(--danger); color: var(--danger); }
.tag-fixed:hover  { background: #1a3870; }
.tag-excl:hover   { background: #4a2020; }

/* 자리 그리드 */
.seat-grid { display: flex; flex-direction: column; gap: 10px; margin: 0 auto; }
.seat-row  { display: flex; gap: 10px; justify-content: center; }
.seat {
    width: 64px; height: 64px;
    border-radius: 12px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 900;
    font-family: 'Space Mono', monospace;
    border: 2px solid var(--border);
    transition: transform .15s, box-shadow .15s;
    position: relative;
}
.seat:hover { transform: translateY(-2px); box-shadow: 0 8px 20px #0006; }
.seat-normal { background: var(--surface2); color: var(--text); border-color: var(--border); }
.seat-fixed  { background: #1a3060; color: #93c5fd; border-color: var(--accent); box-shadow: 0 0 0 1px #4f8ef755; }
.seat-empty  { background: #111318; color: var(--muted); border-color: #1e2030; border-style: dashed; }
.seat-label {
    font-size: 9px; font-weight: 600; letter-spacing: .04em;
    position: absolute; bottom: 5px;
    color: rgba(255,255,255,.3);
    font-family: 'Noto Sans KR', sans-serif;
}
.seat-fixed .seat-label { color: #4f8ef799; }

/* 칠판 */
.blackboard {
    background: linear-gradient(135deg, #1a472a 0%, #145a32 100%);
    border: 3px solid #2ecc71;
    border-radius: 12px;
    text-align: center;
    padding: 12px 30px;
    color: #a9dfbf;
    font-size: 16px; font-weight: 700;
    letter-spacing: .1em;
    box-shadow: inset 0 2px 8px #0004, 0 4px 16px #0005;
    margin-bottom: 24px;
}

/* 카드 */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}
.card-title {
    font-size: 13px; font-weight: 700; letter-spacing: .08em;
    color: var(--muted); text-transform: uppercase; margin-bottom: 12px;
}

/* 배지 */
.badge {
    display: inline-block; padding: 2px 10px; border-radius: 999px;
    font-size: 12px; font-weight: 700;
}
.badge-blue   { background: #1e3a5f; color: var(--accent); }
.badge-purple { background: #2d1f5e; color: var(--accent2); }
.badge-green  { background: #0d3b27; color: var(--success); }
.badge-red    { background: #3b1212; color: var(--danger); }

/* 버튼 오버라이드 */
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: 15px !important;
    transition: opacity .2s, transform .15s !important;
}
[data-testid="baseButton-primary"]:hover {
    opacity: .88 !important; transform: translateY(-1px) !important;
}
[data-testid="baseButton-secondary"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
}

/* 입력 필드 */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
.stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* 구분선 */
hr { border-color: var(--border) !important; }

/* 모바일 */
@media (max-width: 640px) {
    .seat { width: 50px; height: 50px; font-size: 16px; border-radius: 9px; }
}
</style>
""", unsafe_allow_html=True)


# ── 상태 초기화 ──────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "total": 30,
        "cols": 6,
        "excluded": [],
        "fixed": {},        # {번호: 자리인덱스}
        "result": None,     # 배치 결과 (자리인덱스 → 번호)
        "history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
S = st.session_state


# ── 헬퍼 ────────────────────────────────────────────────────────────────────
def parse_numbers(text: str, max_n: int) -> list[int]:
    """콤마·공백·줄바꿈으로 구분된 번호 파싱"""
    nums = []
    for tok in text.replace(",", " ").replace("\n", " ").split():
        try:
            n = int(tok)
            if 1 <= n <= max_n:
                nums.append(n)
        except ValueError:
            pass
    return sorted(set(nums))


def total_seats():
    return math.ceil(S["total"] / S["cols"]) * S["cols"]


def arrange():
    n_total = S["total"]
    cols = S["cols"]
    rows = math.ceil(n_total / cols)
    seats = rows * cols          # 전체 칸 (빈 칸 포함)

    excluded = set(S["excluded"])
    fixed = S["fixed"]           # {번호: 좌석인덱스}

    # 유효한 번호 범위
    active = [i for i in range(1, n_total + 1) if i not in excluded]

    # 고정 번호 검증
    for num, seat_idx in list(fixed.items()):
        if num not in active or seat_idx >= seats:
            del S["fixed"][num]
    fixed = S["fixed"]

    # 고정 번호가 이미 배치할 좌석
    assigned = {}   # seat_idx → 번호
    for num, seat_idx in fixed.items():
        assigned[seat_idx] = num

    # 나머지 번호 섞어서 빈 자리에 배치
    free_nums = [n for n in active if n not in fixed]
    free_seats = [s for s in range(seats) if s not in assigned]

    # 학생 수보다 빈 자리가 더 많을 수 있음 (마지막 줄 빈 칸)
    random.shuffle(free_nums)

    for i, num in enumerate(free_nums):
        if i < len(free_seats):
            assigned[free_seats[i]] = num

    S["result"] = assigned
    S["history"].insert(0, dict(assigned))
    if len(S["history"]) > 5:
        S["history"] = S["history"][:5]


# ── 사이드바 ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    st.markdown("---")

    # 기본 설정
    st.markdown('<div class="card-title">기본 설정</div>', unsafe_allow_html=True)
    S["total"] = st.number_input("총 학생 수", min_value=1, max_value=60, value=S["total"], step=1)
    S["cols"] = st.number_input("가로 줄 수 (열)", min_value=1, max_value=12, value=S["cols"], step=1)

    rows_calc = math.ceil(S["total"] / S["cols"])
    st.markdown(
        f'<span class="badge badge-blue">{S["cols"]}열</span> '
        f'<span class="badge badge-purple">{rows_calc}행</span> '
        f'<span class="badge badge-green">총 {S["total"]}명</span>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # 제외 번호
    st.markdown('<div class="card-title">🚫 제외할 번호</div>', unsafe_allow_html=True)
    excl_input = st.text_input(
        "번호 입력 (콤마 또는 공백으로 구분)",
        key="excl_input",
        placeholder="예: 1, 5, 12",
        label_visibility="collapsed",
    )
    if st.button("추가", key="btn_excl", use_container_width=True):
        nums = parse_numbers(excl_input, S["total"])
        for n in nums:
            if n not in S["excluded"]:
                S["excluded"].append(n)
                # 고정에서도 제거
                S["fixed"].pop(n, None)
        S["excluded"].sort()
        st.rerun()

    if S["excluded"]:
        tags_html = '<div class="tag-container">'
        for n in S["excluded"]:
            tags_html += f'<span class="tag tag-excl">✕ {n}번</span>'
        tags_html += "</div>"
        st.markdown(tags_html, unsafe_allow_html=True)
        if st.button("전체 초기화", key="btn_excl_clear", use_container_width=True):
            S["excluded"] = []
            st.rerun()

    st.markdown("---")

    # 고정 번호 (특정 번호를 특정 자리에 고정)
    st.markdown('<div class="card-title">📌 자리 고정</div>', unsafe_allow_html=True)
    st.caption("번호와 자리 위치(행, 열)를 지정합니다.")

    fix_cols = st.columns([2, 2, 2])
    with fix_cols[0]:
        fix_num = st.number_input("번호", min_value=1, max_value=S["total"], value=1, step=1, key="fix_num")
    with fix_cols[1]:
        fix_row = st.number_input("행", min_value=1, max_value=rows_calc, value=1, step=1, key="fix_row")
    with fix_cols[2]:
        fix_col = st.number_input("열", min_value=1, max_value=S["cols"], value=1, step=1, key="fix_col")

    if st.button("고정 추가", key="btn_fix", use_container_width=True):
        seat_idx = (fix_row - 1) * S["cols"] + (fix_col - 1)
        # 같은 자리에 다른 번호가 있으면 제거
        S["fixed"] = {k: v for k, v in S["fixed"].items() if v != seat_idx}
        S["fixed"][fix_num] = seat_idx
        if fix_num in S["excluded"]:
            S["excluded"].remove(fix_num)
        st.rerun()

    if S["fixed"]:
        tags_html = '<div class="tag-container">'
        cols_n = S["cols"]
        for num, sidx in sorted(S["fixed"].items()):
            r = sidx // cols_n + 1
            c = sidx % cols_n + 1
            tags_html += f'<span class="tag tag-fixed">📌 {num}번 → {r}행{c}열</span>'
        tags_html += "</div>"
        st.markdown(tags_html, unsafe_allow_html=True)
        if st.button("고정 전체 초기화", key="btn_fix_clear", use_container_width=True):
            S["fixed"] = {}
            st.rerun()

    st.markdown("---")

    # JSON 내보내기
    if S["result"]:
        config = {
            "total": S["total"],
            "cols": S["cols"],
            "excluded": S["excluded"],
            "fixed": {str(k): v for k, v in S["fixed"].items()},
        }
        st.download_button(
            "⬇ 설정 저장 (JSON)",
            data=json.dumps(config, ensure_ascii=False, indent=2),
            file_name="seating_config.json",
            mime="application/json",
            use_container_width=True,
        )


# ── 메인 영역 ────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;font-size:2rem;font-weight:900;margin-bottom:4px;'>"
    "🏫 학급 자리 배치기</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#64748b;font-size:.95rem;margin-bottom:24px;'>"
    "무작위 자리 배치 · 특정 번호 고정 · 제외 설정</p>",
    unsafe_allow_html=True,
)

# 버튼 행
b1, b2, b3 = st.columns([3, 2, 2])
with b1:
    if st.button("🎲 자리 배치하기", type="primary", use_container_width=True):
        arrange()
        st.rerun()
with b2:
    if st.button("🔄 초기화", use_container_width=True):
        S["result"] = None
        st.rerun()
with b3:
    if S["history"] and len(S["history"]) > 1:
        if st.button("↩ 이전 결과", use_container_width=True):
            S["history"].pop(0)
            S["result"] = S["history"][0] if S["history"] else None
            st.rerun()

st.markdown("---")

# ── 자리 그리드 출력 ─────────────────────────────────────────────────────────
if S["result"] is not None:
    result = S["result"]
    cols_n = S["cols"]
    rows_n = math.ceil(S["total"] / cols_n)
    seats = rows_n * cols_n
    fixed_seats = set(S["fixed"].values())

    # 칠판
    st.markdown('<div class="blackboard">📋 칠판 (앞)</div>', unsafe_allow_html=True)

    # 그리드 HTML 생성
    grid_html = '<div class="seat-grid">'
    for r in range(rows_n):
        grid_html += '<div class="seat-row">'
        for c in range(cols_n):
            idx = r * cols_n + c
            num = result.get(idx)
            if num is None:
                # 빈 칸
                grid_html += (
                    f'<div class="seat seat-empty" title="빈 자리">'
                    f'<span style="font-size:22px;color:#2d3452">○</span>'
                    f'<span class="seat-label">{r+1}행{c+1}열</span></div>'
                )
            elif idx in fixed_seats:
                grid_html += (
                    f'<div class="seat seat-fixed" title="{num}번 (고정)">'
                    f'{num}'
                    f'<span class="seat-label">📌고정</span></div>'
                )
            else:
                grid_html += (
                    f'<div class="seat seat-normal" title="{num}번 | {r+1}행 {c+1}열">'
                    f'{num}'
                    f'<span class="seat-label">{r+1}행{c+1}열</span></div>'
                )
        grid_html += "</div>"
    grid_html += "</div>"

    # 가운데 정렬
    st.markdown(
        f'<div style="display:flex;justify-content:center;">{grid_html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # 요약 통계
    active_cnt = len([v for v in result.values() if v is not None])
    empty_cnt = seats - active_cnt
    fixed_cnt = len(S["fixed"])

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("총 학생 수", f"{S['total']}명")
    with s2:
        st.metric("배치된 학생", f"{active_cnt}명")
    with s3:
        st.metric("제외된 학생", f"{len(S['excluded'])}명")
    with s4:
        st.metric("고정된 자리", f"{fixed_cnt}개")

    # 번호 순 목록
    with st.expander("📋 번호순 자리 목록 보기"):
        table_data = []
        for sidx, num in sorted(result.items(), key=lambda x: x[1]):
            r = sidx // cols_n + 1
            c = sidx % cols_n + 1
            fixed_mark = "📌 고정" if sidx in fixed_seats else ""
            table_data.append({"번호": num, "행": r, "열": c, "비고": fixed_mark})
        # 번호순 정렬
        table_data.sort(key=lambda x: x["번호"])

        # 3열 레이아웃으로 표시
        chunk = math.ceil(len(table_data) / 3)
        tc1, tc2, tc3 = st.columns(3)
        for col_ui, chunk_data in zip(
            [tc1, tc2, tc3],
            [table_data[:chunk], table_data[chunk:2*chunk], table_data[2*chunk:]],
        ):
            with col_ui:
                for row in chunk_data:
                    badge = "🔵" if row["비고"] else "⚪"
                    st.markdown(
                        f"{badge} **{row['번호']}번** — {row['행']}행 {row['열']}열 {row['비고']}",
                        unsafe_allow_html=False,
                    )

else:
    # 안내 화면
    st.markdown(
        """
        <div style="
            text-align:center; padding: 80px 20px;
            border: 2px dashed #2d3452; border-radius: 20px;
            color: #64748b;
        ">
            <div style="font-size: 60px; margin-bottom: 16px;">🪑</div>
            <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 8px; color:#94a3b8;">
                아직 자리가 배치되지 않았습니다
            </div>
            <div style="font-size: .9rem;">
                왼쪽 사이드바에서 설정 후<br>
                <b style="color:#4f8ef7">🎲 자리 배치하기</b> 버튼을 눌러주세요
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 사용법 카드
    st.markdown("<br>", unsafe_allow_html=True)
    u1, u2, u3 = st.columns(3)
    cards = [
        ("🔢", "총 인원 설정", "학생 수와 열(가로줄) 수를 설정하면 자동으로 행이 계산됩니다."),
        ("🚫", "번호 제외", "결석, 전학 등 배치에서 제외할 번호를 입력합니다."),
        ("📌", "자리 고정", "특정 번호를 지정한 행·열에 고정 배치합니다."),
    ]
    for col_ui, (icon, title, desc) in zip([u1, u2, u3], cards):
        with col_ui:
            st.markdown(
                f"""<div class="card">
                    <div style="font-size:2rem;margin-bottom:8px;">{icon}</div>
                    <div style="font-weight:700;font-size:1rem;margin-bottom:6px;">{title}</div>
                    <div style="color:#64748b;font-size:.85rem;">{desc}</div>
                </div>""",
                unsafe_allow_html=True,
            )

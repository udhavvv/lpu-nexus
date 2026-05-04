import streamlit as st
import google.generativeai as genai
import os
import json
import base64
import random
from datetime import datetime

st.set_page_config(
    page_title="LPU Nexus",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

:root {
    --bg: #07070f;
    --surface: #0f0f1a;
    --surface2: #161625;
    --surface3: #1e1e32;
    --border: #ffffff12;
    --border2: #ffffff1e;
    --accent: #7c6dfa;
    --accent2: #00e5a0;
    --accent3: #ff6b6b;
    --gold: #ffd166;
    --pink: #f72585;
    --blue: #4cc9f0;
    --text: #f0f0fa;
    --muted: #9090b0;
    --card-glow: 0 0 0 1px #ffffff0a, 0 4px 24px #0000004d;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg) !important; color: var(--text); }
.stApp { background: var(--bg) !important; }

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
    padding-top: 0 !important;
}

section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

.main .block-container { padding-top: 1.5rem; max-width: 1100px; }

h1,h2,h3,h4 { font-family: 'Syne', sans-serif; color: var(--text); }

/* ── Sidebar gradient header ── */
.sidebar-header {
    background: linear-gradient(135deg, #1a1535 0%, #0f1628 100%);
    border-bottom: 1px solid var(--border);
    padding: 20px 16px 16px;
    margin-bottom: 8px;
}

.nexus-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #fff 0%, #a29cff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.nexus-tagline { font-size: 0.72rem; color: var(--muted); margin-top: 2px; }

/* ── Profile pic circle ── */
.profile-pic-wrap {
    width: 52px; height: 52px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--pink));
    padding: 2px; margin-bottom: 10px; flex-shrink: 0;
}
.profile-pic-inner {
    width: 100%; height: 100%; border-radius: 50%;
    background: var(--surface2);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif; font-weight: 700;
    font-size: 1.1rem; color: var(--text); overflow: hidden;
}
.profile-pic-inner img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }

/* ── Nav buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.2s !important;
    margin-bottom: 3px !important;
}
.stButton > button:hover {
    background: var(--surface2) !important;
    border-color: var(--accent) !important;
    color: var(--text) !important;
}

/* ── Cards ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: var(--card-glow);
    transition: border-color 0.2s, transform 0.2s;
    position: relative; overflow: hidden;
}
.card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, #ffffff20, transparent);
}
.card:hover { border-color: var(--border2); transform: translateY(-1px); }
.card.glow { border-color: #7c6dfa44; }
.card.glow-green { border-color: #00e5a044; }
.card.glow-pink { border-color: #f7258544; }
.card.glow-gold { border-color: #ffd16644; }

/* ── Stat cards ── */
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 16px; }
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    text-align: center;
    box-shadow: var(--card-glow);
    position: relative; overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 40%; height: 2px; border-radius: 2px;
    background: var(--accent);
}
.stat-val { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 700; line-height: 1.1; }
.stat-label { font-size: 0.7rem; color: var(--muted); margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── Badges ── */
.badge { display: inline-block; padding: 3px 10px; border-radius: 100px; font-size: 0.7rem; font-weight: 600; margin-right: 4px; letter-spacing: 0.3px; }
.badge-purple { background: #2d2b5a; color: #a29cff; border: 1px solid #4a45a020; }
.badge-green  { background: #0d2e22; color: #00e5a0; border: 1px solid #00e5a020; }
.badge-red    { background: #2e1515; color: #ff6b6b; border: 1px solid #ff6b6b20; }
.badge-gold   { background: #2e2510; color: #ffd166; border: 1px solid #ffd16620; }
.badge-pink   { background: #2e0f1e; color: #f72585; border: 1px solid #f7258520; }
.badge-blue   { background: #0f1e2e; color: #4cc9f0; border: 1px solid #4cc9f020; }

/* ── Progress bar ── */
.prog-wrap { background: var(--surface3); border-radius: 8px; height: 10px; overflow: hidden; margin: 8px 0; }
.prog-fill { height: 10px; border-radius: 8px; transition: width 0.6s cubic-bezier(.4,0,.2,1); }

/* ── Chat bubbles ── */
.chat-user {
    background: linear-gradient(135deg, #6c63ff, #8b80ff);
    color: white; border-radius: 18px 18px 4px 18px;
    padding: 12px 16px; margin: 8px 0; margin-left: 15%;
    font-size: 0.88rem; line-height: 1.55;
    box-shadow: 0 4px 16px #6c63ff40;
}
.chat-ai {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px; margin: 8px 0; margin-right: 15%;
    font-size: 0.88rem; line-height: 1.55;
    position: relative;
}
.chat-ai::before {
    content: '⚡';
    font-size: 0.7rem;
    position: absolute; top: -8px; left: 10px;
    background: var(--accent); border-radius: 50%;
    width: 18px; height: 18px;
    display: flex; align-items: center; justify-content: center;
}

/* ── AI response box ── */
.ai-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 0.88rem; line-height: 1.7;
    color: var(--text); margin-top: 12px;
    animation: fadeIn 0.4s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

/* ── Challenge card ── */
.challenge-card {
    background: linear-gradient(135deg, #13132a 0%, #1a1040 100%);
    border: 1px solid #7c6dfa44;
    border-radius: 16px; padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 0 40px #7c6dfa15;
}
.challenge-q { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; color: var(--text); line-height: 1.5; }

/* ── Leaderboard ── */
.lb-row {
    display: flex; align-items: center; gap: 12px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 12px 16px; margin-bottom: 6px;
    transition: border-color 0.2s;
}
.lb-row:hover { border-color: var(--border2); }
.lb-rank { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; width: 28px; text-align: center; }
.lb-avatar { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; flex-shrink: 0; }
.lb-name { flex: 1; font-weight: 500; font-size: 0.9rem; }
.lb-branch { font-size: 0.75rem; color: var(--muted); }
.lb-xp { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; }

/* ── Tribe card ── */
.tribe-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px; padding: 16px;
    margin-bottom: 10px; transition: all 0.2s;
}
.tribe-card:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 32px #7c6dfa20; }

/* ── Skill DNA bars ── */
.skill-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.skill-name { width: 120px; font-size: 0.82rem; color: var(--muted); flex-shrink: 0; }
.skill-bar-wrap { flex: 1; background: var(--surface3); border-radius: 6px; height: 8px; overflow: hidden; }
.skill-bar-fill { height: 8px; border-radius: 6px; }
.skill-pct { width: 36px; text-align: right; font-size: 0.78rem; font-weight: 600; }

/* ── Module grid ── */
.mod-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap: 10px; margin-bottom: 16px; }
.mod-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 16px;
    cursor: pointer; transition: all 0.2s;
    position: relative; overflow: hidden;
}
.mod-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.mod-card.c1::before { background: var(--accent); }
.mod-card.c2::before { background: var(--accent2); }
.mod-card.c3::before { background: var(--gold); }
.mod-card.c4::before { background: var(--pink); }
.mod-card.c5::before { background: var(--blue); }
.mod-card.c6::before { background: #ff9f43; }
.mod-card.c7::before { background: #a29bfe; }
.mod-card:hover { border-color: var(--border2); transform: translateY(-2px); box-shadow: 0 8px 32px #00000040; }
.mod-icon { font-size: 1.6rem; margin-bottom: 8px; }
.mod-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: var(--text); margin-bottom: 4px; }
.mod-desc { font-size: 0.75rem; color: var(--muted); line-height: 1.5; }

/* ── Section heading ── */
.sec-head {
    font-family: 'Syne', sans-serif; font-weight: 700;
    font-size: 1rem; color: var(--text);
    display: flex; align-items: center; gap: 8px;
    margin: 18px 0 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

/* ── Encrypted badge ── */
.enc-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: #0d2e22; color: #00e5a0;
    border: 1px solid #00e5a030; border-radius: 100px;
    font-size: 0.68rem; font-weight: 600; padding: 2px 10px;
    letter-spacing: 0.3px;
}

/* ── Form inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important; border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stSelectbox > div > div { background: var(--surface2) !important; border: 1px solid var(--border2) !important; border-radius: 10px !important; }
.stMultiSelect > div > div { background: var(--surface2) !important; border: 1px solid var(--border2) !important; border-radius: 10px !important; }
label, .stSlider label { color: var(--muted) !important; font-size: 0.82rem !important; }
.stRadio > label { color: var(--text) !important; }
.stTabs [data-baseweb="tab"] { color: var(--muted) !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
.stTabs [aria-selected="true"] { color: var(--text) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--accent) !important; }
.stTabs [data-baseweb="tab-border"] { background: var(--border) !important; }

/* ── Page hero ── */
.page-hero {
    background: linear-gradient(135deg, #13132a 0%, #1a0f2e 50%, #0f1a2e 100%);
    border: 1px solid var(--border); border-radius: 20px;
    padding: 24px 28px; margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.page-hero::after {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 160px; height: 160px; border-radius: 50%;
    background: radial-gradient(circle, #7c6dfa20, transparent 70%);
}
.page-hero-title { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800; margin-bottom: 4px; }
.page-hero-sub { font-size: 0.85rem; color: var(--muted); }
</style>
""", unsafe_allow_html=True)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY",""))
gemini = genai.GenerativeModel("gemini-1.5-flash")

# ── Session state ──────────────────────────────────────
defaults = {
    "page": "home", "profile": {}, "profile_pic": None,
    "ai_messages": [], "arena_score": 0, "streak": 0,
    "answered": False, "current_q": None,
    "acad_analysis": "", "skill_dna": {},
    "mindspace_msgs": [], "project_posts": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ────────────────────────────────────────────
def ask_claude(prompt, system=None, max_tokens=700):
    full_prompt = (system + "\n\n" + prompt) if system else prompt
    resp = gemini.generate_content(full_prompt)
    return resp.text

def ask_claude_chat(messages, system=None, max_tokens=600):
    history = []
    for m in messages[:-1]:
        role = "user" if m["role"] == "user" else "model"
        history.append({"role": role, "parts": [m["content"]]})
    last = messages[-1]["content"]
    chat = gemini.start_chat(history=history)
    sys_prefix = (system + "\n\n") if system else ""
    resp = chat.send_message(sys_prefix + last)
    return resp.text

def profile_pic_html(size=52, font_size="1.1rem"):
    p = st.session_state.profile
    name = p.get("name","?") if p else "?"
    initials = "".join([w[0].upper() for w in name.split()[:2]]) if name != "?" else "?"
    if st.session_state.profile_pic:
        img_b64 = base64.b64encode(st.session_state.profile_pic).decode()
        inner = f'<img src="data:image/jpeg;base64,{img_b64}" />'
    else:
        inner = f'<span style="font-size:{font_size}">{initials}</span>'
    return f'<div class="profile-pic-wrap" style="width:{size}px;height:{size}px"><div class="profile-pic-inner">{inner}</div></div>'

def nav_button(label, key, icon=""):
    active_style = "border-color: var(--accent) !important; color: var(--text) !important; background: var(--surface2) !important;" if st.session_state.page == key else ""
    if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
        st.session_state.page = key; st.rerun()

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <div class="nexus-logo">LPU Nexus</div>
        <div class="nexus-tagline">Your campus. Supercharged by AI.</div>
    </div>""", unsafe_allow_html=True)

    p = st.session_state.profile
    if p and p.get("name"):
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:12px 16px 4px;">
            {profile_pic_html(42,"0.9rem")}
            <div>
                <div style="font-weight:600;font-size:0.88rem;color:#f0f0fa;">{p.get('name','')}</div>
                <div style="font-size:0.72rem;color:#7c6dfa;">{p.get('branch','—')} · Sem {p.get('sem','—')}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:8px 16px;font-size:0.75rem;color:#9090b0;">Set up your profile ↓</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:4px 10px;">', unsafe_allow_html=True)
    nav_button("Home", "home", "🏠")
    nav_button("My Profile", "profile", "👤")
    st.markdown('<div style="font-size:0.68rem;color:#9090b0;padding:8px 4px 4px;letter-spacing:0.5px;text-transform:uppercase;">Academics</div>', unsafe_allow_html=True)
    nav_button("AcadRadar", "acad", "📊")
    nav_button("SkillDNA", "skilldna", "🧬")
    nav_button("FirstSem AI", "firstsem", "🎓")
    st.markdown('<div style="font-size:0.68rem;color:#9090b0;padding:8px 4px 4px;letter-spacing:0.5px;text-transform:uppercase;">Skills & Social</div>', unsafe_allow_html=True)
    nav_button("SkillForge", "arena", "⚡")
    nav_button("CampusConnect", "tribe", "🤝")
    nav_button("ProjectHive", "projecthive", "🐝")
    nav_button("AskTeacher", "askteacher", "🧑‍🏫")
    st.markdown('<div style="font-size:0.68rem;color:#9090b0;padding:8px 4px 4px;letter-spacing:0.5px;text-transform:uppercase;">Wellbeing</div>', unsafe_allow_html=True)
    nav_button("MindSpace", "mindspace", "🫧")
    nav_button("Nexus AI", "ai", "🤖")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="padding:0 12px 12px;display:flex;align-items:center;gap:8px;">
        <div style="font-size:0.72rem;color:#9090b0;">Arena XP:</div>
        <div style="font-family:'Syne',sans-serif;font-weight:700;color:#ffd166;font-size:0.9rem;">{st.session_state.arena_score} ⚡</div>
        <div style="font-size:0.72rem;color:#ff6b6b;margin-left:auto;">{st.session_state.streak}🔥</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    p = st.session_state.profile
    name = p.get("name","Student") if p else "Student"

    st.markdown(f"""
    <div class="page-hero">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
            {profile_pic_html(56,"1.2rem")}
            <div>
                <div class="page-hero-title">Hey, {name} 👋</div>
                <div class="page-hero-sub">Welcome to LPU Nexus — your AI-powered campus companion</div>
            </div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
            <span class="badge badge-purple">AI Powered</span>
            <span class="badge badge-green">40K+ Students</span>
            <span class="badge badge-gold">LPU Campus</span>
            <span class="badge badge-blue">9 Modules</span>
        </div>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:var(--accent);">40K+</div><div class="stat-label">LPU Students</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:var(--gold);">{st.session_state.arena_score}</div><div class="stat-label">Your XP</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:var(--accent3);">{st.session_state.streak}🔥</div><div class="stat-label">Streak</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:var(--accent2);">9</div><div class="stat-label">Modules</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">🧭 All Modules</div>', unsafe_allow_html=True)

    modules = [
        ("📊","AcadRadar","acad","c1","Track attendance, backlogs & get AI rescue plan"),
        ("🧬","SkillDNA","skilldna","c2","Discover your real skills beyond CGPA"),
        ("🎓","FirstSem AI","firstsem","c3","Are you in the right course? Find out early"),
        ("⚡","SkillForge","arena","c4","Daily challenges · XP · Campus leaderboard"),
        ("🤝","CampusConnect","tribe","c5","Find your people, project partners & mentors"),
        ("🐝","ProjectHive","projecthive","c6","Post ideas · Build teams · Ship projects"),
        ("🧑‍🏫","AskTeacher","askteacher","c7","Find the right teacher for your exact doubt"),
        ("🫧","MindSpace","mindspace","c1","Safe space · Stress support · Anonymous"),
        ("🤖","Nexus AI","ai","c2","Your personal AI that knows LPU inside out"),
    ]

    cols = st.columns(3)
    for i,(icon,name_m,page,col,desc) in enumerate(modules):
        with cols[i%3]:
            st.markdown(f"""
            <div class="mod-card {col}">
                <div class="mod-icon">{icon}</div>
                <div class="mod-name">{name_m}</div>
                <div class="mod-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open {name_m}", key=f"home_{page}", use_container_width=True):
                st.session_state.page = page; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PROFILE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "profile":
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">👤 My Profile</div>
        <div class="page-hero-sub">Your identity across all LPU Nexus modules</div>
    </div>""", unsafe_allow_html=True)

    col_pic, col_form = st.columns([1,3])
    with col_pic:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        st.markdown(f'<div style="display:flex;justify-content:center;margin-bottom:10px;">{profile_pic_html(90,"1.8rem")}</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload photo", type=["jpg","jpeg","png"], label_visibility="collapsed")
        if uploaded:
            st.session_state.profile_pic = uploaded.read()
            st.rerun()
        st.markdown('<div style="font-size:0.72rem;color:#9090b0;text-align:center;margin-top:4px;">JPG or PNG</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_form:
        with st.form("profile_form"):
            c1,c2 = st.columns(2)
            with c1:
                name     = st.text_input("Full Name", value=st.session_state.profile.get("name",""))
                roll     = st.text_input("Roll Number", value=st.session_state.profile.get("roll",""))
                branch   = st.selectbox("Branch",["CSE","ECE","ME","Civil","MBA","BCA","B.Sc","EEE","IT","Other"],
                                        index=["CSE","ECE","ME","Civil","MBA","BCA","B.Sc","EEE","IT","Other"].index(st.session_state.profile.get("branch","CSE")))
                sem      = st.selectbox("Semester",list(range(1,9)),index=st.session_state.profile.get("sem",1)-1)
            with c2:
                cgpa     = st.slider("CGPA",0.0,10.0,float(st.session_state.profile.get("cgpa",7.0)),0.1)
                attend   = st.slider("Attendance %",0,100,int(st.session_state.profile.get("attend",75)))
                backlogs = st.number_input("Active Backlogs",0,20,int(st.session_state.profile.get("backlogs",0)))
                year     = st.selectbox("Year",["1st Year","2nd Year","3rd Year","4th Year"],index=st.session_state.profile.get("year_idx",0))

            interests = st.multiselect("Interests",["Coding","Gaming","AI/ML","Web Dev","App Dev","Design","Music","Sports","Startup","Research","Open Source","Data Science","Cybersecurity","Robotics"],default=st.session_state.profile.get("interests",[]))
            skills    = st.text_area("Your Skills (comma separated)",value=st.session_state.profile.get("skills",""))
            goal      = st.text_area("Your goal after LPU",value=st.session_state.profile.get("goal",""))
            hostel    = st.text_input("Hostel / Block (optional)",value=st.session_state.profile.get("hostel",""))

            if st.form_submit_button("Save Profile ✓", use_container_width=True):
                st.session_state.profile = {
                    "name":name,"roll":roll,"branch":branch,"sem":sem,
                    "cgpa":cgpa,"attend":attend,"backlogs":backlogs,
                    "interests":interests,"skills":skills,"goal":goal,
                    "hostel":hostel,"year_idx":["1st Year","2nd Year","3rd Year","4th Year"].index(year)
                }
                st.success("Profile saved! All modules are now personalised. ✅")


# ══════════════════════════════════════════════════════════════════════════════
# ACADRADAR
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "acad":
    p = st.session_state.profile
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">📊 AcadRadar</div>
        <div class="page-hero-sub">Your academic pulse — attendance, backlogs, reappear, and your AI rescue plan</div>
    </div>""", unsafe_allow_html=True)

    if not p:
        st.warning("Set up your profile first.")
        if st.button("Go to Profile"): st.session_state.page="profile"; st.rerun()
    else:
        attend=p.get("attend",75); backlogs=p.get("backlogs",0); cgpa=p.get("cgpa",7.0)
        sem=p.get("sem",1); branch=p.get("branch","CSE")

        if attend<60:     rc,rl="#ff6b6b","CRITICAL ⚠️"
        elif attend<75:   rc,rl="#ffd166","AT RISK 🟡"
        else:             rc,rl="#00e5a0","SAFE ✅"

        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:{rc}">{attend}%</div><div class="stat-label">Attendance</div></div>',unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:{"#ff6b6b" if backlogs>0 else "#00e5a0"}">{backlogs}</div><div class="stat-label">Backlogs</div></div>',unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:{"#ffd166" if cgpa<7 else "#00e5a0"}">{cgpa}</div><div class="stat-label">CGPA</div></div>',unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:{rc};font-size:1rem;">{rl}</div><div class="stat-label">Status</div></div>',unsafe_allow_html=True)

        st.markdown('<div class="sec-head">📈 Attendance Analysis</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="prog-wrap"><div class="prog-fill" style="width:{attend}%;background:{rc};"></div></div>',unsafe_allow_html=True)

        classes_left=st.slider("Classes remaining this semester",10,80,30)
        cur_classes=100
        needed_att=int(0.75*(cur_classes+classes_left))
        cur_att=int(attend/100*cur_classes)
        must_attend=max(0,needed_att-cur_att)
        can_miss=max(0,classes_left-must_attend)

        c1,c2,c3=st.columns(3)
        with c1: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#00e5a0;">{can_miss}</div><div class="stat-label">Can Miss</div></div>',unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ffd166;">{must_attend}</div><div class="stat-label">Must Attend</div></div>',unsafe_allow_html=True)
        with c3:
            proj_att=int((cur_att+classes_left)/( cur_classes+classes_left)*100)
            st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:{"#00e5a0" if proj_att>=75 else "#ff6b6b"}">{proj_att}%</div><div class="stat-label">Projected</div></div>',unsafe_allow_html=True)

        if backlogs>0:
            st.markdown('<div class="sec-head">📋 Reappear / Improvement Tracker</div>',unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card glow">
                <div style="display:flex;gap:10px;align-items:center;margin-bottom:8px;">
                    <span class="badge badge-red">🔴 {backlogs} Active Backlog{'s' if backlogs>1 else ''}</span>
                    <span class="badge badge-gold">Reappear Eligible</span>
                </div>
                <div style="font-size:0.85rem;color:#9090b0;line-height:1.6;">
                    LPU allows reappear exams for failed subjects. Check UMS portal for schedule.
                    Improvement exams are available if you scored below your target grade.
                    <b style="color:#f0f0fa;">Recommended:</b> Contact your mentor teacher immediately.
                </div>
            </div>""",unsafe_allow_html=True)

        st.markdown('<div class="sec-head">🤖 AI Semester Rescue Plan</div>',unsafe_allow_html=True)
        if st.button("⚡ Generate My Personalised Plan", use_container_width=True):
            with st.spinner("Nexus AI is analysing your academic situation..."):
                plan=ask_claude(f"""You are Nexus AI — a caring, direct academic advisor for LPU students.

Student: {branch} Sem {sem} | Attendance: {attend}% | Backlogs: {backlogs} | CGPA: {cgpa}
Classes remaining: {classes_left} | Must attend: {must_attend} | Can miss: {can_miss}
Goal: {p.get('goal','Not specified')}

Write a personalised semester rescue plan. Be honest, warm, and actionable. Cover:
1. Top 3 immediate actions THIS WEEK
2. Attendance recovery strategy  
3. Backlog clearance plan (if any)
4. Daily study schedule suggestion
5. One powerful motivating insight for this student specifically

Speak like a caring senior who's been through it. No fluff.""")
                st.session_state.acad_analysis=plan
        if st.session_state.acad_analysis:
            st.markdown(f'<div class="ai-box">{st.session_state.acad_analysis.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SKILL DNA
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "skilldna":
    p=st.session_state.profile
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">🧬 SkillDNA</div>
        <div class="page-hero-sub">Your real skills mapped — beyond CGPA. What you're actually good at.</div>
    </div>""",unsafe_allow_html=True)

    branch=p.get("branch","CSE") if p else "CSE"
    skills_raw=p.get("skills","") if p else ""
    interests=p.get("interests",[]) if p else []

    st.markdown('<div class="sec-head">🎯 Quick Skill Assessment</div>',unsafe_allow_html=True)

    with st.form("skill_assess"):
        q1=st.selectbox("How comfortable are you with coding?",["Beginner — just started","Intermediate — can build small projects","Advanced — can solve complex problems","Expert — can mentor others"])
        q2=st.selectbox("How strong is your communication?",["Needs work","Okay in class","Confident presenter","Strong leader"])
        q3=st.selectbox("Project experience?",["None yet","1 college project","2-3 projects","Internship / real-world project"])
        q4=st.multiselect("Technologies you've used:",["Python","Java","C++","JavaScript","React","Flutter","SQL","ML/AI","Arduino","Figma","Unity"])
        q5=st.selectbox("Aptitude / Problem solving:",["Struggling","Average","Good","Very strong"])
        submitted=st.form_submit_button("🧬 Analyse My SkillDNA", use_container_width=True)

    if submitted:
        with st.spinner("AI mapping your skill genome..."):
            dna=ask_claude(f"""Analyse this LPU {branch} student's skills and return ONLY a JSON object:

Profile: {q1} | Communication: {q2} | Projects: {q3} | Tech: {q4} | Aptitude: {q5}
Listed skills: {skills_raw} | Interests: {interests}

Return EXACTLY this JSON (scores 0-100):
{{"coding":70,"communication":60,"aptitude":65,"teamwork":75,"creativity":55,"domain_knowledge":68,
"strengths":["strength1","strength2","strength3"],
"gaps":["gap1","gap2"],
"archetype":"The Builder",
"archetype_desc":"one sentence describing this student type",
"next_steps":["action1","action2","action3"]}}""",max_tokens=400)
            try:
                raw=dna.strip().replace("```json","").replace("```","").strip()
                st.session_state.skill_dna=json.loads(raw)
            except:
                st.session_state.skill_dna={"coding":65,"communication":60,"aptitude":70,"teamwork":75,"creativity":55,"domain_knowledge":68,"strengths":["Problem solving","Team player","Curious learner"],"gaps":["Public speaking","Advanced DSA"],"archetype":"The Explorer","archetype_desc":"Someone discovering their strengths with huge untapped potential.","next_steps":["Practice 1 LeetCode problem daily","Join a student club","Build one small project this month"]}

    if st.session_state.skill_dna:
        dna=st.session_state.skill_dna
        st.markdown('<div class="sec-head">🧬 Your Skill Genome</div>',unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card glow" style="margin-bottom:16px;">
            <div style="display:flex;align-items:center;gap:14px;">
                <div style="width:52px;height:52px;border-radius:12px;background:linear-gradient(135deg,var(--accent),var(--pink));display:flex;align-items:center;justify-content:center;font-size:1.4rem;">🧬</div>
                <div>
                    <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;color:#f0f0fa;">{dna.get('archetype','The Explorer')}</div>
                    <div style="font-size:0.82rem;color:#9090b0;margin-top:2px;">{dna.get('archetype_desc','')}</div>
                </div>
            </div>
        </div>""",unsafe_allow_html=True)

        skills_map=[("Coding 💻","coding","#7c6dfa"),("Communication 🗣️","communication","#00e5a0"),("Aptitude 🧠","aptitude","#ffd166"),("Teamwork 🤝","teamwork","#4cc9f0"),("Creativity 🎨","creativity","#f72585"),("Domain Knowledge 📚","domain_knowledge","#ff9f43")]
        for label,key,color in skills_map:
            val=dna.get(key,50)
            st.markdown(f"""
            <div class="skill-row">
                <div class="skill-name">{label}</div>
                <div class="skill-bar-wrap"><div class="skill-bar-fill" style="width:{val}%;background:{color};"></div></div>
                <div class="skill-pct" style="color:{color};">{val}%</div>
            </div>""",unsafe_allow_html=True)

        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="card glow-green"><div style="font-weight:600;margin-bottom:8px;color:#00e5a0;">💪 Your Strengths</div>'+"".join([f'<div style="font-size:0.82rem;color:#f0f0fa;padding:4px 0;border-bottom:1px solid #ffffff08;">✅ {s}</div>' for s in dna.get("strengths",[])])+"</div>",unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card glow"><div style="font-weight:600;margin-bottom:8px;color:#7c6dfa;">🎯 Focus Areas</div>'+"".join([f'<div style="font-size:0.82rem;color:#f0f0fa;padding:4px 0;border-bottom:1px solid #ffffff08;">→ {g}</div>' for g in dna.get("gaps",[])])+"</div>",unsafe_allow_html=True)

        st.markdown('<div class="card"><div style="font-weight:600;margin-bottom:10px;color:#ffd166;">🚀 Next Steps</div>'+"".join([f'<div style="font-size:0.85rem;color:#f0f0fa;padding:6px 0;border-bottom:1px solid #ffffff08;"><span style="color:#ffd166;font-weight:700;">{i+1}.</span> {s}</div>' for i,s in enumerate(dna.get("next_steps",[]))])+"</div>",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FIRSTSEM AI
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "firstsem":
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">🎓 FirstSem AI</div>
        <div class="page-hero-sub">Are you in the right course? Find out in 2 minutes before it's too late.</div>
    </div>""",unsafe_allow_html=True)

    p=st.session_state.profile
    branch=p.get("branch","CSE") if p else "CSE"

    st.markdown(f'<div class="card"><div style="font-size:0.85rem;color:#9090b0;">This tool is especially powerful in <b style="color:#f0f0fa;">Semester 1 and 2</b> when you can still make course changes. Currently showing for: <span class="badge badge-purple">{branch}</span></div></div>',unsafe_allow_html=True)

    with st.form("firstsem_form"):
        q1=st.text_area("Why did you choose your current course? Be honest.",placeholder="My parents wanted me to / I genuinely love coding / I didn't know what else to pick...")
        q2=st.multiselect("What activities genuinely excite you? (pick all that apply)",["Building apps/websites","Fixing/tinkering with hardware","Drawing, designing, creating art","Understanding how businesses work","Helping and teaching people","Writing stories or content","Sports and physical activity","Science experiments","Music or performance","Gaming / game design","Working with data and numbers","Leading teams and organising events"])
        q3=st.selectbox("How do you feel sitting in your current classes?",["Genuinely excited and curious","Okay, sometimes interesting","Mostly bored but managing","Completely lost and uninterested","I haven't decided yet"])
        q4=st.text_area("What would you do if college didn't exist and you had 1 year free?",placeholder="I'd build games / travel / learn music / start a business...")
        q5=st.selectbox("What's your relationship with coding right now?",["Love it, can spend hours","It's okay, manageable","Not my thing but I'll try","Hate it completely"])
        if st.form_submit_button("🎓 Analyse My Course Fit", use_container_width=True):
            with st.spinner("AI analysing your course compatibility..."):
                result=ask_claude(f"""You are FirstSem AI — a compassionate career counsellor for LPU students.

Student is in: {branch}
Why they chose it: {q1}
What excites them: {q2}
Feeling in class: {q3}
Free year plans: {q4}
Relationship with coding: {q5}

Give an honest, warm, non-judgmental analysis:
1. Course Fit Score (0-100) with explanation
2. Are they likely in the right course? Why?
3. If not fitting well — what 2 alternative courses/paths might suit them better at LPU?
4. Skills they should build regardless of course
5. One powerful piece of advice

Be honest but kind. This might be life-changing advice for a young student.""",max_tokens=600)
                st.markdown(f'<div class="ai-box">{result.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SKILLFORGE (Arena)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "arena":
    p=st.session_state.profile
    branch=p.get("branch","CSE") if p else "CSE"
    sem=p.get("sem",3) if p else 3

    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">⚡ SkillForge</div>
        <div class="page-hero-sub">Daily AI challenges. Beat your batch. Earn XP. Get placed faster.</div>
    </div>""",unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)
    with c1: st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#ffd166;">{st.session_state.arena_score}</div><div class="stat-label">Total XP</div></div>',unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><div class="stat-val">{st.session_state.streak}🔥</div><div class="stat-label">Day Streak</div></div>',unsafe_allow_html=True)
    with c3:
        rank=max(1,150-st.session_state.arena_score//10)
        st.markdown(f'<div class="stat-card"><div class="stat-val" style="color:#00e5a0;">#{rank}</div><div class="stat-label">Campus Rank</div></div>',unsafe_allow_html=True)

    tab1,tab2=st.tabs(["⚡ Daily Challenge","🏆 Leaderboard"])

    with tab1:
        cat=st.selectbox("Category",["DSA / Coding","Aptitude & Reasoning","Core Subject","System Design","Communication","General Knowledge","Cybersecurity","AI & ML Basics"])
        diff=st.select_slider("Difficulty",["Easy","Medium","Hard","Expert"],value="Medium")

        if st.button("⚡ Generate Challenge", use_container_width=True):
            with st.spinner("AI crafting your challenge..."):
                xp_map={"Easy":10,"Medium":20,"Hard":35,"Expert":50}
                xp_val=xp_map.get(diff,20)
                qraw=ask_claude(f"""Generate a single {diff} {cat} challenge for LPU {branch} Sem {sem} student.
Return ONLY valid JSON:
{{"question":"...","options":["A) ...","B) ...","C) ...","D) ..."],"answer":"A","explanation":"...","difficulty":"{diff}","xp":{xp_val},"fun_fact":"interesting related fact"}}""",max_tokens=500)
                try:
                    raw=qraw.strip().replace("```json","").replace("```","").strip()
                    st.session_state.current_q=json.loads(raw)
                    st.session_state.answered=False
                except:
                    st.session_state.current_q={"question":"What is the time complexity of merge sort?","options":["A) O(n)","B) O(n log n)","C) O(n²)","D) O(log n)"],"answer":"B","explanation":"Merge sort divides array in half (log n levels) and merges in O(n) time per level = O(n log n).","difficulty":diff,"xp":20,"fun_fact":"Merge sort was invented by John von Neumann in 1945!"}
                    st.session_state.answered=False

        q=st.session_state.current_q
        if q:
            xp_val=q.get('xp',20)
            st.markdown(f"""
            <div class="challenge-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                    <div style="display:flex;gap:6px;">
                        <span class="badge badge-purple">{cat}</span>
                        <span class="badge badge-{"red" if q.get("difficulty")=="Hard" or q.get("difficulty")=="Expert" else "green" if q.get("difficulty")=="Easy" else "gold"}">{q.get("difficulty","Medium")}</span>
                    </div>
                    <span class="badge badge-gold">+{xp_val} XP</span>
                </div>
                <div class="challenge-q">{q["question"]}</div>
            </div>""",unsafe_allow_html=True)

            if not st.session_state.answered:
                choice=st.radio("Your answer:",q["options"],index=None)
                if st.button("Submit Answer ✓",use_container_width=True):
                    if choice:
                        st.session_state.answered=True
                        if choice[0]==q["answer"]:
                            st.session_state.arena_score+=xp_val
                            st.session_state.streak+=1
                            st.success(f"✅ Correct! +{xp_val} XP • Streak: {st.session_state.streak}🔥")
                        else:
                            st.session_state.streak=0
                            st.error(f"❌ Wrong. Answer: {q['answer']}")
                        st.markdown(f'<div class="ai-box"><b>💡 Explanation:</b><br>{q["explanation"]}<br><br><b>🎯 Fun fact:</b> {q.get("fun_fact","")}</div>',unsafe_allow_html=True)
            else:
                st.info("✅ Done! Click Generate Challenge for a new one.")

    with tab2:
        p_name=p.get("name","You") if p else "You"
        leaders=[
            ("Arjun S.","CSE","1,240","#ffd166","AJ"),
            ("Priya K.","ECE","1,180","#c0c0c0","PK"),
            ("Rahul M.","CSE","1,050","#cd7f32","RM"),
            (p_name,branch if p else "CSE",str(st.session_state.arena_score),"#7c6dfa",p_name[:2].upper() if p else "YO"),
            ("Sneha R.","MBA","820","#9090b0","SR"),
        ]
        leaders.sort(key=lambda x: int(x[2].replace(",","")),reverse=True)
        for i,(nm,br,xp,col,init) in enumerate(leaders):
            medal=["🥇","🥈","🥉","",""][i] if i<5 else ""
            st.markdown(f"""
            <div class="lb-row" style="{"border-color:#7c6dfa44;" if nm==p_name else ""}">
                <div class="lb-rank" style="color:{col};">{medal or f"#{i+1}"}</div>
                <div class="lb-avatar" style="background:{"linear-gradient(135deg,#7c6dfa,#f72585)" if nm==p_name else "#1e1e32"};color:{"#fff" if nm==p_name else col};">{init}</div>
                <div style="flex:1;">
                    <div class="lb-name" style="color:{"#fff" if nm==p_name else "#f0f0fa"};">{nm} {"← You" if nm==p_name else ""}</div>
                    <div class="lb-branch">{br}</div>
                </div>
                <div class="lb-xp" style="color:{col};">{xp} XP</div>
            </div>""",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CAMPUSCONNECT (Tribe)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "tribe":
    p=st.session_state.profile
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">🤝 CampusConnect</div>
        <div class="page-hero-sub">Find your people. Build your team. Never go it alone.</div>
    </div>""",unsafe_allow_html=True)

    interests=p.get("interests",[]) if p else []
    tab1,tab2=st.tabs(["👥 Find Students","🎯 Interest Groups"])

    with tab1:
        c1,c2=st.columns(2)
        with c1: find_int=st.multiselect("Interest filter",["Coding","Gaming","AI/ML","Web Dev","App Dev","Design","Music","Sports","Startup","Research","Open Source","Data Science"],default=interests[:2] if len(interests)>=2 else interests)
        with c2: find_br=st.selectbox("Branch",["Any","CSE","ECE","ME","Civil","MBA","BCA"])

        if st.button("🔍 Find My People",use_container_width=True):
            with st.spinner("AI matching you with compatible students..."):
                raw=ask_claude(f"""Generate 4 realistic LPU student profiles matching interests: {find_int}, branch: {find_br}.
Return ONLY a JSON array:
[{{"name":"...","branch":"...","sem":3,"interests":["..."],"skills":"...","looking_for":"...","vibe":"one sentence","online_now":true}}]""",max_tokens=600)
                try:
                    matches=json.loads(raw.strip().replace("```json","").replace("```","").strip())
                except:
                    matches=[{"name":"Karan Mehta","branch":"CSE","sem":4,"interests":["Coding","AI/ML"],"skills":"Python, React","looking_for":"Hackathon partner","vibe":"Serious coder who games on weekends","online_now":True},{"name":"Simran Kaur","branch":"CSE","sem":3,"interests":["Design","Web Dev"],"skills":"Figma, CSS","looking_for":"Startup team","vibe":"10 ideas a day, ships at least 1","online_now":False},{"name":"Rohit Sharma","branch":"ECE","sem":5,"interests":["Coding","Open Source"],"skills":"C++, Arduino","looking_for":"Open source contributors","vibe":"Quiet, writes clean code","online_now":True},{"name":"Anjali Gupta","branch":"BCA","sem":2,"interests":["Gaming","App Dev"],"skills":"Unity, Flutter","looking_for":"Game dev collab","vibe":"Turns everything into a game","online_now":False}]

                for m in matches:
                    tags="".join([f'<span class="badge badge-purple">{i}</span>' for i in m.get("interests",[])])
                    online=m.get("online_now",False)
                    st.markdown(f"""
                    <div class="tribe-card">
                        <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
                            <div style="position:relative;">
                                <div style="width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#2d2b5a,#1e1e32);display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:700;color:#a29cff;border:1px solid #7c6dfa30;">{m['name'][0]}</div>
                                <div style="position:absolute;bottom:0;right:0;width:10px;height:10px;border-radius:50%;background:{"#00e5a0" if online else "#555"};border:2px solid #0f0f1a;"></div>
                            </div>
                            <div style="flex:1;">
                                <div style="font-weight:600;color:#f0f0fa;font-size:0.9rem;">{m['name']}</div>
                                <div style="font-size:0.72rem;color:#9090b0;">{m['branch']} · Sem {m['sem']} · {"🟢 Online" if online else "⚫ Offline"}</div>
                            </div>
                        </div>
                        <div style="margin-bottom:8px;">{tags}</div>
                        <div style="font-size:0.8rem;color:#9090b0;margin-bottom:3px;"><b style="color:#f0f0fa;">Skills:</b> {m.get('skills','—')}</div>
                        <div style="font-size:0.8rem;color:#9090b0;margin-bottom:6px;"><b style="color:#f0f0fa;">Looking for:</b> {m.get('looking_for','—')}</div>
                        <div style="font-size:0.78rem;color:#7c6dfa;font-style:italic;">"{m.get('vibe','—')}"</div>
                    </div>""",unsafe_allow_html=True)

    with tab2:
        groups=[
            ("💻","Coding Club","284 members","CSE, BCA, ECE","Competitive programming, hackathons","#7c6dfa"),
            ("🎮","Game Dev Society","127 members","All branches","Unity, Unreal, indie game jams","#f72585"),
            ("🚀","Startup Cell","203 members","All branches","Ideas, pitching, MVP building","#ffd166"),
            ("🧠","AI/ML Research","156 members","CSE, ECE","Papers, projects, Kaggle","#00e5a0"),
            ("🎨","Design Studio","98 members","All branches","UI/UX, branding, Figma","#4cc9f0"),
            ("🌱","Open Source LPU","74 members","CSE, IT","GitHub contributions, GSoC prep","#ff9f43"),
        ]
        cols=st.columns(2)
        for i,(icon,name_g,members,branches,desc,color) in enumerate(groups):
            with cols[i%2]:
                st.markdown(f"""
                <div class="card" style="border-top:2px solid {color};">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                        <span style="font-size:1.4rem;">{icon}</span>
                        <div>
                            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;">{name_g}</div>
                            <div style="font-size:0.72rem;color:#9090b0;">{members} · {branches}</div>
                        </div>
                    </div>
                    <div style="font-size:0.8rem;color:#9090b0;">{desc}</div>
                </div>""",unsafe_allow_html=True)
                if st.button(f"Join {name_g}",key=f"join_{i}",use_container_width=True):
                    st.success(f"Request sent to {name_g}! 🎉")


# ══════════════════════════════════════════════════════════════════════════════
# PROJECT HIVE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "projecthive":
    p=st.session_state.profile
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">🐝 ProjectHive</div>
        <div class="page-hero-sub">Post your idea. Find your team. Ship something real.</div>
    </div>""",unsafe_allow_html=True)

    tab1,tab2=st.tabs(["🔥 Active Projects","➕ Post Your Idea"])

    with tab1:
        projects=[
            {"title":"AI Attendance System for LPU","owner":"Karan M.","branch":"CSE","need":["ML","Python","React"],"type":"Startup","members":2,"max":4,"desc":"Facial recognition based attendance that integrates with UMS portal"},
            {"title":"Campus Food Delivery App","owner":"Priya S.","branch":"MBA","need":["Flutter","Node.js","Design"],"type":"Startup","members":1,"max":3,"desc":"Canteen to hostel delivery with pre-ordering to skip queues"},
            {"title":"LPU Lost & Found Platform","owner":"Rahul K.","branch":"CSE","need":["Web Dev","Design"],"type":"College Project","members":2,"max":3,"desc":"Post lost items, AI matches descriptions to found items"},
            {"title":"Competitive Programming Study Group","owner":"Sneha R.","branch":"CSE","need":["Coding"],"type":"Study Group","members":5,"max":8,"desc":"DSA prep for placements, daily LeetCode together"},
        ]
        for proj in projects+st.session_state.project_posts:
            need_tags="".join([f'<span class="badge badge-purple">{n}</span>' for n in proj["need"]])
            filled=proj["members"]; total=proj["max"]
            fill_pct=int(filled/total*100)
            st.markdown(f"""
            <div class="card glow">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;color:#f0f0fa;">{proj['title']}</div>
                    <span class="badge badge-gold">{proj['type']}</span>
                </div>
                <div style="font-size:0.8rem;color:#9090b0;margin-bottom:8px;">{proj['desc']}</div>
                <div style="margin-bottom:8px;">{need_tags}</div>
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="flex:1;">
                        <div class="prog-wrap" style="height:6px;"><div class="prog-fill" style="width:{fill_pct}%;background:{"#00e5a0" if fill_pct<80 else "#ffd166"};"></div></div>
                    </div>
                    <div style="font-size:0.75rem;color:#9090b0;">{filled}/{total} members</div>
                    <div style="font-size:0.75rem;color:#9090b0;">by {proj['owner']} · {proj['branch']}</div>
                </div>
            </div>""",unsafe_allow_html=True)
            if st.button(f"Join this project →",key=f"join_proj_{proj['title'][:10]}",use_container_width=True):
                st.success(f"Request sent! The owner will get back to you.")

    with tab2:
        with st.form("post_project"):
            ptitle=st.text_input("Project name")
            pdesc=st.text_area("What are you building? What problem does it solve?")
            pneed=st.multiselect("Skills you need",["Python","React","Flutter","ML","Design","Arduino","Node.js","Data Analysis","Figma","Unity","Java","C++"])
            ptype=st.selectbox("Type",["Hackathon","College Project","Startup","Open Source","Research","Study Group"])
            pmax=st.slider("Max team size",2,8,4)
            if st.form_submit_button("🐝 Post to ProjectHive",use_container_width=True):
                if ptitle and pdesc:
                    new_proj={"title":ptitle,"owner":p.get("name","You") if p else "You","branch":p.get("branch","CSE") if p else "CSE","need":pneed,"type":ptype,"members":1,"max":pmax,"desc":pdesc}
                    st.session_state.project_posts.append(new_proj)
                    with st.spinner("AI analysing your project..."):
                        advice=ask_claude(f"An LPU student posted this project: '{ptitle}' — {pdesc}. They need: {pneed}. Give 3 sentences of encouragement and practical tips for finding the right team at LPU.",max_tokens=200)
                    st.success("Posted! ✅")
                    st.markdown(f'<div class="ai-box">{advice}</div>',unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ASK TEACHER
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "askteacher":
    p=st.session_state.profile
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">🧑‍🏫 AskTeacher</div>
        <div class="page-hero-sub">Find the right teacher for your exact doubt. Stop messaging the wrong faculty.</div>
    </div>""",unsafe_allow_html=True)

    with st.form("ask_teacher_form"):
        doubt=st.text_area("What do you need help with?",placeholder="e.g. I don't understand recursion in Data Structures / I need guidance on my final year project / Career advice for placements")
        dtype=st.selectbox("Type of help",["Subject doubt / concept","Project guidance","Career advice","Research guidance","Mental / personal support","Exam strategy"])
        urgency=st.selectbox("How urgent?",["Can wait a few days","This week","Very urgent — exam soon"])
        if st.form_submit_button("🧑‍🏫 Find My Mentor",use_container_width=True):
            if doubt:
                with st.spinner("AI finding the right mentor approach..."):
                    branch=p.get("branch","CSE") if p else "CSE"
                    result=ask_claude(f"""You are AskTeacher — an LPU student advisor.

Student ({branch}) needs help with: '{doubt}'
Type: {dtype} | Urgency: {urgency}

Give:
1. What TYPE of faculty/mentor to approach (subject teacher, HOD, mentor teacher, counsellor, senior student, placement cell, etc.)
2. Exact HOW to approach them (in person / email / UMS / Teams) with a sample message
3. What to PREPARE before meeting them
4. If a senior student peer would help better — why and how to find one on CampusConnect
5. One tip to get a faster/better response

Be specific to LPU's system. Be practical.""",max_tokens=500)
                    st.markdown(f'<div class="ai-box">{result.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)

    st.markdown('<div class="sec-head">⭐ Most Helpful Faculty (Peer Rated)</div>',unsafe_allow_html=True)
    faculty=[
        ("Dr. Rajesh Kumar","CSE","Data Structures, Algorithms","4.9 ⭐","Open door policy, replies on Teams within 2hrs"),
        ("Prof. Sunita Sharma","CSE/IT","Web Dev, Python","4.8 ⭐","Best for project guidance, very supportive"),
        ("Dr. Amit Verma","ECE","VLSI, Embedded","4.7 ⭐","Patient explainer, available after 4pm"),
        ("Prof. Neha Gupta","MBA","Marketing, Entrepreneurship","4.9 ⭐","Startup mentor, connects students to industry"),
    ]
    for f in faculty:
        st.markdown(f"""
        <div class="tribe-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div style="font-weight:600;font-size:0.9rem;color:#f0f0fa;">{f[0]}</div>
                    <div style="font-size:0.75rem;color:#7c6dfa;margin-top:2px;">{f[1]} · {f[2]}</div>
                    <div style="font-size:0.78rem;color:#9090b0;margin-top:6px;">{f[4]}</div>
                </div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:#ffd166;font-size:0.95rem;">{f[3]}</div>
            </div>
        </div>""",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MINDSPACE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "mindspace":
    st.markdown("""
    <div class="page-hero" style="border-color:#f7258530;">
        <div class="page-hero-title">🫧 MindSpace</div>
        <div class="page-hero-sub">A safe, anonymous space. No judgement. No records. Just support.</div>
    </div>""",unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="border-color:#00e5a030;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span class="enc-badge">🔒 Anonymous & Private</span>
            <span class="enc-badge">💚 Not stored</span>
            <span class="enc-badge">🏥 Connects to real help</span>
        </div>
        <div style="font-size:0.82rem;color:#9090b0;margin-top:10px;line-height:1.6;">
            Everything here stays between you and the AI. If things feel serious, MindSpace will gently connect you to LPU's counselling center or national helplines. You are not alone.
        </div>
    </div>""",unsafe_allow_html=True)

    mood=st.select_slider("How are you feeling right now?",["😔 Really low","😟 Struggling","😐 Okay","🙂 Decent","😊 Good"],value="😐 Okay")

    system_ms="""You are MindSpace AI — a warm, empathetic mental health support companion for LPU students.

You are NOT a therapist and you make that clear if asked. You offer:
- A safe space to vent and be heard without judgement
- Gentle CBT-inspired reframing techniques
- Stress and anxiety management tips
- Academic pressure support
- Loneliness and social anxiety support

IMPORTANT RULES:
- Always validate feelings first before giving advice
- If you detect serious distress, suicidal ideation, or self-harm: immediately and compassionately provide LPU Counselling Centre (iCall: 9152987821) and Vandrevala Foundation (1860-2662-345, 24/7)
- Never diagnose
- Never be preachy or dismissive
- Speak like a caring friend who happens to know about mental health
- Keep responses warm, human, and concise"""

    for msg in st.session_state.mindspace_msgs:
        if msg["role"]=="user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai" style="border-left-color:#f72585;">{msg["content"].replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)

    if not st.session_state.mindspace_msgs:
        st.markdown(f"""
        <div class="chat-ai" style="border-left-color:#f72585;">
            Hey 💙 You came here, and that already takes courage.<br><br>
            I'm MindSpace — a safe, anonymous space just for you. No judgement, no records.<br><br>
            You can talk about anything — stress, pressure, loneliness, feeling lost, or just needing to vent. I'm here.<br><br>
            <i>You're feeling: {mood}</i> — want to tell me more about that?
        </div>""",unsafe_allow_html=True)

    user_ms=st.text_input("Say anything...",key="ms_input",placeholder="How are you feeling? What's going on?")
    c1,c2=st.columns([1,4])
    with c1:
        if st.button("Send 💙",key="ms_send"):
            if user_ms:
                st.session_state.mindspace_msgs.append({"role":"user","content":user_ms})
                with st.spinner(""):
                    reply=ask_claude_chat(st.session_state.mindspace_msgs,system=system_ms,max_tokens=400)
                    st.session_state.mindspace_msgs.append({"role":"assistant","content":reply})
                st.rerun()
    with c2:
        if st.button("Clear & start fresh",key="ms_clear"):
            st.session_state.mindspace_msgs=[]
            st.rerun()

    st.markdown("""
    <div style="background:#0d2e22;border:1px solid #00e5a020;border-radius:12px;padding:12px 16px;margin-top:16px;">
        <div style="font-size:0.78rem;color:#00e5a0;font-weight:600;margin-bottom:6px;">📞 Real Help — Available 24/7</div>
        <div style="font-size:0.8rem;color:#9090b0;line-height:1.7;">
            🏥 <b style="color:#f0f0fa;">LPU Counselling Centre</b> — Visit Student Welfare block<br>
            📞 <b style="color:#f0f0fa;">iCall</b> — 9152987821 (Mon–Sat, 8am–10pm)<br>
            📞 <b style="color:#f0f0fa;">Vandrevala Foundation</b> — 1860-2662-345 (24/7, free)
        </div>
    </div>""",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# NEXUS AI
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "ai":
    p=st.session_state.profile
    st.markdown("""
    <div class="page-hero">
        <div class="page-hero-title">🤖 Nexus AI</div>
        <div class="page-hero-sub">Your personal AI that knows LPU inside out. Ask anything.</div>
    </div>""",unsafe_allow_html=True)

    system_nexus=f"""You are Nexus AI — the intelligent core of LPU Nexus, built specifically for Lovely Professional University students.

You know everything about LPU:
- Academic rules: 75% attendance mandatory, reappear/improvement exam policies, CGPA grading, UMS portal
- Campus life: hostels, canteens, shuttle timings, Euphoria fest, One India, duty leave process
- Courses: BTech (CSE/ECE/ME/Civil/EEE/IT), MBA, BCA, BSc — all semester patterns
- Placement: TCS, Infosys, Wipro, Amazon, Cognizant, Capgemini, and 500+ companies that recruit
- Skills: LeetCode, CodeChef, HackerRank, certifications, project advice
- Mental health: warm, non-judgmental, always refers to professionals when needed

Student profile:
Name: {p.get('name','Not set') if p else 'Not set'}
Branch: {p.get('branch','Unknown') if p else 'Unknown'} | Semester: {p.get('sem','?') if p else '?'}
CGPA: {p.get('cgpa','?') if p else '?'} | Attendance: {p.get('attend','?') if p else '?'}%
Backlogs: {p.get('backlogs',0) if p else '?'} | Interests: {p.get('interests',[]) if p else []}
Goal: {p.get('goal','Not specified') if p else 'Not specified'}

Be conversational, direct, warm. Use the student's name. Never be preachy. Speak like a smart senior who genuinely cares."""

    for msg in st.session_state.ai_messages:
        if msg["role"]=="user":
            st.markdown(f'<div class="chat-user">{msg["content"]}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">{msg["content"].replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)

    if not st.session_state.ai_messages:
        name=p.get("name","there") if p else "there"
        st.markdown(f"""
        <div class="chat-ai">
            Hey {name}! 👋 I'm Nexus AI — I know LPU inside out.<br><br>
            Ask me anything:<br>
            • <i>"Will I pass this semester?"</i><br>
            • <i>"How do I apply for duty leave?"</i><br>
            • <i>"Give me a hard DSA problem"</i><br>
            • <i>"What companies recruit from my branch?"</i><br>
            • <i>"I'm stressed about exams"</i>
        </div>""",unsafe_allow_html=True)

    user_ai=st.text_input("Message Nexus AI...",key="ai_input",placeholder="Ask anything about LPU, your studies, skills, or campus life...")
    c1,c2=st.columns([1,5])
    with c1:
        if st.button("Send →",key="ai_send"):
            if user_ai:
                st.session_state.ai_messages.append({"role":"user","content":user_ai})
                with st.spinner(""):
                    reply=ask_claude_chat(st.session_state.ai_messages,system=system_nexus,max_tokens=600)
                    st.session_state.ai_messages.append({"role":"assistant","content":reply})
                st.rerun()
    with c2:
        if st.button("Clear chat",key="ai_clear"):
            st.session_state.ai_messages=[]
            st.rerun()

    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem;color:#9090b0;margin-bottom:8px;">Quick questions</div>',unsafe_allow_html=True)
    quick=[
        "Will I pass this semester?",
        "How do I apply for duty leave?",
        "What skills should I learn for placements?",
        "Give me a hard DSA problem",
        "Which companies recruit from LPU CSE?",
        "I'm feeling overwhelmed with studies"
    ]
    cols=st.columns(3)
    for i,q in enumerate(quick):
        with cols[i%3]:
            if st.button(q,key=f"q_{i}",use_container_width=True):
                st.session_state.ai_messages.append({"role":"user","content":q})
                with st.spinner(""):
                    reply=ask_claude_chat(st.session_state.ai_messages,system=system_nexus,max_tokens=500)
                    st.session_state.ai_messages.append({"role":"assistant","content":reply})
                st.rerun()


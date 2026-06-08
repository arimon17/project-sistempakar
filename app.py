import streamlit as st
from datetime import datetime
from certainty_factor import proses_diagnosa_lengkap
from knowledge_base import get_semua_gejala_list, validasi_basis_pengetahuan

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExpertDX — Diagnosa Kerusakan Komputer & Laptop",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DESIGN SYSTEM ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Open+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── CSS CUSTOM PROPERTIES (Dark/Light adaptive) ── */
:root {
  --primary:       #3B82F6;
  --primary-dark:  #2563EB;
  --primary-light: #EFF6FF;
  --secondary:     #8B5CF6;
  --success:       #16A34A;
  --success-light: #F0FDF4;
  --warning:       #D97706;
  --warning-light: #FFFBEB;
  --danger:        #DC2626;
  --danger-light:  #FEF2F2;

  --surface:       #FFFFFF;
  --surface-2:     #F8FAFC;
  --surface-3:     #F1F5F9;
  --border:        #E2E8F0;
  --border-strong: #CBD5E1;

  --text-primary:  #0F172A;
  --text-secondary:#475569;
  --text-tertiary: #94A3B8;
  --text-inverse:  #FFFFFF;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg: 0 10px 30px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.06);
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface:       #0F172A;
    --surface-2:     #1E293B;
    --surface-3:     #334155;
    --border:        #334155;
    --border-strong: #475569;
    --text-primary:  #F1F5F9;
    --text-secondary:#CBD5E1;
    --text-tertiary: #64748B;
    --primary-light: #1E3A5F;
    --success-light: #052E16;
    --warning-light: #1C0F00;
    --danger-light:  #1C0202;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
    --shadow-lg: 0 10px 30px rgba(0,0,0,0.5);
  }
}

/* ── STREAMLIT DARK MODE DETECTION ── */
[data-theme="dark"] {
  --surface:       #0F172A;
  --surface-2:     #1E293B;
  --surface-3:     #334155;
  --border:        #334155;
  --border-strong: #475569;
  --text-primary:  #F1F5F9;
  --text-secondary:#CBD5E1;
  --text-tertiary: #64748B;
  --primary-light: #1E3A5F;
  --success-light: #052E16;
  --warning-light: #1C0F00;
  --danger-light:  #1C0202;
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"], .stApp {
  font-family: 'Open Sans', system-ui, sans-serif !important;
  background: var(--surface) !important;
  color: var(--text-primary) !important;
}

/* ── MAIN CONTAINER ── */
.main .block-container {
  padding: 0 2rem 4rem !important;
  max-width: 1280px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 99px;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--surface-2) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── HERO SECTION ── */
.hero {
  background: linear-gradient(135deg, #1D4ED8 0%, #4F46E5 50%, #7C3AED 100%);
  border-radius: var(--radius-lg);
  padding: 3rem 2.5rem;
  margin: 1.5rem 0 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(255,255,255,0.06) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,255,255,0.04) 0%, transparent 40%);
  pointer-events: none;
}
.hero-eyebrow {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.6);
  margin-bottom: 0.75rem;
}
.hero-title {
  font-family: 'Poppins', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.2;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}
.hero-title span {
  background: linear-gradient(90deg, #93C5FD, #C4B5FD);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 0.875rem;
  color: rgba(255,255,255,0.7);
  line-height: 1.6;
  max-width: 480px;
}
.hero-chips {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}
.hero-chip {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 99px;
  border: 1px solid rgba(255,255,255,0.25);
  color: rgba(255,255,255,0.85);
  background: rgba(255,255,255,0.08);
  letter-spacing: 0.05em;
}

/* ── SIDEBAR BRAND ── */
.sb-brand {
  padding: 1.5rem 1.25rem 1rem;
  border-bottom: 1px solid var(--border);
}
.sb-brand-name {
  font-family: 'Poppins', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: -0.01em;
}
.sb-brand-tag {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  color: var(--text-tertiary);
  margin-top: 2px;
  letter-spacing: 0.05em;
}

/* ── SIDEBAR SECTION ── */
.sb-section {
  padding: 1rem 1.25rem 0.5rem;
}
.sb-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin-bottom: 0.75rem;
}
.sb-stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.35rem 0;
  border-bottom: 1px solid var(--border);
}
.sb-stat-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
}
.sb-stat-val {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--primary);
}
.sb-member {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--border);
}
.sb-member-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
}
.sb-member-nim {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
  margin-top: 1px;
}
.sb-member-role {
  font-size: 0.6rem;
  font-weight: 600;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ── SECTION HEADER ── */
.section-header {
  font-family: 'Poppins', sans-serif;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0.02em;
  text-transform: uppercase;
  padding: 0 0 0.75rem;
  border-bottom: 2px solid var(--primary);
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.section-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--primary);
  flex-shrink: 0;
}

/* ── CATEGORY CARD (Gejala) ── */
.cat-header {
  font-family: 'Poppins', sans-serif;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.6rem 0.75rem;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  margin-bottom: 0.5rem;
}

/* ── CHECKBOX OVERRIDE ── */
[data-testid="stCheckbox"] {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.75rem;
  margin-bottom: 4px;
  transition: border-color 0.15s, background 0.15s;
}
[data-testid="stCheckbox"]:hover {
  border-color: var(--primary);
  background: var(--primary-light);
}
.stCheckbox > label {
  font-family: 'Open Sans', sans-serif !important;
  font-size: 0.78rem !important;
  color: var(--text-primary) !important;
  font-weight: 400 !important;
}
.stCheckbox > label span { color: var(--text-primary) !important; }

/* ── COUNTER BADGE ── */
.counter-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 1rem;
  border-radius: var(--radius-md);
  background: var(--surface-2);
  border: 1px solid var(--border);
  margin-bottom: 1rem;
}
.counter-num {
  font-family: 'Poppins', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary);
  min-width: 2ch;
  text-align: center;
}
.counter-label {
  font-size: 0.78rem;
  color: var(--text-secondary);
}
.counter-bar.ready {
  border-color: var(--success);
  background: var(--success-light);
}
.counter-bar.ready .counter-num { color: var(--success); }

/* ── BUTTONS ── */
.stButton > button {
  font-family: 'Poppins', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  border-radius: var(--radius-md) !important;
  padding: 0.625rem 1.25rem !important;
  width: 100% !important;
  transition: all 0.15s ease !important;
  letter-spacing: 0.02em !important;
}
.stButton > button[kind="primary"],
.stButton > button:first-child {
  background: var(--primary) !important;
  color: var(--text-inverse) !important;
  border: 1.5px solid var(--primary) !important;
  box-shadow: 0 1px 3px rgba(59,130,246,0.3) !important;
}
.stButton > button:hover {
  background: var(--primary-dark) !important;
  border-color: var(--primary-dark) !important;
  box-shadow: 0 4px 12px rgba(59,130,246,0.35) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
  box-shadow: 0 1px 3px rgba(59,130,246,0.2) !important;
}
.stButton > button:disabled {
  opacity: 0.45 !important;
  cursor: not-allowed !important;
  transform: none !important;
}

/* ── EMPTY STATE ── */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3.5rem 2rem;
  background: var(--surface-2);
  border: 1.5px dashed var(--border-strong);
  border-radius: var(--radius-lg);
  text-align: center;
  gap: 0.75rem;
}
.empty-icon {
  font-size: 2.5rem;
  line-height: 1;
  opacity: 0.4;
  filter: grayscale(0.5);
}
.empty-title {
  font-family: 'Poppins', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
}
.empty-sub {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  line-height: 1.6;
  max-width: 240px;
}

/* ── NO RESULT ── */
.no-result {
  padding: 2rem;
  background: var(--danger-light);
  border: 1px solid #FECACA;
  border-left: 4px solid var(--danger);
  border-radius: var(--radius-md);
}
.no-result-title {
  font-family: 'Poppins', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--danger);
  margin-bottom: 0.5rem;
}
.no-result-body {
  font-size: 0.78rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

/* ── METRICS ROW ── */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.metric-card {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.875rem 1rem;
}
.metric-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin-bottom: 0.25rem;
}
.metric-value {
  font-family: 'Poppins', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  line-height: 1.1;
}

/* ── RESULT CARD ── */
.result-card {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s;
}
.result-card:hover { box-shadow: var(--shadow-md); }
.result-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--primary);
}
.result-card.rank-1::before {
  background: linear-gradient(90deg, #F59E0B, #EF4444);
}
.result-card.rank-2::before { background: #94A3B8; }
.result-card.rank-3::before { background: #CD7C2F; }

.result-rank {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-tertiary);
  margin-bottom: 0.25rem;
}
.result-nama {
  font-family: 'Poppins', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  line-height: 1.3;
}
.result-kode {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  color: var(--primary);
  font-weight: 500;
}
.result-cf-num {
  font-family: 'Poppins', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 4px;
}
.cf-danger  { color: var(--danger); }
.cf-warning { color: var(--warning); }
.cf-success { color: var(--success); }
.cf-primary { color: var(--primary); }
.cf-muted   { color: var(--text-tertiary); }

/* ── CF PROGRESS BAR ── */
.cf-track {
  height: 6px;
  background: var(--surface-3);
  border-radius: 99px;
  overflow: hidden;
  margin: 0.5rem 0 0.25rem;
}
.cf-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.cf-meta {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
  margin-bottom: 0.75rem;
}

/* ── BADGE ── */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.62rem;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: 99px;
  letter-spacing: 0.04em;
}
.badge-danger  { background: var(--danger-light);  color: var(--danger);  border: 1px solid #FECACA; }
.badge-warning { background: var(--warning-light); color: var(--warning); border: 1px solid #FDE68A; }
.badge-success { background: var(--success-light); color: var(--success); border: 1px solid #BBF7D0; }
.badge-primary { background: var(--primary-light); color: var(--primary); border: 1px solid #BFDBFE; }
.badge-muted   { background: var(--surface-3);     color: var(--text-tertiary); border: 1px solid var(--border); }

/* ── SOLUSI LIST ── */
.solusi-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.6rem 0.75rem;
  background: var(--success-light);
  border: 1px solid #BBF7D0;
  border-radius: var(--radius-sm);
  margin-bottom: 6px;
  font-size: 0.75rem;
  color: var(--text-primary);
  line-height: 1.6;
  align-items: flex-start;
}
.solusi-num {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--success);
  flex-shrink: 0;
  margin-top: 2px;
}
.biaya-box {
  padding: 0.625rem 0.875rem;
  background: var(--warning-light);
  border: 1px solid #FDE68A;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  color: var(--text-primary);
  margin-top: 0.75rem;
}
.biaya-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--warning);
  display: block;
  margin-bottom: 2px;
}

/* ── INFERENSI / RULE CARD ── */
.rule-item {
  padding: 0.625rem 0.875rem;
  background: var(--surface-3);
  border: 1px solid var(--border);
  border-left: 3px solid var(--primary);
  border-radius: var(--radius-sm);
  margin-bottom: 6px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.68rem;
  color: var(--text-secondary);
  line-height: 1.7;
}
.rule-code {
  color: var(--primary);
  font-weight: 600;
}
.rule-arrow { color: var(--secondary); }
.cf-detail-item {
  padding: 0.5rem 0.75rem;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  margin-bottom: 4px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.67rem;
  color: var(--text-secondary);
  line-height: 1.8;
}

/* ── RIWAYAT CARD ── */
.history-item {
  padding: 0.875rem 1rem;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-bottom: 8px;
  transition: box-shadow 0.15s;
}
.history-item:hover { box-shadow: var(--shadow-sm); }
.history-time {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.63rem;
  color: var(--text-tertiary);
  margin-bottom: 0.35rem;
}
.history-diagnosa {
  font-family: 'Poppins', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}
.history-meta {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-tertiary);
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
}
[data-testid="stTabs"] button {
  font-family: 'Poppins', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  color: var(--text-secondary) !important;
  border-bottom: 2px solid transparent !important;
  border-radius: 0 !important;
  padding: 0.75rem 1.25rem !important;
  background: transparent !important;
  transition: color 0.15s, border-color 0.15s !important;
}
[data-testid="stTabs"] button:hover {
  color: var(--primary) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--primary) !important;
  border-bottom: 2px solid var(--primary) !important;
  font-weight: 600 !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
}
[data-testid="stExpander"] summary {
  font-family: 'Open Sans', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  color: var(--text-primary) !important;
  padding: 0.75rem 1rem !important;
}

/* ── DIVIDER ── */
.divider {
  height: 1px;
  background: var(--border);
  margin: 1.25rem 0;
}

/* ── PANDUAN STEPS ── */
.step-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  margin-bottom: 0.75rem;
  align-items: flex-start;
}
.step-num {
  font-family: 'Poppins', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-inverse);
  background: var(--primary);
  width: 28px; height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.step-title {
  font-family: 'Poppins', sans-serif;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 3px;
}
.step-body {
  font-size: 0.75rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

/* ── CF SCALE TABLE ── */
.scale-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.875rem;
  border-radius: var(--radius-sm);
  margin-bottom: 4px;
  background: var(--surface-2);
  border: 1px solid var(--border);
}
.scale-swatch {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.scale-range {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.68rem;
  color: var(--text-tertiary);
  width: 90px;
}
.scale-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* ── METRIC OVERRIDES (native) ── */
[data-testid="stMetric"] {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
  padding: 0.875rem 1rem !important;
}
[data-testid="stMetricLabel"] p {
  font-family: 'IBM Plex Mono', monospace !important;
  font-size: 0.6rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: var(--text-tertiary) !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Poppins', sans-serif !important;
  font-size: 1.5rem !important;
  font-weight: 700 !important;
  color: var(--primary) !important;
}

/* ── REDUCED MOTION ── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "riwayat"          not in st.session_state: st.session_state.riwayat          = []
if "hasil_diagnosa"   not in st.session_state: st.session_state.hasil_diagnosa   = None
if "gejala_dipilih"   not in st.session_state: st.session_state.gejala_dipilih   = []
if "reset_counter"    not in st.session_state: st.session_state.reset_counter    = 0
if "scroll_to_hasil"  not in st.session_state: st.session_state.scroll_to_hasil  = False

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def cf_color_class(warna: str) -> str:
    return {"red":"cf-danger","orange":"cf-warning","yellow":"cf-warning",
            "blue":"cf-primary","green":"cf-success"}.get(warna,"cf-muted")

def cf_fill_color(warna: str) -> str:
    return {"red":"#DC2626","orange":"#D97706","yellow":"#CA8A04",
            "blue":"#3B82F6","green":"#16A34A"}.get(warna,"#94A3B8")

def cf_badge_class(warna: str) -> str:
    return {"red":"badge-danger","orange":"badge-warning","yellow":"badge-warning",
            "blue":"badge-primary","green":"badge-success"}.get(warna,"badge-muted")

def render_cf_bar(persen: float, warna: str):
    fill = cf_fill_color(warna)
    st.markdown(f"""
    <div class="cf-track">
      <div class="cf-fill" style="width:{persen}%; background:{fill};"></div>
    </div>
    <div class="cf-meta">Keyakinan sistem: {persen}%</div>
    """, unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    val = validasi_basis_pengetahuan()

    st.markdown(f"""
    <div class="sb-brand">
      <div class="sb-brand-name">ExpertDX</div>
      <div class="sb-brand-tag">Diagnosa Kerusakan Komputer & Laptop</div>
    </div>

    <div class="sb-section">
      <div class="sb-label">Basis Pengetahuan</div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">Gejala</span>
        <span class="sb-stat-val">{val['total_gejala']}</span>
      </div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">Diagnosa</span>
        <span class="sb-stat-val">{val['total_kerusakan']}</span>
      </div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">Rules IF-THEN</span>
        <span class="sb-stat-val">{val['total_rules']}</span>
      </div>
      <div class="sb-stat-row">
        <span class="sb-stat-label">Metode Inferensi</span>
        <span class="sb-stat-val" style="font-size:0.62rem;">Forward Chaining</span>
      </div>
      <div class="sb-stat-row" style="border:none;">
        <span class="sb-stat-label">Ketidakpastian</span>
        <span class="sb-stat-val" style="font-size:0.62rem;">Certainty Factor</span>
      </div>
    </div>

    <div class="divider" style="margin:0;"></div>

    <div class="sb-section">
      <div class="sb-label">Tim Pengembang</div>
      <div class="sb-member">
        <div class="sb-member-name">Yosua Arimon Lende</div>
        <div class="sb-member-nim">24141101021</div>
        <div class="sb-member-role">Ketua Kelompok</div>
      </div>
      <div class="sb-member">
        <div class="sb-member-name">Fanesha Cicilia Dethan</div>
        <div class="sb-member-nim">24141101009</div>
      </div>
      <div class="sb-member" style="border:none;">
        <div class="sb-member-name">Azaria Harun Zogara</div>
        <div class="sb-member-nim">24141101001</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.riwayat:
        st.markdown(f"""
        <div class="divider" style="margin:0;"></div>
        <div class="sb-section">
          <div class="sb-label">Sesi</div>
          <div class="sb-stat-row" style="border:none;">
            <span class="sb-stat-label">Riwayat konsultasi</span>
            <span class="sb-stat-val">{len(st.session_state.riwayat)}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─── HERO ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Mata Kuliah · Sistem Pakar</div>
  <div class="hero-title">Diagnosa <span>Kerusakan</span><br>Komputer & Laptop</div>
  <div class="hero-sub">
    Identifikasi kemungkinan kerusakan perangkat berdasarkan gejala yang dialami,
    lengkap dengan tingkat keyakinan hasil diagnosa.
  </div>
  <div class="hero-chips">
    <span class="hero-chip">Forward Chaining</span>
    <span class="hero-chip">Certainty Factor</span>
    <span class="hero-chip">22 Gejala</span>
    <span class="hero-chip">6 Diagnosa</span>
    <span class="hero-chip">24 Rules IF-THEN</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Diagnosa", "Riwayat", "Panduan"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — DIAGNOSA
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    semua_gejala = get_semua_gejala_list()
    gejala_dict  = {g["kode"]: g for g in semua_gejala}

    col_l, col_r = st.columns([1, 1.2], gap="large")

    # ── KOLOM KIRI ──────────────────────────────────────────────────────────
    with col_l:
        st.markdown("""
        <div class="section-header">
          <div class="section-dot"></div>Pilih Gejala yang Dialami
        </div>
        <p style="font-size:0.78rem; color:var(--text-secondary);
                  margin-bottom:1rem; line-height:1.7;">
          Centang semua gejala yang sesuai dengan kondisi perangkat.
          Semakin tepat gejala yang dipilih, semakin akurat hasilnya.
        </p>
        """, unsafe_allow_html=True)

        kategori = {
            "Power & Startup"    : ["G01","G02","G12","G20"],
            "Performa Sistem"    : ["G03","G04","G05","G16","G18"],
            "Storage"            : ["G06","G14","G21"],
            "Thermal & Pendingin": ["G10","G11","G13"],
            "Display & Grafis"   : ["G08","G09","G19","G22"],
            "Sistem Operasi"     : ["G07","G15","G17"],
        }

        gejala_terpilih = []
        for nama_kat, kode_list in kategori.items():
            with st.expander(nama_kat, expanded=False):
                for kode in kode_list:
                    if kode not in gejala_dict: continue
                    g = gejala_dict[kode]
                    checked = st.checkbox(
                        f"[{kode}]  {g['nama']}",
                        key=f"cb_{kode}_{st.session_state.reset_counter}",
                        help=g["keterangan"],
                    )
                    if checked:
                        gejala_terpilih.append(kode)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        jumlah  = len(gejala_terpilih)
        is_ready = jumlah >= 2
        st.markdown(f"""
        <div class="counter-bar {'ready' if is_ready else ''}">
          <div class="counter-num">{jumlah}</div>
          <div class="counter-label">
            {'gejala dipilih — siap untuk diagnosa' if is_ready
             else 'gejala dipilih — pilih minimal 2 gejala'}
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Jalankan Diagnosa", key="btn_diagnosa", disabled=(jumlah == 0)):
                with st.spinner("Memproses basis pengetahuan..."):
                    hasil = proses_diagnosa_lengkap(gejala_terpilih)
                    st.session_state.hasil_diagnosa = hasil
                    st.session_state.gejala_dipilih = gejala_terpilih
                    st.session_state.scroll_to_hasil = True

                    if hasil["ada_hasil"]:
                        top = hasil["hasil"][0]
                        st.session_state.riwayat.insert(0, {
                            "waktu"    : datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "gejala"   : gejala_terpilih,
                            "diagnosa" : top["nama"],
                            "cf"       : top["cf_total"],
                            "persen"   : top["persentase"],
                        })
                        if len(st.session_state.riwayat) > 20:
                            st.session_state.riwayat = st.session_state.riwayat[:20]
        with c2:
            if st.button("Reset", key="btn_reset"):
                st.session_state.hasil_diagnosa  = None
                st.session_state.gejala_dipilih  = []
                st.session_state.reset_counter  += 1
                st.rerun()

    # ── KOLOM KANAN ─────────────────────────────────────────────────────────
    with col_r:
        st.markdown('<div id="hasil-diagnosa-anchor"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
          <div class="section-dot"></div>Hasil Diagnosa
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.scroll_to_hasil:
            st.session_state.scroll_to_hasil = False
            st.components.v1.html("""
            <script>
              window.parent.document.getElementById('hasil-diagnosa-anchor')
                ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            </script>
            """, height=0)

        hasil = st.session_state.hasil_diagnosa

        if hasil is None:
            st.markdown("""
            <div class="empty-state">
              <div class="empty-icon">💻</div>
              <div class="empty-title">Belum ada hasil diagnosa</div>
              <div class="empty-sub">
                Pilih gejala di panel kiri, lalu jalankan diagnosa
                untuk mendapatkan hasil analisis.
              </div>
            </div>
            """, unsafe_allow_html=True)

        elif not hasil["ada_hasil"]:
            st.markdown("""
            <div class="no-result">
              <div class="no-result-title">Tidak Terdiagnosa</div>
              <div class="no-result-body">
                Tidak ada rule yang cocok dengan kombinasi gejala yang dipilih.
                Coba tambahkan gejala lain yang relevan, atau konsultasikan
                ke teknisi untuk pemeriksaan langsung.
              </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # Metrics
            m1, m2, m3 = st.columns(3)
            with m1: st.metric("Rules Aktif",  hasil["total_rules_aktif"])
            with m2: st.metric("Diagnosa",     len(hasil["hasil"]))
            with m3: st.metric("Top CF",       f"{hasil['hasil'][0]['persentase']}%")

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            rank_cls = ["rank-1", "rank-2", "rank-3"]
            rank_lbl = ["Diagnosa Utama", "Diagnosa Alternatif", "Diagnosa Alternatif"]

            for i, d in enumerate(hasil["hasil"]):
                rcls = rank_cls[i] if i < 3 else ""
                rlbl = rank_lbl[i] if i < 3 else f"Diagnosa #{i+1}"
                cc   = cf_color_class(d["interpretasi"]["warna"])
                bc   = cf_badge_class(d["interpretasi"]["warna"])
                fill = cf_fill_color(d["interpretasi"]["warna"])

                st.markdown(f"""
                <div class="result-card {rcls}">
                  <div class="result-rank">{rlbl}</div>
                  <div class="result-nama">
                    <span class="result-kode">{d['kode']}</span> &nbsp;—&nbsp; {d['nama']}
                  </div>
                  <div class="result-cf-num {cc}">{d['persentase']}%</div>
                  <div class="cf-track">
                    <div class="cf-fill" style="width:{d['persentase']}%; background:{fill};"></div>
                  </div>
                  <div class="cf-meta">Nilai CF: {d['cf_total']} &nbsp;·&nbsp; {d['interpretasi']['label']}</div>
                  <div>
                    <span class="badge {bc}">{d['interpretasi']['label']}</span>
                    <span class="badge badge-muted">Bahaya: {d['info']['tingkat_bahaya']}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"Solusi & Detail — {d['kode']}"):
                    st.markdown(f"""
                    <p style="font-size:0.75rem; color:var(--text-secondary);
                               line-height:1.7; margin-bottom:0.875rem;">
                      {d['info']['deskripsi']}
                    </p>
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem;
                                letter-spacing:0.1em; text-transform:uppercase;
                                color:var(--success); margin-bottom:0.5rem;">
                      Langkah Penanganan
                    </div>
                    """, unsafe_allow_html=True)
                    for j, sol in enumerate(d["info"]["solusi"], 1):
                        st.markdown(f"""
                        <div class="solusi-item">
                          <span class="solusi-num">{j:02d}</span>
                          <span>{sol}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="biaya-box">
                      <span class="biaya-label">Estimasi Biaya</span>
                      {d['info']['estimasi_biaya']}
                    </div>
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem;
                                letter-spacing:0.1em; text-transform:uppercase;
                                color:var(--primary); margin:0.875rem 0 0.5rem;">
                      Detail Perhitungan CF
                    </div>
                    """, unsafe_allow_html=True)
                    for det in d["detail_cf"]:
                        st.markdown(f"""
                        <div class="cf-detail-item">
                          <span class="rule-code">[{det['rule']}]</span>
                          &nbsp; CF = {det['cf_pakar']} &times; {det['cf_user_min']}
                          = <strong style="color:var(--success);">{det['cf_kombinasi']}</strong><br>
                          <span style="color:var(--text-tertiary);">{det['deskripsi']}</span>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem;
                        letter-spacing:0.1em; text-transform:uppercase;
                        color:var(--text-tertiary); margin-bottom:0.75rem;">
              Jalur Inferensi Aktif
            </div>
            """, unsafe_allow_html=True)
            for jalur in hasil["jalur_inferensi"]:
                st.markdown(f'<div class="rule-item">{jalur}</div>', unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.6rem;
                        letter-spacing:0.1em; text-transform:uppercase;
                        color:var(--text-tertiary); margin-bottom:0.75rem;">
              Gejala yang Dipilih
            </div>
            """, unsafe_allow_html=True)
            badges = "".join([
                f'<span class="badge badge-primary" style="margin:2px;">{k}</span>'
                for k in st.session_state.gejala_dipilih
            ])
            st.markdown(f'<div style="margin-bottom:0.75rem;">{badges}</div>', unsafe_allow_html=True)
            for kode in st.session_state.gejala_dipilih:
                nama = gejala_dict.get(kode, {}).get("nama", kode)
                st.markdown(f"""
                <div class="rule-item">
                  <span class="rule-code">{kode}</span> &nbsp;— {nama}
                </div>
                """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — RIWAYAT
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-header">
      <div class="section-dot"></div>Riwayat Konsultasi
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.riwayat:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">📋</div>
          <div class="empty-title">Belum ada riwayat</div>
          <div class="empty-sub">Hasil konsultasi akan tersimpan di sini secara otomatis.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cr1, cr2 = st.columns([4, 1])
        with cr1:
            st.markdown(f"""
            <p style="font-size:0.75rem; color:var(--text-secondary); margin:0;">
              Menampilkan <strong>{len(st.session_state.riwayat)}</strong> sesi konsultasi
            </p>
            """, unsafe_allow_html=True)
        with cr2:
            if st.button("Hapus Semua", key="btn_hapus"):
                st.session_state.riwayat = []
                st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        for i, r in enumerate(st.session_state.riwayat):
            persen  = r["persen"]
            warna   = "danger" if persen >= 80 else "warning" if persen >= 60 else "primary"
            gejala_str = ", ".join(r["gejala"])
            st.markdown(f"""
            <div class="history-item">
              <div class="history-time">{r['waktu']} &nbsp;·&nbsp; Sesi #{len(st.session_state.riwayat) - i}</div>
              <div class="history-diagnosa">{r['diagnosa']}</div>
              <div class="history-meta">
                CF {r['cf']} ({r['persen']}%) &nbsp;·&nbsp; Gejala: {gejala_str}
              </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — PANDUAN
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    col_p1, col_p2 = st.columns([1.2, 1], gap="large")

    with col_p1:
        st.markdown("""
        <div class="section-header">
          <div class="section-dot"></div>Cara Menggunakan
        </div>
        """, unsafe_allow_html=True)

        steps = [
            ("1", "Buka tab Diagnosa",
             "Pastikan kamu berada di tab Diagnosa di bagian atas halaman."),
            ("2", "Pilih gejala",
             "Klik kategori gejala untuk membukanya, lalu centang semua gejala yang sesuai dengan kondisi perangkat."),
            ("3", "Jalankan diagnosa",
             "Setelah memilih gejala, klik tombol Jalankan Diagnosa. Sistem akan memproses menggunakan metode Forward Chaining."),
            ("4", "Baca hasil",
             "Hasil ditampilkan dengan nilai Certainty Factor (CF). Semakin tinggi nilai CF, semakin tinggi keyakinan sistem."),
            ("5", "Lihat solusi",
             "Klik Solusi & Detail pada setiap hasil diagnosa untuk melihat langkah penanganan dan estimasi biaya."),
            ("6", "Cek riwayat",
             "Semua hasil konsultasi tersimpan otomatis di tab Riwayat."),
        ]
        for num, title, body in steps:
            st.markdown(f"""
            <div class="step-card">
              <div class="step-num">{num}</div>
              <div>
                <div class="step-title">{title}</div>
                <div class="step-body">{body}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col_p2:
        st.markdown("""
        <div class="section-header">
          <div class="section-dot"></div>Skala Certainty Factor
        </div>
        """, unsafe_allow_html=True)

        skala = [
            ("#DC2626", "0.80 – 1.00", "Sangat Yakin"),
            ("#D97706", "0.60 – 0.79", "Kemungkinan Besar"),
            ("#CA8A04", "0.40 – 0.59", "Kemungkinan"),
            ("#3B82F6", "0.20 – 0.39", "Kemungkinan Kecil"),
            ("#94A3B8", "0.00 – 0.19", "Tidak Yakin"),
        ]
        for color, rentang, label in skala:
            st.markdown(f"""
            <div class="scale-row">
              <div class="scale-swatch" style="background:{color};"></div>
              <div class="scale-range">{rentang}</div>
              <div class="scale-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
          <div class="section-dot"></div>Tentang Sistem
        </div>
        <div style="font-size:0.75rem; color:var(--text-secondary); line-height:1.8;">
          <strong style="color:var(--text-primary);">ExpertDX</strong> adalah sistem pakar
          berbasis Python yang dibangun menggunakan metode
          <strong style="color:var(--text-primary);">Forward Chaining</strong> untuk
          penalaran dan <strong style="color:var(--text-primary);">Certainty Factor</strong>
          untuk menangani ketidakpastian dalam diagnosa kerusakan komputer dan laptop.
          <br><br>
          Sistem ini dikembangkan sebagai proyek akhir mata kuliah Sistem Pakar,
          Program Studi Informatika.
        </div>
        """, unsafe_allow_html=True)

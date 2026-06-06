import streamlit as st
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

st.set_page_config(
    page_title='AgroPredict Colombia',
    page_icon='\U0001F33E',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    .stApp {
        background-color: #0E1117;
    }

    section[data-testid="stSidebar"] {
        background-color: #1A1C23 !important;
        border-right: 1px solid #2A2D35;
    }
    section[data-testid="stSidebar"] .st-emotion-cache-1wmy9hl {
        background-color: #1A1C23;
    }
    section[data-testid="stSidebar"] a {
        color: #CCCCCC !important;
    }
    section[data-testid="stSidebar"] a:hover {
        color: #4CAF50 !important;
    }

    .main-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        background: linear-gradient(180deg, rgba(76,175,80,0.08) 0%, transparent 100%);
        border-bottom: 1px solid #2A2D35;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: #4CAF50;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.3rem;
        text-shadow: 0 2px 10px rgba(76,175,80,0.2);
    }
    .main-header p {
        color: #888888;
        font-size: 1.1rem;
        font-weight: 300;
    }

    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }
    h1 { color: #4CAF50 !important; font-size: 2.2rem !important; }
    h2 { color: #66BB6A !important; font-size: 1.6rem !important; }
    h3 { color: #81C784 !important; font-size: 1.3rem !important; }

    p, li, .stMarkdown {
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }

    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
        border: none;
    }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(76,175,80,0.3);
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #2E7D32, #4CAF50) !important;
        color: white !important;
    }
    .stButton button[kind="secondary"] {
        background: #2A2D35 !important;
        color: #E0E0E0 !important;
        border: 1px solid #444 !important;
    }
    .stButton button[kind="secondary"]:hover {
        background: #333 !important;
        border-color: #4CAF50 !important;
    }

    div[data-testid="stMetric"] {
        background: #1A1C23;
        border: 1px solid #2A2D35;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #4CAF50;
        box-shadow: 0 4px 16px rgba(76,175,80,0.15);
        transform: translateY(-2px);
    }
    div[data-testid="stMetric"] > div {
        color: #FFFFFF !important;
    }
    div[data-testid="stMetric"] label {
        color: #AAAAAA !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stExpander"] {
        background: #1A1C23;
        border: 1px solid #2A2D35;
        border-radius: 12px;
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600;
        color: #4CAF50;
    }

    div.stTabs button {
        background: transparent;
        color: #888888;
        font-weight: 500;
        padding: 0.6rem 1.2rem;
        border-radius: 8px 8px 0 0;
        transition: all 0.2s;
    }
    div.stTabs button:hover {
        color: #4CAF50;
        background: rgba(76,175,80,0.05);
    }
    div.stTabs button[aria-selected="true"] {
        color: #4CAF50;
        border-bottom: 2px solid #4CAF50;
        background: rgba(76,175,80,0.1);
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stNumberInput"] label {
        color: #AAAAAA !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background: #262730;
        border: 1px solid #3A3D45;
        border-radius: 8px;
    }
    div[data-testid="stNumberInput"] input {
        background: #262730;
        border: 1px solid #3A3D45;
        color: #FFFFFF;
        border-radius: 8px;
    }

    div.stSlider div[data-baseweb="slider"] div {
        background: #4CAF50 !important;
    }
    div.stSlider div[data-baseweb="slider"] div[role="slider"] {
        background: #4CAF50 !important;
        box-shadow: 0 0 8px rgba(76,175,80,0.4);
    }

    div[data-testid="stDataFrame"] {
        background: #1A1C23;
        border: 1px solid #2A2D35;
        border-radius: 12px;
        overflow: hidden;
    }
    div[data-testid="stDataFrame"] div[data-testid="stTable"] {
        color: #E0E0E0;
    }

    div.stAlert {
        background: #1A1C23 !important;
        border: 1px solid #2A2D35;
        border-radius: 12px;
    }
    div.stAlert[data-baseweb="notification"] {
        background: #1A1C23;
    }

    div.stSuccess {
        background: rgba(76,175,80,0.1) !important;
        border: 1px solid rgba(76,175,80,0.3) !important;
        color: #81C784 !important;
    }
    div.stWarning {
        background: rgba(255,152,0,0.1) !important;
        border: 1px solid rgba(255,152,0,0.3) !important;
        color: #FFB74D !important;
    }
    div.stInfo {
        background: rgba(33,150,243,0.1) !important;
        border: 1px solid rgba(33,150,243,0.3) !important;
        color: #64B5F6 !important;
    }
    div.stError {
        background: rgba(244,67,54,0.1) !important;
        border: 1px solid rgba(244,67,54,0.3) !important;
        color: #E57373 !important;
    }

    div[data-testid="stContainer"] {
        border-color: #2A2D35 !important;
        background: #1A1C23;
        border-radius: 12px;
        padding: 1.5rem;
    }

    hr {
        border-color: #2A2D35 !important;
        margin: 2rem 0 !important;
    }

    .st-emotion-cache-1qg05tj {
        padding: 2rem 1.5rem !important;
    }

    .dark-card {
        background: #1A1C23;
        border: 1px solid #2A2D35;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .dark-card:hover {
        border-color: #4CAF50;
        box-shadow: 0 4px 16px rgba(76,175,80,0.1);
    }
    .dark-card h3 {
        color: #4CAF50;
        margin: 0 0 0.5rem 0;
    }
    .dark-card p {
        color: #AAAAAA;
        margin: 0;
    }

    .kpi-card {
        background: linear-gradient(135deg, #1A1C23, #1E2128);
        border: 1px solid #2A2D35;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        border-color: #4CAF50;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(76,175,80,0.15);
    }
    .kpi-card h3 {
        color: #4CAF50;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }
    .kpi-card p {
        color: #888888;
        margin: 0.3rem 0 0 0;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
    }

    .rec-card {
        background: rgba(255,152,0,0.08);
        border: 1px solid rgba(255,152,0,0.2);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        border-left: 3px solid #FF9800;
        color: #E0E0E0;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .rec-card:hover {
        background: rgba(255,152,0,0.12);
        border-color: rgba(255,152,0,0.3);
    }

    .result-card {
        background: rgba(76,175,80,0.08);
        border: 1px solid rgba(76,175,80,0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .insight-card {
        background: rgba(33,150,243,0.06);
        border: 1px solid rgba(33,150,243,0.15);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.2s;
    }
    .insight-card:hover {
        background: rgba(33,150,243,0.1);
        border-color: rgba(33,150,243,0.3);
    }

    a {
        color: #4CAF50 !important;
    }
    a:hover {
        color: #66BB6A !important;
    }

    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
        .kpi-card h3 { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>\U0001F33E AgroPredict Colombia</h1><p>Optimización y Transferencia Tecnológica en el Sector Agropecuario Colombiano</p></div>', unsafe_allow_html=True)
st.divider()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import base64
import io
import numpy as np
import re
from typing import Dict, List, Tuple, Optional

# --- Wilton Weavers Aviation Carpets & Fine Wool Broadloom Streamlit App ---

# Set page config
st.set_page_config(
    page_title="Wilton Weavers | Aviation Carpets & Fine Wool Broadloom | Kerala, India",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.wilton.in/contact',
        'Report a bug': "https://www.wilton.in/support",
        'About': "# Wilton Weavers BOM Search Platform\nSpecialising in Aviation Carpets & Fine Wool Broadloom since 1982"
    }
)

# --- Session State Initialization ---
if 'design_df' not in st.session_state:
    st.session_state.design_df = None
if 'yarn_df' not in st.session_state:
    st.session_state.yarn_df = None
if 'selected_colors' not in st.session_state:
    st.session_state.selected_colors = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Premium Professional Aviation Carpet Manufacturing Dashboard CSS - High Contrast
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    
    /* Global Professional Styling with High Contrast */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Force white text everywhere */
    * {
        color: #ffffff !important;
    }
    
    /* Executive Header */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #1e40af 100%);
        background-size: 200% 200%;
        animation: headerShine 8s ease infinite;
        padding: 4rem 3rem;
        border-radius: 16px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.6),
            0 0 0 2px rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
        border: 3px solid #ffffff;
    }
    
    @keyframes headerShine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 3.8rem;
        font-weight: 900;
        margin: 0;
        color: #ffffff !important;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.8);
        letter-spacing: -1px;
        position: relative;
        z-index: 2;
    }
    
    .company-location {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 1.5rem 0;
        color: #ffffff !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }
    
    .company-tagline {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 500;
        margin: 2rem auto 0;
        max-width: 700px;
        line-height: 1.7;
        color: #ffffff !important;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
    }
    
    .heritage-badge {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: #ffffff !important;
        padding: 1rem 3rem;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 800;
        margin: 2rem auto;
        display: inline-block;
        box-shadow: 0 8px 25px rgba(220, 38, 38, 0.5);
        text-transform: uppercase;
        letter-spacing: 2px;
        border: 2px solid #ffffff;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    .aviation-badge {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: #ffffff !important;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-left: 1rem;
        display: inline-block;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 2px solid #ffffff;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    /* Executive Section Containers */
    .upload-section, .search-container {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        padding: 3rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        border: 3px solid #ffffff;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.5),
            inset 0 2px 0 rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .upload-section::before, .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e40af 0%, #dc2626 50%, #059669 100%);
    }
    
    .upload-section:hover, .search-container:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 35px 70px rgba(0,0,0,0.6),
            0 0 0 3px rgba(255,255,255,0.8);
    }
    
    .upload-section h3, .search-container h3 {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }
    
    /* Premium Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        color: #ffffff !important;
        text-align: center;
        margin: 1rem;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.4),
            0 0 0 2px rgba(255,255,255,0.3);
        transition: all 0.3s ease;
        border: 2px solid #ffffff;
        position: relative;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.6),
            0 0 50px rgba(30, 64, 175, 0.3);
    }
    
    .metric-number {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        display: block;
        margin-bottom: 1rem;
        color: #ffffff !important;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.8);
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    /* Executive Status Messages */
    .success-message {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: #ffffff !important;
        padding: 2.5rem;
        border-radius: 16px;
        margin: 2rem 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 15px 30px rgba(5, 150, 105, 0.4);
        border: 2px solid #ffffff;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    .error-message {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: #ffffff !important;
        padding: 2.5rem;
        border-radius: 16px;
        margin: 2rem 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 15px 30px rgba(220, 38, 38, 0.4);
        border: 2px solid #ffffff;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    /* Executive Data Display */
    .dataframe-container {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        padding: 3rem;
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin: 2rem 0;
        border: 3px solid #ffffff;
    }
    
    /* Executive Sidebar */
    .sidebar-content {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 3rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: #ffffff !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border: 3px solid #ffffff;
    }
    
    .sidebar-content h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        margin-bottom: 2rem;
        color: #ffffff !important;
        font-size: 1.8rem;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }
    
    /* Executive Welcome Section */
    .welcome-section {
        text-align: center;
        padding: 6rem 3rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        border-radius: 20px;
        margin: 3rem 0;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        border: 3px solid #ffffff;
    }
    
    .welcome-section h2 {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.8);
    }
    
    /* Executive Feature Cards */
    .feature-card {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
        margin: 2rem;
        border: 2px solid #ffffff;
    }
    
    .feature-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.6);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 2rem;
        display: block;
        color: #ffffff !important;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }
    
    .feature-card h4 {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.8);
    }
    
    .feature-card p {
        color: #ffffff !important;
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 500;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    /* Executive Footer */
    .footer {
        text-align: center;
        padding: 5rem 3rem;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
        margin-top: 5rem;
        border-radius: 20px;
        border: 3px solid #ffffff;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }
    
    .footer a {
        color: #ffffff !important;
        text-decoration: none;
        font-weight: 700;
        transition: all 0.3s ease;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    .footer a:hover {
        color: #3b82f6 !important;
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.8);
    }
    
    /* Streamlit Component Overrides - HIGH CONTRAST */
    .stSelectbox > label, 
    .stTextInput > label,
    .stNumberInput > label,
    .stDateInput > label,
    .stTimeInput > label,
    .stCheckbox > label,
    .stRadio > label,
    .stSlider > label,
    .stMultiSelect > label,
    .stFileUploader > label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
    }
    
    /* Input Fields */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stDateInput > div > div,
    .stTimeInput > div > div,
    .stMultiSelect > div > div {
        background-color: #1e293b !important;
        border: 3px solid #ffffff !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3) !important;
    }
    
    .stSelectbox input,
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTimeInput input,
    .stMultiSelect input {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        border: 3px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 1rem 3rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px rgba(5, 150, 105, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 15px 30px rgba(5, 150, 105, 0.6) !important;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        padding: 1rem 2rem !important;
        margin: 0.5rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 64, 175, 0.3) !important;
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
    }
    
    /* Data Tables */
    .dataframe {
        background-color: #1e293b !important;
        border: 3px solid #ffffff !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .dataframe table {
        background-color: #1e293b !important;
        color: #ffffff !important;
        width: 100% !important;
    }
    
    .dataframe th {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        font-weight: 800 !important;
        padding: 1rem !important;
        text-align: center !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
    }
    
    .dataframe td {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        font-weight: 600 !important;
        padding: 0.8rem !important;
        text-align: center !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 6px;
        border: 1px solid #ffffff;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1e40af, #dc2626);
        border-radius: 6px;
        border: 1px solid #ffffff;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3b82f6, #ef4444);
    }
    
    /* Additional High Contrast Elements */
    .stMarkdown, .stText, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .stSidebar {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: 3px solid #ffffff !important;
    }
    
    .stSidebar * {
        color: #ffffff !important;
    }
    
    /* File Uploader */
    .stFileUploader > div {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border: 3px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        text-align: center !important;
    }
    
    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2.5rem !important;
        }
        
        .main-header {
            padding: 3rem 2rem !important;
        }
        
        .upload-section, .search-container {
            padding: 2rem !important;
        }
        
        .feature-card {
            margin: 1rem !important;
        }
        
        .metric-card {
            margin: 0.5rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Utility Functions ---
def clean_design_name(name: str) -> str:
    if pd.isna(name):
        return ""
    return str(name).strip().upper()

def extract_colors_from_text(text: str) -> List[str]:
    if pd.isna(text) or not text:
        return []
    separators = [',', ';', '/', '|', '+', '&', '-']
    colors = [text]
    for sep in separators:
        new_colors = []
        for color in colors:
            new_colors.extend(color.split(sep))
        colors = new_colors
    cleaned_colors = []
    for color in colors:
        color = color.strip().upper()
        if color and color != 'NAN' and len(color) > 1:
            cleaned_colors.append(color)
    return list(set(cleaned_colors))

def get_available_colors(df: pd.DataFrame) -> List[str]:
    if df is None or df.empty:
        return []
    color_columns = [col for col in df.columns if 
                    any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye', 'hue'])]
    all_colors = set()
    for col in color_columns:
        for value in df[col].dropna():
            colors = extract_colors_from_text(str(value))
            all_colors.update(colors)
    if not all_colors:
        all_colors = {
            'NAVY BLUE', 'ROYAL BLUE', 'DEEP BLUE', 'SKY BLUE', 'COBALT BLUE',
            'BURGUNDY', 'WINE RED', 'CRIMSON', 'MAROON', 'CARDINAL RED',
            'FOREST GREEN', 'EMERALD', 'SAGE GREEN', 'OLIVE', 'HUNTER GREEN',
            'CHARCOAL GREY', 'SILVER GREY', 'LIGHT GREY', 'STEEL GREY', 'SLATE GREY',
            'BEIGE', 'CREAM', 'IVORY', 'CHAMPAGNE', 'PEARL WHITE',
            'GOLD', 'BRONZE', 'COPPER', 'AMBER', 'ANTIQUE GOLD',
            'BLACK', 'WHITE', 'PEARL', 'PLATINUM', 'STONE GREY'
        }
    return sorted(list(all_colors))

def create_export_excel(data_dict: Dict[str, pd.DataFrame], filename_prefix: str) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return buffer.getvalue()

def display_metrics_cards(metrics: Dict[str, int]):
    cols = st.columns(len(metrics))
    for i, (label, value) in enumerate(metrics.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-number">{value}</span>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>✈️ WILTON WEAVERS</h1>
    <div class="company-location">KERALA • INDIA</div>
    <div class="heritage-badge">Est. 1982 • 40+ Years of Excellence</div>
    <div class="company-tagline">
        Specialists in Aviation Carpets & Fine Wool Broadloom<br>
        Manufacturers of Quality Floor Coverings • Innovators Par Excellence
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🚀 BOM Search Platform</h3>
        <p><strong>Quick Start Guide:</strong></p>
        <p>1️⃣ Upload Design Master Excel</p>
        <p>2️⃣ Upload Yarn Specifications</p>
        <p>3️⃣ Search Aviation Carpet Designs</p>
        <p>4️⃣ Analyze Quality Metrics</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2c3e50, #34495e); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
        <h4 style="color: #ecf0f1; margin-bottom: 1rem;">🏭 Company Info</h4>
        <p style="margin: 0.5rem 0;"><strong>Specialization:</strong><br>Aviation Carpets & Fine Wool</p>
        <p style="margin: 0.5rem 0;"><strong>Experience:</strong><br>40+ Years Collective Expertise</p>
        <p style="margin: 0.5rem 0;"><strong>Type:</strong><br>Private Family Business</p>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.design_df is not None and st.session_state.yarn_df is not None:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
            <h4 style="margin-bottom: 1rem;">📊 Database Statistics</h4>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Design Records", len(st.session_state.design_df), delta="Active")
        with col2:
            st.metric("Yarn Records", len(st.session_state.yarn_df), delta="Active")
        unique_designs = st.session_state.design_df['Design Name'].nunique() if 'Design Name' in st.session_state.design_df.columns else 0
        st.metric("Unique Designs", unique_designs, delta="Available")
    if st.session_state.search_history:
        st.markdown("---")
        st.markdown("""
        <div class="search-history">
            <h5 style="margin-bottom: 0.5rem;">🔍 Recent Searches</h5>
        </div>
        """, unsafe_allow_html=True)
        for search in st.session_state.search_history[-3:]:
            if st.button(f"🔄 {search}", key=f"history_{search}"):
                st.session_state.search_input = search
                st.experimental_rerun()
    st.markdown("---")
    st.subheader("🎯 Advanced Features")
    show_analytics = st.checkbox("📈 Analytics Dashboard", value=True)
    show_export = st.checkbox("📥 Export Options", value=True)
    auto_refresh = st.checkbox("🔄 Auto-refresh Results", value=False)
    case_sensitive = st.checkbox("🔤 Case Sensitive Search", value=False)
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
        <h5 style="margin-bottom: 0.5rem;">📞 Need Support?</h5>
        <p style="margin: 0; font-size: 0.9rem;">Visit: <a href="https://www.wilton.in" target="_blank" style="color: #ffeaa7;">wilton.in</a></p>
    </div>
    """, unsafe_allow_html=True)

# --- File Upload Section ---
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class="upload-section">
        <h3>📋 Design Master Database</h3>
        <p style="color: #7f8c8d; font-family: 'Inter', sans-serif;">Upload your comprehensive design master Excel file containing aviation carpet specifications and patterns</p>
    </div>
    """, unsafe_allow_html=True)
    design_file = st.file_uploader(
        "Choose Design Master Excel File",
        type=["xlsx", "xls"],
        help="Upload your design master Excel file containing carpet patterns, specifications, and aviation standards",
        key="design_upload"
    )
with col2:
    st.markdown("""
    <div class="upload-section">
        <h3>🧶 Yarn Specifications</h3>
        <p style="color: #7f8c8d; font-family: 'Inter', sans-serif;">Upload your yarn database containing fine wool specifications, aviation-grade materials, and quality standards</p>
    </div>
    """, unsafe_allow_html=True)
    yarn_file = st.file_uploader(
        "Choose Yarn Specifications Excel File",
        type=["xlsx", "xls"],
        help="Upload your yarn specifications file containing wool grades, aviation compliance, and material properties",
        key="yarn_upload"
    )

# --- Multi-Filter Section (Color, Construction, No. of Frames) ---
st.markdown("""
<div class="color-filter-section">
    <h3>🎨 Multi-Filter Design Search</h3>
    <p style="color: #7f8c8d; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Select multiple colors, construction, and number of frames to find aviation carpet designs that match your criteria.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Filter Option Preparation ---
available_colors = []
available_constructions = []
available_frames = []

if st.session_state.design_df is not None:
    df = st.session_state.design_df
    # Colors
    color_columns = [col for col in df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
    for col in color_columns:
        colors_in_col = df[col].dropna().astype(str).str.split(',|;|/|\\|').explode().str.strip().str.upper().unique()
        available_colors.extend(colors_in_col)
    available_colors = sorted(list(set([color for color in available_colors if color and color != 'NAN'])))
    # Construction
    construction_col = None
    for col in df.columns:
        if 'construction' in col.lower():
            construction_col = col
            break
    if construction_col:
        available_constructions = sorted(df[construction_col].dropna().astype(str).str.strip().unique())
    # No. of Frames
    frames_col = None
    for col in df.columns:
        if 'frame' in col.lower():
            frames_col = col
            break
    if frames_col:
        available_frames = sorted(df[frames_col].dropna().astype(str).str.strip().unique())

if not available_colors:
    available_colors = [
        'NAVY BLUE', 'ROYAL BLUE', 'DEEP BLUE', 'SKY BLUE',
        'BURGUNDY', 'WINE RED', 'CRIMSON', 'MAROON',
        'FOREST GREEN', 'EMERALD', 'SAGE GREEN', 'OLIVE',
        'CHARCOAL GREY', 'SILVER GREY', 'LIGHT GREY', 'STEEL GREY',
        'BEIGE', 'CREAM', 'IVORY', 'CHAMPAGNE',
        'GOLD', 'BRONZE', 'COPPER', 'AMBER',
        'BLACK', 'WHITE', 'PEARL', 'PLATINUM'
    ]

# --- Filter UI ---
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
with col1:
    selected_colors = st.multiselect(
        "🎨 Select Colors (Choose multiple colors used in carpet design)",
        options=available_colors,
        help="Select one or more colors that should be present in the carpet design. The system will find designs using these color combinations.",
        key="color_multiselect"
    )
with col2:
    selected_construction = st.selectbox(
        "🏗️ Construction",
        options=["Any"] + available_constructions if available_constructions else ["Any"],
        help="Filter by construction type (e.g., WILTON, AXMINSTER, TUFTED, etc.)"
    )
with col3:
    selected_frames = st.selectbox(
        "🖼️ No. of Frames",
        options=["Any"] + available_frames if available_frames else ["Any"],
        help="Filter by number of frames (if available in your data)"
    )
with col4:
    match_type = st.radio(
        "Match Type:",
        options=["All Colors (AND)", "Any Color (OR)"],
        help="All Colors: Design must contain ALL selected colors\nAny Color: Design must contain AT LEAST ONE selected color",
        key="match_type"
    )
    color_search_button = st.button("🔍 SEARCH BY FILTERS", type="secondary")

# --- Display Selected Filters ---
if selected_colors or (selected_construction and selected_construction != "Any") or (selected_frames and selected_frames != "Any"):
    st.markdown("**Selected Filters:**")
    chips = ""
    for color in selected_colors:
        chips += f'<span class="color-chip">{color}</span> '
    if selected_construction and selected_construction != "Any":
        chips += f'<span class="color-chip" style="background:#1e40af;">{selected_construction}</span> '
    if selected_frames and selected_frames != "Any":
        chips += f'<span class="color-chip" style="background:#8b4513;">{selected_frames} Frames</span> '
    st.markdown(chips, unsafe_allow_html=True)
    match_info = "Exact Match" if match_type == "All Colors (AND)" else "Partial Match"
    st.markdown(f"""
    <div class="match-type-info">
        🎯 Search Mode: <strong>{match_info}</strong> - 
        {"All selected colors must be present in the design" if match_type == "All Colors (AND)" else "At least one selected color must be present in the design"}
    </div>
    """, unsafe_allow_html=True)

# --- File Processing ---
if design_file is not None and yarn_file is not None:
    try:
        with st.spinner('🔄 Processing Aviation Carpet Database...'):
            design_df = pd.read_excel(design_file)
            yarn_df = pd.read_excel(yarn_file)
            st.session_state.design_df = design_df
            st.session_state.yarn_df = yarn_df
            design_df.columns = design_df.columns.str.strip().str.title()
            yarn_df.columns = yarn_df.columns.str.strip().str.title()
            if 'Design Name' in design_df.columns:
                design_df['Design Name'] = design_df['Design Name'].astype(str).str.strip()
                if not case_sensitive:
                    design_df['Design Name'] = design_df['Design Name'].str.upper()
            if 'Design Name' in yarn_df.columns:
                yarn_df['Design Name'] = yarn_df['Design Name'].astype(str).str.strip()
                if not case_sensitive:
                    yarn_df['Design Name'] = yarn_df['Design Name'].str.upper()
        st.markdown("""
        <div class="success-message">
            ✅ Aviation Carpet Database Successfully Loaded! Ready for Professional Design Search.
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-number">{len(design_df)}</span>
                <div class="metric-label">Design Records</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-number">{len(yarn_df)}</span>
                <div class="metric-label">Yarn Specifications</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            unique_designs = design_df['Design Name'].nunique() if 'Design Name' in design_df.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-number">{unique_designs}</span>
                <div class="metric-label">Unique Designs</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-number">{len(design_df.columns) + len(yarn_df.columns)}</span>
                <div class="metric-label">Data Attributes</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div class="search-container">
            <h3>🔍 Aviation Carpet Design Search</h3>
            <p style="color: #7f8c8d; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
                Search across our comprehensive database of aviation-grade carpet designs and fine wool specifications
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        with col1:
            design_input = st.text_input(
                "🎯 Design Name Search",
                placeholder="Enter aviation carpet design name (e.g., 'BOEING-737', 'AIRBUS-A320', etc.)",
                help="Search supports partial matches and is case-insensitive. Try aircraft model numbers or pattern names.",
                key="search_input"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_button = st.button("🔍 SEARCH DATABASE", type="primary")
        if design_input or search_button:
            if design_input:
                design_input_clean = design_input.strip()
                if not case_sensitive:
                    design_input_clean = design_input_clean.upper()
                with st.spinner('🔍 Searching Aviation Carpet Database...'):
                    if case_sensitive:
                        design_matches = design_df[design_df['Design Name'].str.contains(design_input_clean, na=False)] if 'Design Name' in design_df.columns else pd.DataFrame()
                        yarn_matches = yarn_df[yarn_df['Design Name'].str.contains(design_input_clean, na=False)] if 'Design Name' in yarn_df.columns else pd.DataFrame()
                    else:
                        design_matches = design_df[design_df['Design Name'].str.contains(design_input_clean, na=False, case=False)] if 'Design Name' in design_df.columns else pd.DataFrame()
                        yarn_matches = yarn_df[yarn_df['Design Name'].str.contains(design_input_clean, na=False, case=False)] if 'Design Name' in yarn_df.columns else pd.DataFrame()
                if not design_matches.empty and not yarn_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Perfect Match Found! Design and Yarn Specifications Located in Database
                    </div>
                    """, unsafe_allow_html=True)
                    merged = pd.merge(design_matches, yarn_matches, on='Design Name', how='left')
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📊 Complete Specification", 
                        "🎨 Design Details", 
                        "🧶 Yarn & Material", 
                        "📈 Quality Analytics"
                    ])
                    with tab1:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🔧 Complete Aviation Carpet Specification")
                        st.markdown("*Combined design and yarn specifications for aviation-grade floor coverings*")
                        st.dataframe(merged, use_container_width=True, height=400)
                        if show_export:
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                merged.to_excel(writer, sheet_name='Complete_Specification', index=False)
                                design_matches.to_excel(writer, sheet_name='Design_Details', index=False)
                                yarn_matches.to_excel(writer, sheet_name='Yarn_Specifications', index=False)
                            st.download_button(
                                label="📥 Download Complete Specification",
                                data=buffer.getvalue(),
                                file_name=f"WiltonWeavers_AviationCarpet_{design_input_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)
                    with tab2:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🎨 Aviation Carpet Design Details")
                        st.markdown("*Comprehensive design specifications, patterns, and aviation compliance standards*")
                        st.dataframe(design_matches, use_container_width=True, height=400)
                        if len(design_matches) > 0:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Design Variants", len(design_matches))
                            with col2:
                                st.metric("Data Points", len(design_matches.columns))
                            with col3:
                                if 'Pattern Type' in design_matches.columns:
                                    pattern_types = design_matches['Pattern Type'].nunique()
                                    st.metric("Pattern Types", pattern_types)
                                else:
                                    st.metric("Records Found", len(design_matches))
                        st.markdown('</div>', unsafe_allow_html=True)
                    with tab3:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🧶 Fine Wool & Yarn Specifications")
                        st.markdown("*Premium yarn specifications, wool grades, and material properties for aviation use*")
                        st.dataframe(yarn_matches, use_container_width=True, height=400)
                        if len(yarn_matches) > 0:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Yarn Specifications", len(yarn_matches))
                            with col2:
                                if 'Yarn Type' in yarn_matches.columns:
                                    yarn_types = yarn_matches['Yarn Type'].nunique()
                                    st.metric("Yarn Types", yarn_types)
                                else:
                                    st.metric("Specification Points", len(yarn_matches.columns))
                            with col3:
                                if 'Quality Grade' in yarn_matches.columns:
                                    quality_grades = yarn_matches['Quality Grade'].nunique()
                                    st.metric("Quality Grades", quality_grades)
                                else:
                                    st.metric("Material Records", len(yarn_matches))
                        st.markdown('</div>', unsafe_allow_html=True)
                    with tab4:
                        if show_analytics:
                            st.subheader("📈 Aviation Carpet Quality Analytics")
                            st.markdown("*Advanced analytics for design performance, material quality, and manufacturing insights*")
                            col1, col2 = st.columns(2)
                            with col1:
                                fig = go.Figure()
                                fig.add_trace(go.Bar(
                                    name='Design Records',
                                    x=['Design Database'],
                                    y=[len(design_matches)],
                                    marker=dict(
                                        color='rgba(52, 152, 219, 0.8)',
                                        line=dict(color='rgba(52, 152, 219, 1.0)', width=2)
                                    ),
                                    text=[len(design_matches)],
                                    textposition='auto',
                                ))
                                fig.add_trace(go.Bar(
                                    name='Yarn Specifications',
                                    x=['Yarn Database'],
                                    y=[len(yarn_matches)],
                                    marker=dict(
                                        color='rgba(231, 76, 60, 0.8)',
                                        line=dict(color='rgba(231, 76, 60, 1.0)', width=2)
                                    ),
                                    text=[len(yarn_matches)],
                                    textposition='auto',
                                ))
                                fig.update_layout(
                                    title="Database Records Found",
                                    xaxis_title="Database Category",
                                    yaxis_title="Record Count",
                                    height=400,
                                    font=dict(family="Inter, sans-serif"),
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    showlegend=True
                                )
                                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
                                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
                                st.plotly_chart(fig, use_container_width=True)
                            with col2:
                                st.markdown("""
                                <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 2rem; border-radius: 15px; border-left: 4px solid #3498db;">
                                    <h4 style="color: #2c3e50; margin-bottom: 1.5rem;">🏆 Quality Metrics</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                total_matches = len(design_matches) + len(yarn_matches)
                                st.metric("Total Matches", total_matches, delta="Complete Dataset")
                                st.metric("Design Matches", len(design_matches), delta="Aviation Grade")
                                st.metric("Yarn Matches", len(yarn_matches), delta="Fine Wool")
                                st.metric("Combined Records", len(merged), delta="Ready for Production")
                                if total_matches > 0:
                                    completion_rate = (len(merged) / max(len(design_matches), len(yarn_matches))) * 100
                                    st.metric("Specification Completeness", f"{completion_rate:.1f}%", delta="Quality Assured")
                elif not design_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ⚠️ Design Found in Design Database Only - Yarn Specifications May Need Separate Lookup
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.subheader("🎨 Aviation Carpet Design Details")
                    st.markdown("*Found in design database - yarn specifications not matched*")
                    st.dataframe(design_matches, use_container_width=True, height=400)
                    st.markdown('</div>', unsafe_allow_html=True)
                elif not yarn_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ⚠️ Yarn Specifications Found Only - Design Details May Need Separate Lookup
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.subheader("🧶 Fine Wool & Yarn Specifications")
                    st.markdown("*Found in yarn database - design details not matched*")
                    st.dataframe(yarn_matches, use_container_width=True, height=400)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ No Matching Aviation Carpet Designs Found in Database
                    </div>
                    """, unsafe_allow_html=True)
                    if 'Design Name' in design_df.columns:
                        search_term = design_input_clean[:3] if len(design_input_clean) >= 3 else design_input_clean
                        if case_sensitive:
                            partial_matches = design_df[design_df['Design Name'].str.contains(search_term, na=False)]['Design Name'].unique()[:8]
                        else:
                            partial_matches = design_df[design_df['Design Name'].str.contains(search_term, na=False, case=False)]['Design Name'].unique()[:8]
                        if len(partial_matches) > 0:
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #f39c12, #e67e22); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                                <h4 style="margin-bottom: 1rem;">💡 Similar Aviation Carpet Designs Found:</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            cols = st.columns(min(4, len(partial_matches)))
                            for i, suggestion in enumerate(partial_matches):
                                with cols[i % len(cols)]:
                                    if st.button(f"🔍 {suggestion}", key=f"suggestion_{i}"):
                                        st.session_state.search_input = suggestion
                                        st.rerun()
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 1.5rem; border-radius: 15px; text-align: center;">
                    ⚠️ Please enter a design name to search the aviation carpet database
                </div>
                """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Database Processing Error: {str(e)}
            <br><small>Please ensure your Excel files contain proper column headers and design names.</small>
        </div>
        """, unsafe_allow_html=True)

# --- Multi-Filter Search (Color, Construction, No. of Frames) ---
if (selected_colors or (selected_construction and selected_construction != "Any") or (selected_frames and selected_frames != "Any")) and (color_search_button or auto_refresh):
    if st.session_state.design_df is not None:
        df = st.session_state.design_df
        with st.spinner('🎨 Searching designs by selected filters...'):
            # Prepare color columns
            color_columns = [col for col in df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
            construction_col = None
            for col in df.columns:
                if 'construction' in col.lower():
                    construction_col = col
                    break
            frames_col = None
            for col in df.columns:
                if 'frame' in col.lower():
                    frames_col = col
                    break

            matches = []
            for idx, row in df.iterrows():
                # --- Color Matching ---
                row_colors = []
                for col in color_columns:
                    if pd.notna(row[col]):
                        text = str(row[col]).upper()
                        for delimiter in [',', ';', '/', '|', '-', '+', '&']:
                            text = text.replace(delimiter, ',')
                        color_parts = [c.strip().replace(' ', '') for c in text.split(',') if c.strip()]
                        row_colors.extend([c for c in color_parts if len(c) > 1])
                row_colors = list(set(row_colors))
                color_pass = True
                if selected_colors:
                    if match_type == "All Colors (AND)":
                        normalized_row_colors = sorted([c.upper() for c in row_colors])
                        normalized_selected_colors = sorted([c.upper().replace(' ', '') for c in selected_colors])
                        color_pass = normalized_row_colors == normalized_selected_colors
                    else:
                        color_pass = any(selected_color.replace(' ', '').upper() in [c.upper() for c in row_colors] for selected_color in selected_colors)
                # --- Construction Matching ---
                construction_pass = True
                if selected_construction and selected_construction != "Any" and construction_col:
                    construction_pass = str(row[construction_col]).strip() == selected_construction
                # --- Frames Matching ---
                frames_pass = True
                if selected_frames and selected_frames != "Any" and frames_col:
                    frames_pass = str(row[frames_col]).strip() == selected_frames
                # --- Final Decision ---
                if color_pass and construction_pass and frames_pass:
                    matches.append(idx)
            filtered_df = df.iloc[matches].copy() if matches else pd.DataFrame()

            # Find matching yarn data
            yarn_matches = pd.DataFrame()
            if (st.session_state.yarn_df is not None and 
                not filtered_df.empty and 
                'Design Name' in filtered_df.columns):
                design_names = filtered_df['Design Name'].unique()
                yarn_matches = st.session_state.yarn_df[
                    st.session_state.yarn_df['Design Name'].isin(design_names)
                ] if 'Design Name' in st.session_state.yarn_df.columns else pd.DataFrame()

            # --- Display Results ---
            if not filtered_df.empty:
                st.success(f"Found {len(filtered_df)} designs matching your filter criteria:")
                st.dataframe(filtered_df)
                if not yarn_matches.empty:
                    st.info(f"Related yarn information ({len(yarn_matches)} entries):")
                    st.dataframe(yarn_matches)
                # Show metrics and tabs for results
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="metric-number">{len(filtered_df)}</span>
                        <div class="metric-label">Matching Designs</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    unique_designs = filtered_df['Design Name'].nunique() if 'Design Name' in filtered_df.columns else len(filtered_df)
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="metric-number">{unique_designs}</span>
                        <div class="metric-label">Unique Patterns</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="metric-number">{len(selected_colors)}</span>
                        <div class="metric-label">Colors Selected</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    yarn_count = len(yarn_matches) if not yarn_matches.empty else 0
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="metric-number">{yarn_count}</span>
                        <div class="metric-label">Yarn Matches</div>
                    </div>
                    """, unsafe_allow_html=True)
                if not yarn_matches.empty:
                    merged_color = pd.merge(filtered_df, yarn_matches, on='Design Name', how='left')
                    tab1, tab2, tab3 = st.tabs([
                        "🎨 Filtered Designs", 
                        "🧶 Corresponding Yarn Specs", 
                        "📊 Complete Filtered Specification"
                    ])
                    with tab1:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🎨 Designs Matching Your Filters")
                        st.markdown(f"*Found {len(filtered_df)} designs using your filter criteria*")
                        st.dataframe(filtered_df, use_container_width=True, height=400)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with tab2:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🧶 Yarn Specifications for Filtered Designs")
                        st.dataframe(yarn_matches, use_container_width=True, height=400)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with tab3:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("📊 Complete Specification (Design + Yarn)")
                        st.dataframe(merged_color, use_container_width=True, height=400)
                        if show_export:
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                merged_color.to_excel(writer, sheet_name='Filtered_Complete', index=False)
                            st.download_button(
                                label="📥 Download Filtered Specification",
                                data=buffer.getvalue(),
                                file_name=f"WiltonWeavers_Filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-message">
                    ❌ No Matching Aviation Carpet Designs Found for Selected Filters
                </div>
                """, unsafe_allow_html=True)

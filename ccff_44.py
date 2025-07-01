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

# Start of Wilton Weavers Aviation Carpets & Fine Wool Broadloom Streamlit App

# Set page config with enhanced styling
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

# Initialize session state
if 'design_df' not in st.session_state:
    st.session_state.design_df = None
if 'yarn_df' not in st.session_state:
    st.session_state.yarn_df = None
if 'selected_colors' not in st.session_state:
    st.session_state.selected_colors = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Enhanced Custom CSS with premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #0d1421 0%, #1a2332 25%, #2c3e50 50%, #34495e 75%, #2c3e50 100%);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 3rem 2rem;
        border-radius: 20px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15), 0 0 80px rgba(52, 73, 94, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="carpet-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><rect fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.5" width="20" height="20"/><circle fill="rgba(255,255,255,0.03)" cx="10" cy="10" r="2"/></pattern></defs><rect width="100" height="100" fill="url(%23carpet-pattern)"/></svg>');
        opacity: 0.4;
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 4.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        letter-spacing: -2px;
        position: relative;
        z-index: 2;
    }
    
    .company-location {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0.5rem 0;
        color: #ecf0f1;
        letter-spacing: 2px;
        text-transform: uppercase;
        position: relative;
        z-index: 2;
    }
    
    .company-tagline {
        font-family: 'Crimson Text', serif;
        font-size: 1.3rem;
        font-weight: 400;
        margin: 1.5rem auto 0;
        max-width: 800px;
        line-height: 1.6;
        color: #bdc3c7;
        font-style: italic;
        position: relative;
        z-index: 2;
    }
    
    .heritage-badge {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 1rem auto;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
        position: relative;
        z-index: 2;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 3px solid transparent;
        background-clip: padding-box;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .upload-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3498db, #e74c3c, #f39c12, #27ae60);
        border-radius: 20px 20px 0 0;
    }
    
    .upload-section:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .upload-section h3 {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .search-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 6px solid #3498db;
        position: relative;
    }
    
    .search-container::before {
        content: '🔍';
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 2rem;
        background: linear-gradient(135deg, #3498db, #2980b9);
        padding: 10px;
        border-radius: 50%;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    
    .search-container h3 {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
        opacity: 0;
    }
    
    .metric-card:hover::before {
        animation: shimmer 0.6s ease-in-out;
        opacity: 1;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .metric-number {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .success-message {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
        animation: slideInFromTop 0.5s ease-out;
    }
    
    @keyframes slideInFromTop {
        0% { transform: translateY(-20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    .error-message {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 8px 25px rgba(231, 76, 60, 0.3);
    }
    
    .dataframe-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 1px solid #e9ecef;
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #74b9ff 0%, #55a3ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 6px 20px rgba(116, 185, 255, 0.3);
    }
    
    .sidebar-content h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .welcome-section {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="welcome-pattern" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse"><rect fill="none" stroke="rgba(52,73,94,0.05)" stroke-width="1" width="40" height="40"/><circle fill="rgba(52,73,94,0.03)" cx="20" cy="20" r="3"/></pattern></defs><rect width="100" height="100" fill="url(%23welcome-pattern)"/></svg>');
        opacity: 0.6;
    }
    
    .welcome-section h2 {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
    }
    
    .feature-card {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        margin: 1rem;
        position: relative;
        z-index: 2;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-card h4 {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: #ecf0f1;
        font-family: 'Inter', sans-serif;
        margin-top: 4rem;
        border-radius: 20px 20px 0 0;
    }
    
    .footer a {
        color: #3498db;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer a:hover {
        color: #5dade2;
        text-decoration: underline;
    }
    
    .stSelectbox > label, .stTextInput > label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #2c3e50;
        font-size: 1.1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 30px rgba(52, 152, 219, 0.4);
        background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 10px;
        color: #2c3e50;
    }
    
    .aviation-badge {
        background: linear-gradient(135deg, #f39c12, #e67e22);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Utility Functions
def clean_design_name(name: str) -> str:
    """Clean and standardize design names"""
    if pd.isna(name):
        return ""
    return str(name).strip().upper()

def extract_colors_from_text(text: str) -> List[str]:
    """Extract colors from text with various separators"""
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

def search_designs_by_colors(df: pd.DataFrame, selected_colors: List[str], match_type: str) -> pd.DataFrame:
    """Search designs by color combinations"""
    if df is None or df.empty or not selected_colors:
        return pd.DataFrame()
    color_columns = [col for col in df.columns if 
                    any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye', 'hue'])]
    if not color_columns:
        return pd.DataFrame()
    matching_rows = []
    for idx, row in df.iterrows():
        row_colors = []
        for col in color_columns:
            if pd.notna(row[col]):
                colors_in_cell = extract_colors_from_text(str(row[col]))
                row_colors.extend(colors_in_cell)
        row_colors = list(set(row_colors))
        if match_type == "All Colors (AND)":
            if all(color in row_colors for color in selected_colors):
                matching_rows.append(idx)
        else:
            if any(color in row_colors for color in selected_colors):
                matching_rows.append(idx)
    return df.iloc[matching_rows].copy() if matching_rows else pd.DataFrame()

def get_available_colors(df: pd.DataFrame) -> List[str]:
    """Extract all available colors from dataframe"""
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
    """Create Excel file with multiple sheets"""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return buffer.getvalue()

def display_metrics_cards(metrics: Dict[str, int]):
    """Display metrics in attractive cards"""
    cols = st.columns(len(metrics))
    for i, (label, value) in enumerate(metrics.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-number">{value}</span>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# Enhanced Header with company branding
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

# Enhanced Sidebar
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

# Main content area - File Upload Section
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

# Multi-color filtering section
st.markdown("""
<div class="color-filter-section">
    <h3>🎨 Multi-Color Design Search</h3>
    <p style="color: #7f8c8d; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Select multiple colors to find aviation carpet designs that use these color combinations
    </p>
</div>
""", unsafe_allow_html=True)

# Color selection interface
col1, col2 = st.columns([3, 1])
with col1:
    available_colors = []
    if st.session_state.design_df is not None:
        color_columns = [col for col in st.session_state.design_df.columns if 
                        any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
        if color_columns:
            for col in color_columns:
                colors_in_col = st.session_state.design_df[col].dropna().astype(str).str.split(',|;|/|\\|').explode().str.strip().str.upper().unique()
                available_colors.extend(colors_in_col)
        available_colors = sorted(list(set([color for color in available_colors if color and color != 'NAN'])))
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
    selected_colors = st.multiselect(
        "🎨 Select Colors (Choose multiple colors used in carpet design)",
        options=available_colors,
        help="Select one or more colors that should be present in the carpet design. The system will find designs using these color combinations.",
        key="color_multiselect"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    match_type = st.radio(
        "Match Type:",
        options=["All Colors (AND)", "Any Color (OR)"],
        help="All Colors: Design must contain ALL selected colors\nAny Color: Design must contain AT LEAST ONE selected color",
        key="match_type"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    color_search_button = st.button("🔍 SEARCH BY COLORS", type="secondary")

# Display selected colors
if selected_colors:
    st.markdown("**Selected Colors:**")
    color_chips = ""
    for color in selected_colors:
        color_chips += f'<span class="color-chip">{color}</span>'
    st.markdown(color_chips, unsafe_allow_html=True)
    match_info = "Exact Match" if match_type == "All Colors (AND)" else "Partial Match"
    st.markdown(f"""
    <div class="match-type-info">
        🎯 Search Mode: <strong>{match_info}</strong> - 
        {"All selected colors must be present in the design" if match_type == "All Colors (AND)" else "At least one selected color must be present in the design"}
    </div>
    """, unsafe_allow_html=True)

# File processing with enhanced feedback
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

# Color-based search functionality
if selected_colors and (color_search_button or auto_refresh):
    if st.session_state.design_df is not None:
        with st.spinner('🎨 Searching designs by color combinations...'):
            # Find color-related columns
            color_columns = [col for col in st.session_state.design_df.columns if 
                            any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
            
            if color_columns:
                design_color_matches = pd.DataFrame()
                
                for _, row in st.session_state.design_df.iterrows():
                    row_colors = []
                    
                    # Extract and normalize colors from all color columns
                    for col in color_columns:
                        if pd.notna(row[col]):
                            # Use the robust color extraction function from your utilities
                            row_colors.extend(extract_colors_from_text(str(row[col])))
                    
                    # Remove duplicates and normalize
                    row_colors = [color.replace(' ', '').upper() for color in set(row_colors)]
                    
                    # Check color matching based on match type
                    if match_type == "All Colors (AND)":
                        # All selected colors must be present (exact, space-insensitive match)
                        if all(selected_color.replace(' ', '').upper() in row_colors for selected_color in selected_colors):
                            design_color_matches = pd.concat([design_color_matches, row.to_frame().T], ignore_index=True)
                    else:
                        # Any selected color must be present (OR logic)
                        if any(selected_color.replace(' ', '').upper() in row_colors for selected_color in selected_colors):
                            design_color_matches = pd.concat([design_color_matches, row.to_frame().T], ignore_index=True)
                yarn_color_matches = pd.DataFrame()
                if st.session_state.yarn_df is not None and not design_color_matches.empty and 'Design Name' in design_color_matches.columns:
                    design_names = design_color_matches['Design Name'].unique()
                    yarn_color_matches = st.session_state.yarn_df[
                        st.session_state.yarn_df['Design Name'].isin(design_names)
                    ] if 'Design Name' in st.session_state.yarn_df.columns else pd.DataFrame()
                if not design_color_matches.empty:
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Found {len(design_color_matches)} Aviation Carpet Design(s) Using Selected Color Combination!
                    </div>
                    """, unsafe_allow_html=True)
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <span class="metric-number">{len(design_color_matches)}</span>
                            <div class="metric-label">Matching Designs</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        unique_designs = design_color_matches['Design Name'].nunique() if 'Design Name' in design_color_matches.columns else len(design_color_matches)
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
                        yarn_count = len(yarn_color_matches) if not yarn_color_matches.empty else 0
                        st.markdown(f"""
                        <div class="metric-card">
                            <span class="metric-number">{yarn_count}</span>
                            <div class="metric-label">Yarn Matches</div>
                        </div>
                        """, unsafe_allow_html=True)
                    if not yarn_color_matches.empty:
                        merged_color = pd.merge(design_color_matches, yarn_color_matches, on='Design Name', how='left')
                        tab1, tab2, tab3 = st.tabs([
                            "🎨 Color-Matched Designs", 
                            "🧶 Corresponding Yarn Specs", 
                            "📊 Complete Color Specification"
                        ])
                        with tab1:
                            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                            st.subheader("🎨 Designs Matching Your Color Selection")
                            st.markdown(f"*Found {len(design_color_matches)} designs using {match_info.lower()} criteria*")
                            st.dataframe(design_color_matches, use_container_width=True, height=400)
                            st.markdown('</div>', unsafe_allow_html=True)
                        with tab2:
                            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                            st.subheader("🧶 Yarn Specifications for Color-Matched Designs")
                            st.dataframe(yarn_color_matches, use_container_width=True, height=400)
                            st.markdown('</div>', unsafe_allow_html=True)
                        with tab3:
                            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                            st.subheader("📊 Complete Specification (Design + Yarn)")
                            st.dataframe(merged_color, use_container_width=True, height=400)
                            if show_export:
                                buffer = io.BytesIO()
                                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                    merged_color.to_excel(writer, sheet_name='Color_Matched_Complete', index=False)
                                    design_color_matches.to_excel(writer, sheet_name='Color_Matched_Designs', index=False)
                                    yarn_color_matches.to_excel(writer, sheet_name='Corresponding_Yarn', index=False)
                                color_string = "_".join(selected_colors[:3])
                                st.download_button(
                                    label="📥 Download Color-Matched Specifications",
                                    data=buffer.getvalue(),
                                    file_name=f"WiltonWeavers_ColorSearch_{color_string}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🎨 Designs Matching Your Color Selection")
                        st.markdown(f"*Found {len(design_color_matches)} designs using {match_info.lower()} criteria*")
                        st.dataframe(design_color_matches, use_container_width=True, height=400)
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ No Aviation Carpet Designs Found Using Selected Color Combination
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #f39c12, #e67e22); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                        <h4 style="margin-bottom: 1rem;">💡 Try These Popular Aviation Color Combinations:</h4>
                        <p>• Navy Blue + Gold • Burgundy + Cream • Charcoal Grey + Silver • Royal Blue + White</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-message">
                    ❌ No color-related columns found in the design database. Please ensure your data includes color specifications.
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 1.5rem; border-radius: 15px; text-align: center;">
            ⚠️ Please upload design database first to search by colors
        </div>
        """, unsafe_allow_html=True)

# Store selected colors in session state for sidebar display
if selected_colors:
    st.session_state.selected_colors = selected_colors

# Feature cards section
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🔍</span>
        <h4>Advanced Search</h4>
        <p style="color: #7f8c8d; font-family: 'Inter', sans-serif;">Search aviation carpet designs by name, pattern, or specifications with intelligent matching algorithms</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📊</span>
        <h4>Quality Analytics</h4>
        <p style="color: #7f8c8d; font-family: 'Inter', sans-serif;">Comprehensive analysis of design metrics, yarn specifications, and manufacturing quality standards</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">✈️</span>
        <h4>Aviation Grade</h4>
        <p style="color: #7f8c8d; font-family: 'Inter', sans-serif;">Specialized in aviation industry standards with fire-resistant and durable fine wool broadloom solutions</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
<div class="footer">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 2rem; text-align: left;">
        <div>
            <h4 style="color: #3498db; margin-bottom: 1rem;">✈️ Wilton Weavers</h4>
            <p style="margin: 0.5rem 0;">Aviation Carpets & Fine Wool Broadloom</p>
            <p style="margin: 0.5rem 0;">Kerala, India • Est. 1982</p>
            <p style="margin: 0.5rem 0;">Quality Floor Coverings Since 40+ Years</p>
        </div>
        <div>
            <h4 style="color: #3498db; margin-bottom: 1rem;">🌐 Connect With Us</h4>
            <p style="margin: 0.5rem 0;">Website: <a href="https://www.wilton.in" target="_blank">www.wilton.in</a></p>
            <p style="margin: 0.5rem 0;">Specializing in Aviation Industry</p>
            <p style="margin: 0.5rem 0;">Premium Quality Assurance</p>
        </div>
        <div>
            <h4 style="color: #3498db; margin-bottom: 1rem;">🏭 Our Expertise</h4>
            <p style="margin: 0.5rem 0;">• Aviation Grade Carpets</p>
            <p style="margin: 0.5rem 0;">• Fine Wool Broadloom</p>
            <p style="margin: 0.5rem 0;">• Custom Design Solutions</p>
        </div>
    </div>
    <div style="text-align: center; padding-top: 2rem; border-top: 1px solid #7f8c8d;">
        <p style="margin: 0; color: #bdc3c7;">© 2024 Wilton Weavers • All Rights Reserved • Professional BOM Search Platform</p>
        <p style="margin: 0.5rem 0; color: #95a5a6; font-size: 0.9rem;">Crafted with Excellence for Aviation Industry Professionals</p>
    </div>
</div>
""", unsafe_allow_html=True)

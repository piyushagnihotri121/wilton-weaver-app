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

# --- CSS Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }
    
    .company-location {
        font-size: 1.2rem;
        font-weight: 500;
        margin: 0.5rem 0;
        color: #ecf0f1;
    }
    
    .heritage-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .company-tagline {
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 1rem;
        color: #bdc3c7;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border-left: 4px solid #3498db;
    }
    
    .upload-section h3 {
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #00b894, #00a085);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    .error-message {
        background: linear-gradient(135deg, #e17055, #d63031);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    .search-container {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .search-container h3 {
        margin-bottom: 1rem;
        font-size: 1.8rem;
    }
    
    .dataframe-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .color-filter-section {
        background: linear-gradient(135deg, #fd79a8, #e84393);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .color-chip {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .match-type-info {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    
    .sidebar-content h3 {
        margin-bottom: 1rem;
        color: #ecf0f1;
    }
    
    .sidebar-content p {
        margin: 0.5rem 0;
        color: #bdc3c7;
    }
    
    .search-history {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .frame-colors-display {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        color: #2c3e50;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
        border-left: 4px solid #e17055;
    }
    
    .frame-color-item {
        background: rgba(255,255,255,0.7);
        padding: 0.5rem;
        border-radius: 8px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.9rem;
        font-weight: 600;
        border: 1px solid rgba(0,0,0,0.1);
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

def extract_frame_colors_from_yarn_description(yarn_desc: str) -> str:
    """
    Extract frame-wise colors from yarn description
    Logic: Remove entries ending with 'CN', keep only 'BB' entries, extract colors
    """
    if pd.isna(yarn_desc) or not yarn_desc:
        return ""
    
    lines = str(yarn_desc).split('\n')
    bb_entries = []
    
    # Filter out CN entries and keep only BB entries that start with WOOL
    for line in lines:
        line = line.strip()
        if line.endswith('-BB') and line.startswith('WOOL'):
            bb_entries.append(line)
    
    # Extract colors from BB entries
    frame_colors = []
    for entry in bb_entries:
        # Pattern: WOOL [COLOR]-DW-[specs]-BB
        # Extract color between "WOOL " and "-DW-"
        match = re.search(r'WOOL\s+(.+?)-DW-', entry)
        if match:
            color = match.group(1).strip()
            frame_colors.append(color)
    
    return ' ; '.join(frame_colors) if frame_colors else ""

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

def get_available_weft_heads(df: pd.DataFrame) -> List[str]:
    """Extract available weft head options from the dataframe"""
    if df is None or df.empty:
        return []
    
    weft_head_col = None
    for col in df.columns:
        if 'weft' in col.lower() and 'head' in col.lower():
            weft_head_col = col
            break
    
    if weft_head_col:
        return sorted(df[weft_head_col].dropna().astype(str).str.strip().unique())
    return []

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
                st.rerun()
    
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

# --- Multi-Filter Section (Color, Construction, No. of Frames, Weft Head) ---
st.markdown("""
<div class="color-filter-section">
    <h3>🎨 Multi-Filter Design Search</h3>
    <p style="color: #ecf0f1; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Select multiple colors, construction, number of frames, and weft head to find aviation carpet designs that match your criteria.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Filter Option Preparation ---
available_colors = []
available_constructions = []
available_frames = []
available_weft_heads = []

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
    
    # Weft Head
    available_weft_heads = get_available_weft_heads(df)

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
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

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
    selected_weft_head = st.selectbox(
        "🧵 Weft Head",
        options=["Any"] + available_weft_heads if available_weft_heads else ["Any"],
        help="Filter by weft head specifications"
    )

with col5:
    match_type = st.radio(
        "Match Type:",
        options=["All Colors (AND)", "Any Color (OR)"],
        help="All Colors: Design must contain ALL selected colors\nAny Color: Design must contain AT LEAST ONE selected color",
        key="match_type"
    )
    color_search_button = st.button("🔍 SEARCH BY FILTERS", type="secondary")

# --- Display Selected Filters ---
if selected_colors or (selected_construction and selected_construction != "Any") or (selected_frames and selected_frames != "Any") or (selected_weft_head and selected_weft_head != "Any"):
    st.markdown("**Selected Filters:**")
    chips = ""
    for color in selected_colors:
        chips += f'<span class="color-chip">{color}</span> '
    if selected_construction and selected_construction != "Any":
        chips += f'<span class="color-chip" style="background:#1e40af;">{selected_construction}</span> '
    if selected_frames and selected_frames != "Any":
        chips += f'<span class="color-chip" style="background:#8b4513;">{selected_frames} Frames</span> '
    if selected_weft_head and selected_weft_head != "Any":
        chips += f'<span class="color-chip" style="background:#059669;">{selected_weft_head}</span> '
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
            
            # Clean column names
            design_df.columns = design_df.columns.str.strip().str.title()
            yarn_df.columns = yarn_df.columns.str.strip().str.title()
            
            # Process design names
            if 'Design Name' in design_df.columns:
                design_df['Design Name'] = design_df['Design Name'].astype(str).str.strip()
                if not case_sensitive:
                    design_df['Design Name'] = design_df['Design Name'].str.upper()
            
            if 'Design Name' in yarn_df.columns:
                yarn_df['Design Name'] = yarn_df['Design Name'].astype(str).str.strip()
                if not case_sensitive:
                    yarn_df['Design Name'] = yarn_df['Design Name'].str.upper()
            
            # Add frame-wise colors column to yarn_df
            yarn_desc_col = None
            for col in yarn_df.columns:
                if 'yarn' in col.lower() and 'description' in col.lower():
                    yarn_desc_col = col
                    break
            
            if yarn_desc_col:

    # Step 1: Combine yarn descriptions for each design
              combined_yarn_desc = yarn_df.groupby('Design Name')[yarn_desc_col].apply(lambda x: '\n'.join(x.dropna().astype(str))).reset_index()
              combined_yarn_desc.columns = ['Design Name', 'Combined Yarn Description']
    
    # Step 2: Apply extraction function
              combined_yarn_desc['Frame Colors'] = combined_yarn_desc['Combined Yarn Description'].apply(extract_frame_colors_from_yarn_description)
    
    # Step 3: Merge into design_df
              design_df = design_df.merge(combined_yarn_desc[['Design Name', 'Frame Colors']], on='Design Name', how='left')
            
        st.markdown("""
        <div class="success-message">
            ✅ Aviation Carpet Database Successfully Loaded! Ready for Professional Design Search.
        </div>
        """, unsafe_allow_html=True)
        
        # Display metrics
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
        
        # Search section
        st.markdown("""
        <div class="search-container">
            <h3>🔍 Aviation Carpet Design Search</h3>
            <p style="color: #ecf0f1; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
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
        
        # Search processing
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





                        
                    
                    # Add to search history
                    if design_input_clean not in st.session_state.search_history:
                        st.session_state.search_history.append(design_input_clean)
                        if len(st.session_state.search_history) > 10:
                            st.session_state.search_history.pop(0)
                    
                    # Display results
                    if not design_matches.empty or not yarn_matches.empty:
                        st.markdown(f"""
                        <div class="success-message">
                            🎯 Found {len(design_matches)} Design Record(s) and {len(yarn_matches)} Yarn Record(s) for: "{design_input}"
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display metrics for search results
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Design Matches", len(design_matches))
                        with col2:
                            st.metric("Yarn Matches", len(yarn_matches))
                        with col3:
                            total_matches = len(design_matches) + len(yarn_matches)
                            st.metric("Total Records", total_matches)
                        with col4:
                            if not design_matches.empty:
                                unique_designs = design_matches['Design Name'].nunique()
                                st.metric("Unique Designs", unique_designs)
                        
                        # Enhanced Design Results Display
                        if not design_matches.empty:
                            st.markdown("""
                            <div class="dataframe-container">
                                <h4 style="color: #2c3e50; margin-bottom: 1rem;">📋 Design Master Results</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Add frame-wise colors to design results if yarn data is available
                            if not yarn_matches.empty and 'Frame Colors' in yarn_matches.columns:
                                design_with_colors = design_matches.copy()
                                design_with_colors['Frame Colors'] = design_with_colors['Design Name'].map(
                                    yarn_matches.drop_duplicates('Design Name').set_index('Design Name')['Frame Colors']
                                )
                                st.dataframe(design_with_colors, use_container_width=True)
                            else:
                                st.dataframe(design_matches, use_container_width=True)
                            
                            if show_export:
                                excel_data = create_export_excel(
                                    {"Design_Results": design_matches},
                                    f"WiltonWeavers_Design_Search_{design_input}"
                                )
                                st.download_button(
                                    label="📥 Download Design Results (Excel)",
                                    data=excel_data,
                                    file_name=f"WiltonWeavers_Design_Results_{design_input}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        
                        # Enhanced Yarn Results Display
                        if not yarn_matches.empty:
                            st.markdown("""
                            <div class="dataframe-container">
                                <h4 style="color: #2c3e50; margin-bottom: 1rem;">🧶 Yarn Specifications Results</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display frame-wise colors prominently
                            if 'Frame Colors' in yarn_matches.columns:
                                for _, row in yarn_matches.iterrows():
                                    if pd.notna(row['Frame Colors']) and row['Frame Colors'].strip():
                                        st.markdown(f"""
                                        <div class="frame-colors-display">
                                            <strong>🎨 Frame-wise Colors for {row['Design Name']}:</strong><br>
                                            {' → '.join([f'<span class="frame-color-item">Frame {i+1}: {color.strip()}</span>' for i, color in enumerate(row['Frame Colors'].split(';')) if color.strip()])}
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            st.dataframe(yarn_matches, use_container_width=True)
                            
                            if show_export:
                                excel_data = create_export_excel(
                                    {"Yarn_Results": yarn_matches},
                                    f"WiltonWeavers_Yarn_Search_{design_input}"
                                )
                                st.download_button(
                                    label="📥 Download Yarn Results (Excel)",
                                    data=excel_data,
                                    file_name=f"WiltonWeavers_Yarn_Results_{design_input}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        
                        # Combined Export Option
                        if show_export and (not design_matches.empty or not yarn_matches.empty):
                            export_dict = {}
                            if not design_matches.empty:
                                export_dict["Design_Master"] = design_matches
                            if not yarn_matches.empty:
                                export_dict["Yarn_Specifications"] = yarn_matches
                            
                            combined_excel = create_export_excel(export_dict, f"WiltonWeavers_Combined_{design_input}")
                            st.download_button(
                                label="📦 Download Combined Results (Excel)",
                                data=combined_excel,
                                file_name=f"WiltonWeavers_Combined_Results_{design_input}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    else:
                        st.markdown(f"""
                        <div class="error-message">
                            ❌ No Aviation Carpet Designs Found for: "{design_input}"
                            <br>Try different search terms or check spelling.
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please enter a design name to search.")

        # Multi-Filter Search Processing
        if color_search_button and st.session_state.design_df is not None:
            with st.spinner('🔍 Searching with Multiple Filters...'):
                filtered_df = st.session_state.design_df.copy()
                
                # Apply color filters
                if selected_colors:
                    color_columns = [col for col in filtered_df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
                    
                    if match_type == "All Colors (AND)":
                        # All selected colors must be present
                        for color in selected_colors:
                            color_mask = pd.Series([False] * len(filtered_df))
                            for col in color_columns:
                                color_mask |= filtered_df[col].astype(str).str.upper().str.contains(color, na=False)
                            filtered_df = filtered_df[color_mask]
                    else:
                        # At least one selected color must be present
                        color_mask = pd.Series([False] * len(filtered_df))
                        for color in selected_colors:
                            for col in color_columns:
                                color_mask |= filtered_df[col].astype(str).str.upper().str.contains(color, na=False)
                        filtered_df = filtered_df[color_mask]
                
                # Apply construction filter
                if selected_construction and selected_construction != "Any":
                    construction_col = None
                    for col in filtered_df.columns:
                        if 'construction' in col.lower():
                            construction_col = col
                            break
                    if construction_col:
                        filtered_df = filtered_df[filtered_df[construction_col].astype(str).str.contains(selected_construction, na=False, case=False)]
                
                # Apply frames filter
                if selected_frames and selected_frames != "Any":
                    frames_col = None
                    for col in filtered_df.columns:
                        if 'frame' in col.lower():
                            frames_col = col
                            break
                    if frames_col:
                        filtered_df = filtered_df[filtered_df[frames_col].astype(str).str.contains(selected_frames, na=False, case=False)]
                
                # Apply weft head filter
                if selected_weft_head and selected_weft_head != "Any":
                    weft_head_col = None
                    for col in filtered_df.columns:
                        if 'weft' in col.lower() and 'head' in col.lower():
                            weft_head_col = col
                            break
                    if weft_head_col:
                        filtered_df = filtered_df[filtered_df[weft_head_col].astype(str).str.contains(selected_weft_head, na=False, case=False)]
                
                # Display filter results
                if not filtered_df.empty:
                    st.markdown(f"""
                    <div class="success-message">
                        🎯 Found {len(filtered_df)} Design(s) Matching Your Filter Criteria
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Get corresponding yarn data for filtered designs
                    if st.session_state.yarn_df is not None and 'Design Name' in filtered_df.columns:
                        design_names = filtered_df['Design Name'].unique()
                        yarn_filtered = st.session_state.yarn_df[st.session_state.yarn_df['Design Name'].isin(design_names)]
                        
                        # Add frame-wise colors to filtered results
                        if 'Frame Colors' in yarn_filtered.columns:
                            filtered_with_colors = filtered_df.copy()
                            filtered_with_colors['Frame Colors'] = filtered_with_colors['Design Name'].map(
                                yarn_filtered.drop_duplicates('Design Name').set_index('Design Name')['Frame Colors']
                            )
                            
                            # Display frame-wise colors prominently
                            st.markdown("""
                            <div class="frame-colors-display">
                                <h4 style="color: #2c3e50; margin-bottom: 1rem;">🎨 Frame-wise Colors for Filtered Designs:</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            for _, row in filtered_with_colors.iterrows():
                                if pd.notna(row.get('Frame Colors')) and str(row.get('Frame Colors')).strip():
                                    frame_colors = str(row['Frame Colors']).split(';')
                                    frame_display = ' → '.join([f'<span class="frame-color-item">Frame {i+1}: {color.strip()}</span>' for i, color in enumerate(frame_colors) if color.strip()])
                                    st.markdown(f"""
                                    <div class="frame-colors-display">
                                        <strong>🎨 {row['Design Name']}:</strong><br>
                                        {frame_display}
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            st.dataframe(filtered_with_colors, use_container_width=True)
                        else:
                            st.dataframe(filtered_df, use_container_width=True)
                        
                        # Display corresponding yarn data
                        if not yarn_filtered.empty:
                            st.markdown("""
                            <div class="dataframe-container">
                                <h4 style="color: #2c3e50; margin-bottom: 1rem;">🧶 Corresponding Yarn Specifications</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            st.dataframe(yarn_filtered, use_container_width=True)
                    else:
                        st.dataframe(filtered_df, use_container_width=True)
                    
                    # Export filtered results
                    if show_export:
                        export_dict = {"Filtered_Designs": filtered_df}
                        if st.session_state.yarn_df is not None and 'Design Name' in filtered_df.columns:
                            design_names = filtered_df['Design Name'].unique()
                            yarn_filtered = st.session_state.yarn_df[st.session_state.yarn_df['Design Name'].isin(design_names)]
                            if not yarn_filtered.empty:
                                export_dict["Filtered_Yarn_Specs"] = yarn_filtered
                        
                        filtered_excel = create_export_excel(export_dict, "WiltonWeavers_Filtered_Results")
                        st.download_button(
                            label="📥 Download Filtered Results (Excel)",
                            data=filtered_excel,
                            file_name=f"WiltonWeavers_Filtered_Results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ No Designs Found Matching Your Filter Criteria
                        <br>Try adjusting your filter selections or using different combinations.
                    </div>
                    """, unsafe_allow_html=True)
        
        # Analytics Dashboard
        if show_analytics and st.session_state.design_df is not None:
            st.markdown("---")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
                <h3>📊 Aviation Carpet Analytics Dashboard</h3>
                <p style="color: #ecf0f1; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
                    Comprehensive analysis of your aviation carpet design database
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Color distribution analysis
                if st.session_state.design_df is not None:
                    color_columns = [col for col in st.session_state.design_df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
                    if color_columns:
                        all_colors = []
                        for col in color_columns:
                            colors_in_col = st.session_state.design_df[col].dropna().astype(str).str.split(',|;|/|\\|').explode().str.strip().str.upper()
                            all_colors.extend(colors_in_col.tolist())
                        
                        color_counts = pd.Series(all_colors).value_counts().head(10)
                        if not color_counts.empty:
                            fig = px.bar(
                                x=color_counts.index,
                                y=color_counts.values,
                                title="Top 10 Colors in Aviation Carpet Designs",
                                labels={'x': 'Colors', 'y': 'Frequency'},
                                color=color_counts.values,
                                color_continuous_scale='viridis'
                            )
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#2c3e50')
                            )
                            st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Construction type distribution
                construction_col = None
                for col in st.session_state.design_df.columns:
                    if 'construction' in col.lower():
                        construction_col = col
                        break
                
                if construction_col:
                    construction_counts = st.session_state.design_df[construction_col].value_counts()
                    if not construction_counts.empty:
                        fig = px.pie(
                            values=construction_counts.values,
                            names=construction_counts.index,
                            title="Construction Type Distribution"
                        )
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='#2c3e50')
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            # Frame-wise color analysis
            if st.session_state.yarn_df is not None and 'Frame Colors' in st.session_state.yarn_df.columns:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ffecd2, #fcb69f); color: #2c3e50; padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <h4 style="margin-bottom: 1rem;">🎨 Frame-wise Color Analysis</h4>
                </div>
                """, unsafe_allow_html=True)
                
                frame_colors_data = st.session_state.yarn_df[st.session_state.yarn_df['Frame Colors'].notna()]
                if not frame_colors_data.empty:
                    # Create frame color summary
                    frame_summary = []
                    for _, row in frame_colors_data.iterrows():
                        colors = str(row['Frame Colors']).split(';')
                        for i, color in enumerate(colors):
                            if color.strip():
                                frame_summary.append({
                                    'Design': row['Design Name'],
                                    'Frame': f'Frame {i+1}',
                                    'Color': color.strip()
                                })
                    
                    if frame_summary:
                        frame_df = pd.DataFrame(frame_summary)
                        
                        # Frame color distribution
                        col1, col2 = st.columns(2)
                        with col1:
                            frame_color_counts = frame_df['Color'].value_counts().head(10)
                            fig = px.bar(
                                x=frame_color_counts.values,
                                y=frame_color_counts.index,
                                orientation='h',
                                title="Most Used Frame Colors",
                                labels={'x': 'Usage Count', 'y': 'Colors'},
                                color=frame_color_counts.values,
                                color_continuous_scale='plasma'
                            )
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#2c3e50')
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            frame_position_counts = frame_df['Frame'].value_counts()
                            fig = px.bar(
                                x=frame_position_counts.index,
                                y=frame_position_counts.values,
                                title="Color Distribution by Frame Position",
                                labels={'x': 'Frame Position', 'y': 'Color Count'},
                                color=frame_position_counts.values,
                                color_continuous_scale='viridis'
                            )
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='#2c3e50')
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Display frame color table
                        st.markdown("**📋 Frame Color Details:**")
                        st.dataframe(frame_df, use_container_width=True)
        
        # Data Preview Section
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a8edea, #fed6e3); color: #2c3e50; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
            <h3>📊 Database Preview</h3>
            <p style="font-family: 'Inter', sans-serif; font-size: 1.1rem;">
                Preview of your aviation carpet design and yarn specification databases
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📋 Design Master Preview", "🧶 Yarn Specifications Preview"])
        
        with tab1:
            st.markdown("**Design Master Database (First 10 records):**")
            preview_design = st.session_state.design_df.head(10)
            st.dataframe(preview_design, use_container_width=True)
        
        with tab2:
            st.markdown("**Yarn Specifications Database (First 10 records):**")
            preview_yarn = st.session_state.yarn_df.head(10)
            st.dataframe(preview_yarn, use_container_width=True)
            
            # Display frame colors if available
            if 'Frame Colors' in preview_yarn.columns:
                st.markdown("**🎨 Frame-wise Colors (First 10 records):**")
                frame_colors_preview = preview_yarn[['Design Name', 'Frame Colors']].dropna()
                if not frame_colors_preview.empty:
                    for _, row in frame_colors_preview.iterrows():
                        if str(row['Frame Colors']).strip():
                            frame_colors = str(row['Frame Colors']).split(';')
                            frame_display = ' → '.join([f'<span class="frame-color-item">Frame {i+1}: {color.strip()}</span>' for i, color in enumerate(frame_colors) if color.strip()])
                            st.markdown(f"""
                            <div class="frame-colors-display">
                                <strong>🎨 {row['Design Name']}:</strong><br>
                                {frame_display}
                            </div>
                            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error processing files: {str(e)}
            <br>Please check your Excel file format and try again.
        </div>
        """, unsafe_allow_html=True)
        st.error(f"Detailed error: {str(e)}")

elif design_file is not None or yarn_file is not None:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fdcb6e, #e17055); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center;">
        <h4 style="margin-bottom: 0.5rem;">⚠️ Both Files Required</h4>
        <p style="margin: 0; font-size: 1rem;">
            Please upload both Design Master and Yarn Specifications Excel files to proceed with the aviation carpet search.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #74b9ff, #0984e3); color: white; padding: 3rem; border-radius: 20px; margin: 2rem 0; text-align: center;">
        <h3 style="margin-bottom: 1rem;">🚀 Welcome to Wilton Weavers BOM Search Platform</h3>
        <p style="font-size: 1.2rem; margin-bottom: 2rem; color: #ecf0f1;">
            Upload your aviation carpet design master and yarn specification files to begin your professional search experience.
        </p>
        <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
            <h4 style="color: #ecf0f1; margin-bottom: 1rem;">🎯 Platform Features</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="margin: 0.5rem; color: #ecf0f1;">
                    <strong>🔍 Advanced Search</strong><br>
                    <small>Multi-filter design search</small>
                </div>
                <div style="margin: 0.5rem; color: #ecf0f1;">
                    <strong>🎨 Color Analysis</strong><br>
                    <small>Frame-wise color extraction</small>
                </div>
                <div style="margin: 0.5rem; color: #ecf0f1;">
                    <strong>📊 Analytics</strong><br>
                    <small>Comprehensive reporting</small>
                </div>
                <div style="margin: 0.5rem; color: #ecf0f1;">
                    <strong>📥 Export</strong><br>
                    <small>Professional Excel reports</small>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #2c3e50, #34495e); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
    <h4 style="margin-bottom: 1rem;">✈️ Wilton Weavers - Aviation Carpet Specialists</h4>
    <p style="margin: 0.5rem 0; color: #bdc3c7;">
        <strong>Kerala, India</strong> • Est. 1982 • 40+ Years of Excellence in Fine Wool Broadloom
    </p>
    <p style="margin: 0.5rem 0; color: #bdc3c7;">
        Manufacturers of Premium Aviation Carpets • Quality Assured • Innovation Driven
    </p>
    <div style="margin-top: 1rem;">
        <small style="color: #95a5a6;">
            © 2024 Wilton Weavers. All rights reserved. | 
            <a href="https://www.wilton.in" target="_blank" style="color: #74b9ff; text-decoration: none;">www.wilton.in</a>
        </small>
    </div>
</div>
""", unsafe_allow_html=True)




         
                     
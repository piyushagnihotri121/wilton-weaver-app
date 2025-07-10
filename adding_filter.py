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
/* Main styling for the application */
.main-header {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.main-header h1 {
    font-size: 3rem;
    margin: 0;
    font-weight: 700;
    letter-spacing: 2px;
}

.company-location {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-top: 0.5rem;
    font-weight: 500;
}

.heritage-badge {
    background: rgba(255,255,255,0.2);
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    margin-top: 1rem;
    font-size: 0.9rem;
}

.company-tagline {
    font-size: 1.1rem;
    margin-top: 1rem;
    opacity: 0.9;
    line-height: 1.6;
}

.upload-section {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    border-left: 4px solid #3498db;
}

.upload-section h3 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

.color-filter-section {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin: 2rem 0;
    text-align: center;
}

.color-filter-section h3 {
    margin-bottom: 1rem;
    font-size: 2rem;
}

.color-chip {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    margin: 0.25rem;
    font-size: 0.9rem;
    font-weight: 500;
}

.match-type-info {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: center;
}

.search-container {
    background: linear-gradient(135deg, #2c3e50, #34495e);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin: 2rem 0;
    text-align: center;
}

.search-container h3 {
    margin-bottom: 1rem;
    font-size: 2rem;
}

.success-message {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    text-align: center;
    font-weight: 500;
}

.error-message {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    text-align: center;
    font-weight: 500;
}

.metric-card {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.metric-number {
    font-size: 2.5rem;
    font-weight: bold;
    display: block;
}

.metric-label {
    font-size: 1rem;
    opacity: 0.9;
    margin-top: 0.5rem;
}

.dataframe-container {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 1rem 0;
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
}

.search-history {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.debug-info {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
    font-family: monospace;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# --- Utility Functions ---
def clean_design_name(name: str) -> str:
    if pd.isna(name):
        return ""
    return str(name).strip().upper()

def extract_colors_from_text(text: str) -> List[str]:
    """Extract and clean colors from text with multiple separators"""
    if pd.isna(text) or not text:
        return []
    
    # Convert to string and clean
    text = str(text).strip()
    if not text or text.upper() in ['NAN', 'NA', 'NULL', '']:
        return []
    
    # Define separators
    separators = [',', ';', '/', '|', '+', '&', '-', '\\', '\n', '\t']
    
    # Split by separators
    colors = [text]
    for sep in separators:
        new_colors = []
        for color in colors:
            if sep in color:
                new_colors.extend(color.split(sep))
            else:
                new_colors.append(color)
        colors = new_colors
    
    # Clean and filter colors
    cleaned_colors = []
    for color in colors:
        color = color.strip().upper()
        if color and color not in ['NAN', 'NA', 'NULL', ''] and len(color) > 1:
            cleaned_colors.append(color)
    
    return list(set(cleaned_colors))  # Remove duplicates

def get_available_colors(df: pd.DataFrame) -> List[str]:
    """Get all available colors from the dataframe"""
    if df is None or df.empty:
        return []
    
    color_columns = [col for col in df.columns if 
                    any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye', 'hue'])]
    
    all_colors = set()
    for col in color_columns:
        for value in df[col].dropna():
            colors = extract_colors_from_text(str(value))
            all_colors.update(colors)
    
    # If no colors found, use default aviation carpet colors
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

def check_row_colors(row, color_columns, selected_colors, match_type):
    """Check if a row matches the color criteria"""
    row_colors = set()
    
    # Extract all colors from the row
    for col in color_columns:
        if pd.notna(row[col]):
            colors = extract_colors_from_text(str(row[col]))
            row_colors.update(colors)
    
    # Apply matching logic
    if match_type == "All Colors (AND)":
        # All selected colors must be present
        return all(color in row_colors for color in selected_colors)
    else:  # "Any Color (OR)"
        # At least one selected color must be present
        return any(color in row_colors for color in selected_colors)

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
    show_debug = st.checkbox("🔧 Debug Mode", value=False, help="Show debug information for troubleshooting")
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

# --- Enhanced Multi-Filter Section ---
st.markdown("""
<div class="color-filter-section">
    <h3>🎨 Enhanced Multi-Filter Design Search</h3>
    <p style="color: #ecf0f1; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Select multiple colors, construction, number of frames, and weft head specifications to find aviation carpet designs that match your criteria.
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
        for value in df[col].dropna():
            colors = extract_colors_from_text(str(value))
            available_colors.extend(colors)
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
    weft_head_col = None
    for col in df.columns:
        if 'weft' in col.lower() and 'head' in col.lower():
            weft_head_col = col
            break
    if weft_head_col:
        available_weft_heads = sorted(df[weft_head_col].dropna().astype(str).str.strip().unique())

# Default colors if none found
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

# --- Enhanced Filter UI ---
# First row - Colors and Match Type
col1, col2 = st.columns([3, 1])
with col1:
    selected_colors = st.multiselect(
        "🎨 Select Colors (Choose multiple colors used in carpet design)",
        options=available_colors,
        help="Select one or more colors that should be present in the carpet design. The system will find designs using these color combinations.",
        key="color_multiselect"
    )
with col2:
    match_type = st.radio(
        "Match Type:",
        options=["All Colors (AND)", "Any Color (OR)"],
        help="All Colors: Design must contain ALL selected colors\nAny Color: Design must contain AT LEAST ONE selected color",
        key="match_type"
    )

# Second row - Construction, Frames, Weft Head, and Search button
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    selected_construction = st.selectbox(
        "🏗️ Construction",
        options=["Any"] + available_constructions if available_constructions else ["Any"],
        help="Filter by construction type (e.g., WILTON, AXMINSTER, TUFTED, etc.)"
    )
with col2:
    selected_frames = st.selectbox(
        "🖼️ No. of Frames",
        options=["Any"] + available_frames if available_frames else ["Any"],
        help="Filter by number of frames (if available in your data)"
    )
with col3:
    selected_weft_head = st.selectbox(
        "🧵 Weft Head",
        options=["Any"] + available_weft_heads if available_weft_heads else ["Any"],
        help="Filter by weft head specifications"
    )
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    color_search_button = st.button("🔍 SEARCH BY FILTERS", type="primary")

# --- Display Selected Filters ---
if (selected_colors or 
    (selected_construction and selected_construction != "Any") or 
    (selected_frames and selected_frames != "Any") or 
    (selected_weft_head and selected_weft_head != "Any")):
    
    st.markdown("**Selected Filters:**")
    chips = ""
    
    # Color chips
    for color in selected_colors:
        chips += f'<span class="color-chip">{color}</span> '
    
    # Construction chip
    if selected_construction and selected_construction != "Any":
        chips += f'<span class="color-chip" style="background:#1e40af;">{selected_construction}</span> '
    
    # Frames chip
    if selected_frames and selected_frames != "Any":
        chips += f'<span class="color-chip" style="background:#8b4513;">{selected_frames} Frames</span> '
    
    # Weft Head chip
    if selected_weft_head and selected_weft_head != "Any":
        chips += f'<span class="color-chip" style="background:#7c3aed;">{selected_weft_head}</span> '
    
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
            
            # Clean design names
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

                        st.dataframe(merged, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if show_export:
                            excel_data = create_export_excel(
                                {"Complete_Specification": merged},
                                f"Aviation_Carpet_{design_input_clean}"
                            )
                            st.download_button(
                                label="📥 Download Complete Specification",
                                data=excel_data,
                                file_name=f"Aviation_Carpet_Specification_{design_input_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    
                    with tab2:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🎨 Design Master Details")
                        st.dataframe(design_matches, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if show_export:
                            excel_data = create_export_excel(
                                {"Design_Details": design_matches},
                                f"Design_Details_{design_input_clean}"
                            )
                            st.download_button(
                                label="📥 Download Design Details",
                                data=excel_data,
                                file_name=f"Design_Details_{design_input_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    
                    with tab3:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🧶 Yarn & Material Specifications")
                        st.dataframe(yarn_matches, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if show_export:
                            excel_data = create_export_excel(
                                {"Yarn_Specifications": yarn_matches},
                                f"Yarn_Specifications_{design_input_clean}"
                            )
                            st.download_button(
                                label="📥 Download Yarn Specifications",
                                data=excel_data,
                                file_name=f"Yarn_Specifications_{design_input_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    
                    with tab4:
                        if show_analytics:
                            st.subheader("📈 Quality Analytics Dashboard")
                            
                            # Quality metrics
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if 'Quality Grade' in merged.columns:
                                    quality_counts = merged['Quality Grade'].value_counts()
                                    fig = px.pie(
                                        values=quality_counts.values,
                                        names=quality_counts.index,
                                        title="Quality Grade Distribution"
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                if 'Construction' in merged.columns:
                                    construction_counts = merged['Construction'].value_counts()
                                    fig = px.bar(
                                        x=construction_counts.index,
                                        y=construction_counts.values,
                                        title="Construction Type Analysis"
                                    )
                                    st.plotly_chart(fig, use_container_width=True)
                            
                            with col3:
                                color_columns = [col for col in merged.columns if any(word in col.lower() for word in ['color', 'colour'])]
                                if color_columns:
                                    all_colors = []
                                    for col in color_columns:
                                        for value in merged[col].dropna():
                                            colors = extract_colors_from_text(str(value))
                                            all_colors.extend(colors)
                                    
                                    if all_colors:
                                        color_counts = pd.Series(all_colors).value_counts()
                                        fig = px.bar(
                                            x=color_counts.values,
                                            y=color_counts.index,
                                            orientation='h',
                                            title="Color Usage Analysis"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                
                elif not design_matches.empty:
                    st.markdown("""
                    <div class="error-message">
                        ⚠️ Design Found but No Matching Yarn Specifications. Please check your yarn database.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.subheader("🎨 Available Design Details")
                    st.dataframe(design_matches, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                elif not yarn_matches.empty:
                    st.markdown("""
                    <div class="error-message">
                        ⚠️ Yarn Specifications Found but No Matching Design Details. Please check your design database.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.subheader("🧶 Available Yarn Specifications")
                    st.dataframe(yarn_matches, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ No matches found for your search criteria. Please try different keywords or check your data.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add search suggestions
                    if 'Design Name' in design_df.columns:
                        st.subheader("💡 Search Suggestions")
                        unique_designs = design_df['Design Name'].dropna().unique()[:10]
                        cols = st.columns(2)
                        for i, design in enumerate(unique_designs):
                            with cols[i % 2]:
                                if st.button(f"🔍 {design}", key=f"suggest_{i}"):
                                    st.session_state.search_input = design
                                    st.rerun()
                
                # Add to search history
                if design_input_clean and design_input_clean not in st.session_state.search_history:
                    st.session_state.search_history.append(design_input_clean)
                    if len(st.session_state.search_history) > 10:
                        st.session_state.search_history.pop(0)
        
        # Enhanced Color Filter Search - FIXED VERSION
        if color_search_button and (selected_colors or 
                                   (selected_construction and selected_construction != "Any") or 
                                   (selected_frames and selected_frames != "Any") or 
                                   (selected_weft_head and selected_weft_head != "Any")):
            
            with st.spinner('🔍 Searching with Enhanced Filters...'):
                filtered_df = design_df.copy()
                
                # Apply color filter
                if selected_colors:
                    color_columns = [col for col in filtered_df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
                    
                    if color_columns:
                        color_mask = pd.Series([False] * len(filtered_df))
                        
                        for idx, row in filtered_df.iterrows():
                            row_colors = set()
                            # Extract all colors from the row
                            for col in color_columns:
                                if pd.notna(row[col]):
                                    colors = extract_colors_from_text(str(row[col]))
                                    row_colors.update(colors)
                            
                            # Apply matching logic
                            if match_type == "All Colors (AND)":
                                # All selected colors must be present
                                if row_colors and all(color in row_colors for color in selected_colors):
                                    color_mask.iloc[idx] = True
                            else:  # "Any Color (OR)"
                                # At least one selected color must be present
                                if row_colors and any(color in row_colors for color in selected_colors):
                                    color_mask.iloc[idx] = True
                        
                        filtered_df = filtered_df[color_mask]
                
                # Apply construction filter
                if selected_construction and selected_construction != "Any":
                    construction_col = None
                    for col in filtered_df.columns:
                        if 'construction' in col.lower():
                            construction_col = col
                            break
                    
                    if construction_col:
                        filtered_df = filtered_df[filtered_df[construction_col].astype(str).str.strip() == selected_construction]
                
                # Apply frames filter
                if selected_frames and selected_frames != "Any":
                    frames_col = None
                    for col in filtered_df.columns:
                        if 'frame' in col.lower():
                            frames_col = col
                            break
                    
                    if frames_col:
                        filtered_df = filtered_df[filtered_df[frames_col].astype(str).str.strip() == selected_frames]
                
                # Apply weft head filter
                if selected_weft_head and selected_weft_head != "Any":
                    weft_head_col = None
                    for col in filtered_df.columns:
                        if 'weft' in col.lower() and 'head' in col.lower():
                            weft_head_col = col
                            break
                    
                    if weft_head_col:
                        filtered_df = filtered_df[filtered_df[weft_head_col].astype(str).str.strip() == selected_weft_head]
                
                # Display results
                if not filtered_df.empty:
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Found {len(filtered_df)} designs matching your enhanced filter criteria!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display metrics
                    display_metrics_cards({
                        "Total Matches": len(filtered_df),
                        "Unique Designs": filtered_df['Design Name'].nunique() if 'Design Name' in filtered_df.columns else 0,
                        "Color Matches": len(selected_colors) if selected_colors else 0,
                        "Filter Applied": 1 if (selected_construction != "Any" or selected_frames != "Any" or selected_weft_head != "Any") else 0
                    })
                    
                    # Show filtered results
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.subheader("🎯 Filtered Aviation Carpet Designs")
                    st.dataframe(filtered_df, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Export options
                    if show_export:
                        excel_data = create_export_excel(
                            {"Filtered_Designs": filtered_df},
                            "Enhanced_Filter_Results"
                        )
                        st.download_button(
                            label="📥 Download Filtered Results",
                            data=excel_data,
                            file_name=f"Enhanced_Filter_Results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    # Analytics for filtered results
                    if show_analytics:
                        st.subheader("📊 Filtered Results Analytics")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Color distribution in filtered results
                            if selected_colors:
                                color_columns = [col for col in filtered_df.columns if any(word in col.lower() for word in ['color', 'colour'])]
                                if color_columns:
                                    all_colors = []
                                    for col in color_columns:
                                        for value in filtered_df[col].dropna():
                                            colors = extract_colors_from_text(str(value))
                                            all_colors.extend(colors)
                                    
                                    if all_colors:
                                        color_counts = pd.Series(all_colors).value_counts()
                                        fig = px.bar(
                                            x=color_counts.index,
                                            y=color_counts.values,
                                            title="Color Distribution in Filtered Results"
                                        )
                                        st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Construction type distribution if available
                            construction_col = None
                            for col in filtered_df.columns:
                                if 'construction' in col.lower():
                                    construction_col = col
                                    break
                            
                            if construction_col:
                                construction_counts = filtered_df[construction_col].value_counts()
                                fig = px.pie(
                                    values=construction_counts.values,
                                    names=construction_counts.index,
                                    title="Construction Type Distribution"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ No designs found matching your enhanced filter criteria. Please try different combinations.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Debug information
                    if show_debug:
                        st.markdown("""
                        <div class="debug-info">
                            <h4>🔧 Debug Information</h4>
                            <p><strong>Selected Colors:</strong> {}</p>
                            <p><strong>Match Type:</strong> {}</p>
                            <p><strong>Construction:</strong> {}</p>
                            <p><strong>Frames:</strong> {}</p>
                            <p><strong>Weft Head:</strong> {}</p>
                            <p><strong>Total Records Before Filter:</strong> {}</p>
                            <p><strong>Records After Filter:</strong> {}</p>
                        </div>
                        """.format(
                            selected_colors,
                            match_type,
                            selected_construction,
                            selected_frames,
                            selected_weft_head,
                            len(design_df),
                            len(filtered_df)
                        ), unsafe_allow_html=True)
                        
                        # Show available values for debugging
                        st.subheader("🔍 Available Values in Database")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if available_colors:
                                st.write("**Available Colors:**")
                                st.write(available_colors[:20])  # Show first 20
                        
                        with col2:
                            if available_constructions:
                                st.write("**Available Constructions:**")
                                st.write(available_constructions)
        
        # Display sample data if no search performed
        if not design_input and not color_search_button:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f39c12, #e67e22); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center;">
                <h4>👀 Database Preview</h4>
                <p>Here's a preview of your aviation carpet database. Use the search above to find specific designs.</p>
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🎨 Design Preview", "🧶 Yarn Preview"])
            
            with tab1:
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.subheader("🎨 Design Master Database Preview")
                st.dataframe(design_df.head(10), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.info(f"📊 Showing first 10 records out of {len(design_df)} total design records")
            
            with tab2:
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.subheader("🧶 Yarn Database Preview")
                st.dataframe(yarn_df.head(10), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.info(f"📊 Showing first 10 records out of {len(yarn_df)} total yarn records")
        
        # Debug information
        if show_debug:
            st.markdown("---")
            st.subheader("🔧 Debug Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Design DataFrame Info:**")
                st.write(f"Shape: {design_df.shape}")
                st.write(f"Columns: {list(design_df.columns)}")
                
                if 'Design Name' in design_df.columns:
                    st.write(f"Unique Design Names: {design_df['Design Name'].nunique()}")
                    st.write("Sample Design Names:")
                    st.write(design_df['Design Name'].dropna().head().tolist())
            
            with col2:
                st.markdown("**Yarn DataFrame Info:**")
                st.write(f"Shape: {yarn_df.shape}")
                st.write(f"Columns: {list(yarn_df.columns)}")
                
                if 'Design Name' in yarn_df.columns:
                    st.write(f"Unique Design Names: {yarn_df['Design Name'].nunique()}")
                    st.write("Sample Design Names:")
                    st.write(yarn_df['Design Name'].dropna().head().tolist())
    
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error processing files: {str(e)}
        </div>
        """, unsafe_allow_html=True)
        
        if show_debug:
            st.exception(e)

else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0; text-align: center;">
        <h3>🚀 Welcome to Wilton Weavers BOM Search Platform</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">
            Your comprehensive solution for aviation carpet design management and yarn specification analysis.
        </p>
        <p style="font-size: 1rem; opacity: 0.9;">
            📋 Please upload both Design Master Database and Yarn Specifications files to begin your professional search experience.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #ffffff; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0; text-align: center;">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">🎨 Multi-Color Search</h4>
            <p style="color: #7f8c8d; font-size: 0.9rem;">
                Advanced color filtering with AND/OR logic for precise aviation carpet design matching.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #ffffff; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0; text-align: center;">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">🏗️ Construction Filter</h4>
            <p style="color: #7f8c8d; font-size: 0.9rem;">
                Filter by construction type, frames, and weft head specifications for technical accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #ffffff; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0; text-align: center;">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">📊 Analytics Dashboard</h4>
            <p style="color: #7f8c8d; font-size: 0.9rem;">
                Comprehensive analytics and export capabilities for professional reporting.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #2c3e50, #34495e); color: white; border-radius: 15px; margin-top: 2rem;">
    <h3 style="margin-bottom: 1rem;">✈️ WILTON WEAVERS</h3>
    <p style="margin: 0.5rem 0; font-size: 1rem;">
        <strong>Kerala, India</strong> | Est. 1982 | Aviation Carpets & Fine Wool Broadloom Specialists
    </p>
    <p style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.8;">
        40+ Years of Excellence in Quality Floor Coverings | Innovators Par Excellence
    </p>
    <p style="margin: 1rem 0; font-size: 0.9rem;">
        🌐 <a href="https://www.wilton.in" target="_blank" style="color: #3498db;">www.wilton.in</a> | 
        📧 <a href="mailto:info@wilton.in" style="color: #3498db;">info@wilton.in</a>
    </p>
    <p style="margin: 0; font-size: 0.8rem; opacity: 0.7;">
        © 2024 Wilton Weavers. All rights reserved. | BOM Search Platform v2.0
    </p>
</div>
""", unsafe_allow_html=True)

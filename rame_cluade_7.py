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
from collections import Counter

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
    .main-header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 2rem 3rem;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        letter-spacing: 2px;
    }
    .company-location {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    .heritage-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .company-tagline {
        font-size: 1.1rem;
        line-height: 1.6;
        opacity: 0.95;
        max-width: 600px;
        margin: 0 auto;
    }
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
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
        font-size: 1.8rem;
    }
    .color-chip {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
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
        font-size: 1.8rem;
    }
    .success-message {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 500;
    }
    .error-message {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 500;
    }
    .metric-card {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        display: block;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .dataframe-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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

def extract_color_from_yarn(yarn_desc: str) -> str:
    """Extract just the color part from a yarn description"""
    if pd.isna(yarn_desc):
        return ""
    
    # Remove suffixes like -BB, -CN, etc.
    yarn_desc = re.sub(r'(-BB|-CN|-BM|-SP|-PL|-XX|-ZZ)$', '', yarn_desc)
    
    # Extract the color part (after WOOL and before the next hyphen)
    match = re.search(r'WOOL\s+([^-]+)', yarn_desc)
    if match:
        return match.group(1).strip()
    return ""

def process_yarn_description(desc: str) -> str:
    """Process yarn description according to business rules"""
    if pd.isna(desc):
        return ""
    
    desc = str(desc).upper()
    yarns = []
    
    # Split by common delimiters
    parts = re.split(r'[,;/|&+]', desc)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Only process yarns that start with 'WOOL'
        if not part.startswith('WOOL'):
            continue
            
        # Extract base yarn (without suffix)
        base_yarn = re.sub(r'(-BB|-CN|-BM|-SP|-PL|-XX|-ZZ)$', '', part)
        
        # Check if we already have this yarn (prefer BB over others)
        existing = next((y for y in yarns if re.sub(r'(-BB|-CN|-BM|-SP|-PL|-XX|-ZZ)$', '', y) == base_yarn), None)
        
        if existing:
            # Prefer BB suffix if available
            if part.endswith('-BB') and not existing.endswith('-BB'):
                yarns.remove(existing)
                yarns.append(part)
        else:
            yarns.append(part)
    
    return " - ".join(yarns)

def optimize_color_sequence(color_sequence: str) -> str:
    """Optimize color sequence by reducing even-count colors by half"""
    if not color_sequence:
        return ""
    
    colors = color_sequence.split(" - ")
    if not colors:
        return ""
    
    # Count occurrences of each color
    color_counts = Counter(colors)
    
    # Build optimized sequence
    optimized_colors = []
    for color in colors:
        if color not in [c for c in optimized_colors]:  # If we haven't processed this color yet
            count = color_counts[color]
            if count % 2 == 0:  # Even count - divide by 2
                times_to_add = count // 2
            else:  # Odd count - keep as is
                times_to_add = count
            
            # Add the color the calculated number of times
            for _ in range(times_to_add):
                optimized_colors.append(color)
    
    return " - ".join(optimized_colors)

def deduplicate_consecutive_colors(color_sequence: str) -> str:
    """Remove consecutive duplicate colors from the sequence"""
    if not color_sequence:
        return ""
    
    colors = color_sequence.split(" - ")
    deduplicated = []
    prev_color = None
    
    for color in colors:
        if color != prev_color:
            deduplicated.append(color)
            prev_color = color
    
    return " - ".join(deduplicated)

def get_frame_wise_colors(design_df: pd.DataFrame, yarn_df: pd.DataFrame) -> pd.DataFrame:
    """Create frame-wise color mapping from design and yarn data"""
    if design_df is None or yarn_df is None:
        return pd.DataFrame()
    
    # Find yarn description column
    yarn_desc_col = None
    for col in yarn_df.columns:
        if 'description' in col.lower() or 'yarn' in col.lower():
            yarn_desc_col = col
            break
    
    if not yarn_desc_col:
        return pd.DataFrame()
    
    # Process each yarn description to get only WOOL yarns with BB preference
    yarn_df['Processed_Yarn'] = yarn_df[yarn_desc_col].apply(process_yarn_description)
    
    # Extract just the color parts from the processed yarn descriptions
    yarn_df['Extracted_Colors'] = yarn_df['Processed_Yarn'].apply(lambda x: " - ".join(
        [extract_color_from_yarn(y) for y in x.split(" - ") if extract_color_from_yarn(y)]
    ))
    
    # First deduplicate consecutive colors, then optimize the sequence
    yarn_df['Deduplicated_Colors'] = yarn_df['Extracted_Colors'].apply(deduplicate_consecutive_colors)
    yarn_df['Frame-wise Color'] = yarn_df['Deduplicated_Colors'].apply(optimize_color_sequence)
    
    # Merge with design data
    if 'Design Name' not in design_df.columns or 'Design Name' not in yarn_df.columns:
        return pd.DataFrame()
    
    # Group by design name and combine the frame-wise colors
    frame_colors = yarn_df.groupby('Design Name')['Frame-wise Color'].apply(
        lambda x: " - ".join([y for y in x if pd.notna(y) and y])
    ).reset_index()
    
    frame_colors.columns = ['Design Name', 'Frame-wise Color']
    
    return frame_colors

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

# --- Multi-Filter Section (Color, Construction, No. of Frames, Weft Heads) ---
st.markdown("""
<div class="color-filter-section">
    <h3>🎨 Multi-Filter Design Search</h3>
    <p style="color: #f8f9fa; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Select multiple colors, construction, number of frames, and weft heads to find aviation carpet designs that match your criteria.
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
    # Weft Heads
    weft_col = None
    for col in df.columns:
        if 'weft' in col.lower() and 'head' in col.lower():
            weft_col = col
            break
    if weft_col:
        available_weft_heads = sorted(df[weft_col].dropna().astype(str).str.strip().unique())

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
    selected_weft = st.selectbox(
        "🧵 Weft Heads",
        options=["Any"] + available_weft_heads if available_weft_heads else ["Any"],
        help="Filter by number of weft heads (if available in your data)"
    )

# Match type and search button
col1, col2 = st.columns([3, 1])
with col1:
    match_type = st.radio(
        "Match Type:",
        options=["All Colors (AND)", "Any Color (OR)"],
        help="All Colors: Design must contain ALL selected colors\nAny Color: Design must contain AT LEAST ONE selected color",
        key="match_type"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    color_search_button = st.button("🔍 SEARCH BY FILTERS", type="secondary")

# --- Display Selected Filters ---
if selected_colors or (selected_construction and selected_construction != "Any") or (selected_frames and selected_frames != "Any") or (selected_weft and selected_weft != "Any"):
    st.markdown("**Selected Filters:**")
    chips = ""
    for color in selected_colors:
        chips += f'<span class="color-chip">{color}</span> '
    if selected_construction and selected_construction != "Any":
        chips += f'<span class="color-chip" style="background:#1e40af;">{selected_construction}</span> '
    if selected_frames and selected_frames != "Any":
        chips += f'<span class="color-chip" style="background:#8b4513;">{selected_frames} Frames</span> '
    if selected_weft and selected_weft != "Any":
        chips += f'<span class="color-chip" style="background:#6b7280;">{selected_weft} Weft Heads</span> '
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
            
            # Generate frame-wise colors mapping
            frame_colors_df = get_frame_wise_colors(design_df, yarn_df)
            if not frame_colors_df.empty:
                design_df = pd.merge(design_df, frame_colors_df, on='Design Name', how='left')
            
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
            unique_designs = design_df['Design Name'].nunique

            () if 'Design Name' in design_df.columns else 0
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-number">{unique_designs}</span>
                <div class="metric-label">Unique Designs</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display sample data
        if st.checkbox("📊 Preview Data Structure", value=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Design Master Sample:**")
                st.dataframe(design_df.head(3), use_container_width=True)
            with col2:
                st.markdown("**Yarn Specifications Sample:**")
                st.dataframe(yarn_df.head(3), use_container_width=True)
                
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error processing files: {str(e)}
        </div>
        """, unsafe_allow_html=True)

# --- Multi-Filter Color Search ---
if color_search_button and st.session_state.design_df is not None:
    df = st.session_state.design_df.copy()
    
    # Initialize results
    results = pd.DataFrame()
    
    # Apply filters
    if selected_colors:
        # Get all color columns
        color_columns = [col for col in df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye', 'frame-wise'])]
        
        matching_rows = []
        for idx, row in df.iterrows():
            row_colors = set()
            for col in color_columns:
                if pd.notna(row[col]):
                    colors_in_cell = extract_colors_from_text(str(row[col]))
                    row_colors.update(colors_in_cell)
            
            if match_type == "All Colors (AND)":
                if all(color in row_colors for color in selected_colors):
                    matching_rows.append(idx)
            else:  # Any Color (OR)
                if any(color in row_colors for color in selected_colors):
                    matching_rows.append(idx)
        
        results = df.iloc[matching_rows]
    else:
        results = df
    
    # Apply construction filter
    if selected_construction and selected_construction != "Any":
        construction_col = None
        for col in results.columns:
            if 'construction' in col.lower():
                construction_col = col
                break
        if construction_col:
            results = results[results[construction_col].astype(str).str.contains(selected_construction, case=False, na=False)]
    
    # Apply frames filter
    if selected_frames and selected_frames != "Any":
        frames_col = None
        for col in results.columns:
            if 'frame' in col.lower():
                frames_col = col
                break
        if frames_col:
            results = results[results[frames_col].astype(str).str.contains(selected_frames, case=False, na=False)]
    
    # Apply weft heads filter
    if selected_weft and selected_weft != "Any":
        weft_col = None
        for col in results.columns:
            if 'weft' in col.lower() and 'head' in col.lower():
                weft_col = col
                break
        if weft_col:
            results = results[results[weft_col].astype(str).str.contains(selected_weft, case=False, na=False)]
    
    # Display results
    if not results.empty:
        st.markdown(f"""
        <div class="success-message">
            ✅ Found {len(results)} aviation carpet designs matching your criteria!
        </div>
        """, unsafe_allow_html=True)
        
        # Display metrics
        display_metrics_cards({
            "Total Matches": len(results),
            "Unique Designs": results['Design Name'].nunique() if 'Design Name' in results.columns else 0,
            "Color Combinations": len(selected_colors) if selected_colors else 0,
            "Filter Criteria": sum([1 for f in [selected_construction, selected_frames, selected_weft] if f != "Any"])
        })
        
        # Display results table
        st.markdown("### 🎯 Matching Aviation Carpet Designs")
        st.dataframe(results, use_container_width=True, height=400)
        
        # Export options
        if show_export:
            st.markdown("### 📥 Export Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Export to Excel"):
                    excel_data = create_export_excel(
                        {"Color_Search_Results": results},
                        "aviation_carpet_search"
                    )
                    st.download_button(
                        label="📥 Download Excel File",
                        data=excel_data,
                        file_name=f"aviation_carpet_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            with col2:
                if st.button("📋 Export to CSV"):
                    csv_data = results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV File",
                        data=csv_data,
                        file_name=f"aviation_carpet_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            with col3:
                if st.button("🔗 Generate Report"):
                    st.markdown(f"""
                    **Search Summary Report**
                    - **Search Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    - **Total Results:** {len(results)}
                    - **Colors Selected:** {', '.join(selected_colors) if selected_colors else 'None'}
                    - **Construction:** {selected_construction if selected_construction != 'Any' else 'Any'}
                    - **Frames:** {selected_frames if selected_frames != 'Any' else 'Any'}
                    - **Weft Heads:** {selected_weft if selected_weft != 'Any' else 'Any'}
                    - **Match Type:** {match_type}
                    """)
        
        # Add to search history
        search_term = f"Colors: {', '.join(selected_colors[:3])}" if selected_colors else "Multi-Filter Search"
        if search_term not in st.session_state.search_history:
            st.session_state.search_history.append(search_term)
    
    else:
        st.markdown("""
        <div class="error-message">
            ❌ No aviation carpet designs found matching your criteria. Try adjusting your filters.
        </div>
        """, unsafe_allow_html=True)
        
        # Suggestions
        st.markdown("### 💡 Search Suggestions:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Try These Tips:**
            - Use 'Any Color (OR)' instead of 'All Colors (AND)'
            - Select fewer colors
            - Check if color names match your data
            - Try different construction types
            """)
        with col2:
            st.markdown("""
            **Common Color Names:**
            - NAVY BLUE, ROYAL BLUE, DEEP BLUE
            - BURGUNDY, WINE RED, CRIMSON
            - FOREST GREEN, EMERALD GREEN
            - CHARCOAL GREY, SILVER GREY
            """)

# --- Design Name Search Section ---
st.markdown("""
<div class="search-container">
    <h3>🔍 Design Name Search</h3>
    <p style="color: #ecf0f1; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Enter design name or pattern to search aviation carpet specifications
    </p>
</div>
""", unsafe_allow_html=True)

# Search input
search_input = st.text_input(
    "Enter Design Name or Pattern:",
    placeholder="e.g., WW-001, ROYAL BLUE, AVIATION SERIES, etc.",
    help="Search for specific design names, patterns, or any text that might appear in your design database",
    key="search_input"
)

# Search options
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    search_type = st.radio(
        "Search Type:",
        ["Contains (Partial)", "Exact Match", "Starts With", "Ends With"],
        help="Choose how to match your search term with design names"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🔍 SEARCH DESIGNS", type="primary")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    clear_button = st.button("🗑️ Clear Search", type="secondary")

if clear_button:
    st.session_state.search_input = ""
    st.rerun()

# --- Search Execution ---
if search_button and search_input and st.session_state.design_df is not None:
    design_df = st.session_state.design_df
    yarn_df = st.session_state.yarn_df
    
    # Add to search history
    if search_input not in st.session_state.search_history:
        st.session_state.search_history.append(search_input)
    
    # Search in design_df
    search_term = search_input if case_sensitive else search_input.upper()
    
    if search_type == "Contains (Partial)":
        design_results = design_df[design_df.astype(str).apply(lambda x: x.str.contains(search_term, case=case_sensitive, na=False)).any(axis=1)]
    elif search_type == "Exact Match":
        design_results = design_df[design_df['Design Name'].str.contains(f"^{re.escape(search_term)}$", case=case_sensitive, na=False)]
    elif search_type == "Starts With":
        design_results = design_df[design_df['Design Name'].str.startswith(search_term, na=False)]
    elif search_type == "Ends With":
        design_results = design_df[design_df['Design Name'].str.endswith(search_term, na=False)]
    
    # Search in yarn_df
    if search_type == "Contains (Partial)":
        yarn_results = yarn_df[yarn_df.astype(str).apply(lambda x: x.str.contains(search_term, case=case_sensitive, na=False)).any(axis=1)]
    elif search_type == "Exact Match":
        yarn_results = yarn_df[yarn_df['Design Name'].str.contains(f"^{re.escape(search_term)}$", case=case_sensitive, na=False)]
    elif search_type == "Starts With":
        yarn_results = yarn_df[yarn_df['Design Name'].str.startswith(search_term, na=False)]
    elif search_type == "Ends With":
        yarn_results = yarn_df[yarn_df['Design Name'].str.endswith(search_term, na=False)]
    
    # Display results
    if not design_results.empty or not yarn_results.empty:
        st.markdown(f"""
        <div class="success-message">
            ✅ Search Results for "{search_input}" - Found {len(design_results)} design records and {len(yarn_results)} yarn records
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        display_metrics_cards({
            "Design Matches": len(design_results),
            "Yarn Matches": len(yarn_results),
            "Search Type": search_type.split()[0],
            "Total Records": len(design_results) + len(yarn_results)
        })
        
        # Tabs for results
        tab1, tab2, tab3 = st.tabs(["🎨 Design Results", "🧶 Yarn Results", "📊 Combined Analysis"])
        
        with tab1:
            if not design_results.empty:
                st.markdown("### 🎨 Aviation Carpet Design Results")
                st.dataframe(design_results, use_container_width=True, height=400)
                
                # Show Frame-wise Color if available
                if 'Frame-wise Color' in design_results.columns:
                    st.markdown("### 🎯 Frame-wise Color Analysis")
                    for idx, row in design_results.iterrows():
                        if pd.notna(row['Frame-wise Color']) and row['Frame-wise Color']:
                            st.markdown(f"**{row['Design Name']}:** {row['Frame-wise Color']}")
            else:
                st.info("No design records found for this search term.")
        
        with tab2:
            if not yarn_results.empty:
                st.markdown("### 🧶 Yarn Specification Results")
                st.dataframe(yarn_results, use_container_width=True, height=400)
            else:
                st.info("No yarn records found for this search term.")
        
        with tab3:
            if not design_results.empty and not yarn_results.empty:
                st.markdown("### 📊 Combined Design & Yarn Analysis")
                
                # Merge results on Design Name
                if 'Design Name' in design_results.columns and 'Design Name' in yarn_results.columns:
                    combined_results = pd.merge(design_results, yarn_results, on='Design Name', how='inner', suffixes=('_Design', '_Yarn'))
                    
                    if not combined_results.empty:
                        st.markdown(f"**✅ {len(combined_results)} designs have both design and yarn specifications**")
                        st.dataframe(combined_results, use_container_width=True, height=400)
                        
                        # Show Frame-wise Color analysis for combined results
                        if 'Frame-wise Color' in combined_results.columns:
                            st.markdown("### 🎯 Frame-wise Color Analysis (Combined)")
                            for idx, row in combined_results.iterrows():
                                if pd.notna(row['Frame-wise Color']) and row['Frame-wise Color']:
                                    st.markdown(f"**{row['Design Name']}:** {row['Frame-wise Color']}")
                    else:
                        st.warning("No designs found with both design and yarn specifications.")
                else:
                    st.error("Cannot combine results - Design Name column not found in both datasets.")
            else:
                st.info("Combined analysis requires results from both design and yarn searches.")
        
        # Export options
        if show_export:
            st.markdown("### 📥 Export Search Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Export Design Results"):
                    excel_data = create_export_excel(
                        {"Design_Results": design_results, "Yarn_Results": yarn_results},
                        f"search_results_{search_input}"
                    )
                    st.download_button(
                        label="📥 Download Excel File",
                        data=excel_data,
                        file_name=f"search_results_{search_input}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            with col2:
                if st.button("📋 Export to CSV"):
                    csv_data = design_results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV File",
                        data=csv_data,
                        file_name=f"design_results_{search_input}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            with col3:
                if st.button("🔗 Generate Report"):
                    st.markdown(f"""
                    **Search Report**
                    - **Search Term:** {search_input}
                    - **Search Type:** {search_type}
                    - **Case Sensitive:** {case_sensitive}
                    - **Design Matches:** {len(design_results)}
                    - **Yarn Matches:** {len(yarn_results)}
                    - **Search Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    """)
    
    else:
        st.markdown(f"""
        <div class="error-message">
            ❌ No results found for "{search_input}". Try different search terms or check your spelling.
        </div>
        """, unsafe_allow_html=True)
        
        # Suggestions
        if st.session_state.design_df is not None:
            st.markdown("### 💡 Available Design Names (Sample):")
            sample_designs = st.session_state.design_df['Design Name'].dropna().head(10).tolist()
            st.write(", ".join(sample_designs))

# --- Analytics Dashboard ---
if show_analytics and st.session_state.design_df is not None:
    st.markdown("---")
    st.markdown("## 📈 Aviation Carpet Analytics Dashboard")
    
    design_df = st.session_state.design_df
    yarn_df = st.session_state.yarn_df
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_designs = len(design_df)
        st.metric("Total Designs", total_designs)
    with col2:
        unique_designs = design_df['Design Name'].nunique() if 'Design Name' in design_df.columns else 0
        st.metric("Unique Designs", unique_designs)
    with col3:
        total_yarns = len(yarn_df)
        st.metric("Yarn Records", total_yarns)
    with col4:
        completion_rate = round((unique_designs / total_designs * 100), 1) if total_designs > 0 else 0
        st.metric("Data Completeness", f"{completion_rate}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Design distribution
        if 'Design Name' in design_df.columns:
            design_counts = design_df['Design Name'].value_counts().head(10)
            fig = px.bar(
                x=design_counts.index,
                y=design_counts.values,
                title="Top 10 Aviation Carpet Designs",
                labels={'x': 'Design Name', 'y': 'Count'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Color analysis
        all_colors = []
        color_columns = [col for col in design_df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade'])]
        for col in color_columns:
            for value in design_df[col].dropna():
                colors = extract_colors_from_text(str(value))
                all_colors.extend(colors)
        
        if all_colors:
            color_counts = pd.Series(all_colors).value_counts().head(10)
            fig = px.pie(
                values=color_counts.values,
                names=color_counts.index,
                title="Top 10 Color Distribution"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Frame-wise Color Analysis
    if 'Frame-wise Color' in design_df.columns:
        st.markdown("### 🎯 Frame-wise Color Analysis")
        
        frame_color_data = design_df[design_df['Frame-wise Color'].notna()]['Frame-wise Color']
        if not frame_color_data.empty:
            # Count color occurrences in frame-wise colors
            frame_colors = []
            for color_sequence in frame_color_data:
                if color_sequence:
                    colors = color_sequence.split(" - ")
                    frame_colors.extend(colors)
            
            if frame_colors:
                frame_color_counts = pd.Series(frame_colors).value_counts().head(15)
                fig = px.bar(
                    x=frame_color_counts.values,
                    y=frame_color_counts.index,
                    orientation='h',
                    title="Most Used Colors in Frame-wise Sequences",
                    labels={'x': 'Frequency', 'y': 'Color'}
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show sample frame-wise color sequences
                st.markdown("### 🎨 Sample Frame-wise Color Sequences")
                sample_sequences = frame_color_data.head(10)
                for i, (idx, sequence) in enumerate(sample_sequences.items()):
                    design_name = design_df.loc[idx, 'Design Name'] if 'Design Name' in design_df.columns else f"Design {i+1}"
                    st.markdown(f"**{design_name}:** {sequence}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #2c3e50, #34495e); color: white; border-radius: 15px;">
    <h3 style="margin-bottom: 1rem;">✈️ WILTON WEAVERS</h3>
    <p style="margin-bottom: 0.5rem;"><strong>Specialists in Aviation Carpets & Fine Wool Broadloom</strong></p>
    <p style="margin-bottom: 0.5rem;">📍 Kerala, India | 📞 Contact: wilton.in | 📧 Professional Aviation Carpet Solutions</p>
    <p style="margin-bottom: 0; font-size: 0.9rem; opacity: 0.8;">© 2024 Wilton Weavers | Est. 1982 | 40+ Years of Excellence in Aviation Floor Coverings</p>
</div>
""", unsafe_allow_html=True)
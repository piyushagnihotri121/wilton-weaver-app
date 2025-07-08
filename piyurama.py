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

# --- NEW: Frame-wise Color Analysis Functions ---
def extract_frame_wise_colors_from_yarn_description(yarn_description: str, num_frames: int = None) -> str:
    """
    Extract frame-wise colors from yarn description based on the logic:
    1. Ignore entries ending with 'CN' if same yarn exists with 'BB'
    2. Only keep 'CN' entries if no 'BB' equivalent exists
    3. Extract colors from remaining entries
    4. Map colors to frames sequentially
    """
    if pd.isna(yarn_description) or not yarn_description:
        return ""
    
    # Split yarn description into individual entries
    yarn_entries = [entry.strip() for entry in yarn_description.split('\n') if entry.strip()]
    
    # Separate BB and CN entries
    bb_entries = []
    cn_entries = []
    other_entries = []
    
    for entry in yarn_entries:
        if entry.endswith('-BB'):
            bb_entries.append(entry)
        elif entry.endswith('-CN'):
            cn_entries.append(entry)
        else:
            other_entries.append(entry)
    
    # Apply the logic: prefer BB over CN for same yarn
    selected_entries = []
    
    # First, add all BB entries
    selected_entries.extend(bb_entries)
    
    # Then, add CN entries only if no BB equivalent exists
    for cn_entry in cn_entries:
        cn_base = cn_entry[:-3]  # Remove '-CN'
        bb_equivalent = cn_base + '-BB'
        if bb_equivalent not in bb_entries:
            selected_entries.append(cn_entry)
    
    # Add other entries (those not ending with BB or CN)
    selected_entries.extend(other_entries)
    
    # Extract colors from selected entries
    frame_colors = []
    for entry in selected_entries:
        # Extract color from yarn description
        # Look for color keywords in the entry
        color_match = extract_color_from_yarn_entry(entry)
        if color_match:
            frame_colors.append(color_match)
    
    # If we have number of frames, ensure we have the right number of colors
    if num_frames and len(frame_colors) != num_frames:
        # If we have fewer colors than frames, repeat the last color
        while len(frame_colors) < num_frames:
            if frame_colors:
                frame_colors.append(frame_colors[-1])
            else:
                frame_colors.append("UNKNOWN")
        # If we have more colors than frames, truncate
        frame_colors = frame_colors[:num_frames]
    
    return " - ".join(frame_colors) if frame_colors else ""

def extract_color_from_yarn_entry(yarn_entry: str) -> str:
    """Extract color name from a single yarn entry"""
    if not yarn_entry:
        return ""
    
    # Common color patterns in yarn descriptions
    color_patterns = [
        r'WOOL\s+(\w+(?:\s+\w+)?)',  # WOOL COTTON WHITE, WOOL MINT, etc.
        r'PP\s+(\w+(?:\s+\w+)?)',    # PP BEIGE, etc.
        r'COTTON\s+(\w+)',           # COTTON WHITE, etc.
        r'(\w+)\s+WEFT',             # BEIGE WEFT, etc.
    ]
    
    for pattern in color_patterns:
        match = re.search(pattern, yarn_entry, re.IGNORECASE)
        if match:
            color = match.group(1).strip().upper()
            # Clean up common non-color words
            if color not in ['COTTON', 'WOOL', 'POLYESTER', 'JUTE', 'CHEMICAL', 'LATEX', 'THICKENER']:
                return color
    
    # Fallback: look for standalone color words
    color_words = ['WHITE', 'MINT', 'BEIGE', 'BLACK', 'BLUE', 'RED', 'GREEN', 'YELLOW', 'BROWN', 'GREY', 'GRAY']
    for word in color_words:
        if word in yarn_entry.upper():
            return word
    
    return "UNKNOWN"

def add_frame_wise_color_column(design_df: pd.DataFrame, yarn_df: pd.DataFrame) -> pd.DataFrame:
    """Add frame-wise color column to design dataframe"""
    if design_df is None or yarn_df is None:
        return design_df
    
    # Create a copy to avoid modifying the original
    enhanced_df = design_df.copy()
    
    # Find yarn description column
    yarn_desc_col = None
    for col in yarn_df.columns:
        if any(word in col.lower() for word in ['description', 'yarn', 'spec', 'detail']):
            yarn_desc_col = col
            break
    
    # Find frames column in design df
    frames_col = None
    for col in design_df.columns:
        if 'frame' in col.lower():
            frames_col = col
            break
    
    if yarn_desc_col and 'Design Name' in yarn_df.columns and 'Design Name' in design_df.columns:
        frame_wise_colors = []
        
        for _, row in enhanced_df.iterrows():
            design_name = row['Design Name']
            num_frames = None
            
            # Get number of frames if available
            if frames_col and pd.notna(row[frames_col]):
                try:
                    num_frames = int(row[frames_col])
                except (ValueError, TypeError):
                    num_frames = None
            
            # Find corresponding yarn description
            yarn_row = yarn_df[yarn_df['Design Name'] == design_name]
            if not yarn_row.empty:
                yarn_desc = yarn_row.iloc[0][yarn_desc_col]
                frame_colors = extract_frame_wise_colors_from_yarn_description(yarn_desc, num_frames)
                frame_wise_colors.append(frame_colors)
            else:
                frame_wise_colors.append("")
        
        # Add the new column
        enhanced_df['Frame Wise Colour'] = frame_wise_colors
    
    return enhanced_df

# --- CSS Styling ---
st.markdown("""
<style>
/* Main styling */
.main-header {
    background: linear-gradient(135deg, #2c3e50, #3498db);
    color: white;
    padding: 3rem 2rem;
    text-align: center;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.main-header h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.company-location {
    font-size: 1.2rem;
    opacity: 0.9;
    margin-bottom: 1rem;
    letter-spacing: 2px;
}

.heritage-badge {
    background: rgba(255,255,255,0.2);
    padding: 0.5rem 1.5rem;
    border-radius: 25px;
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

.metric-card {
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
    transition: transform 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-number {
    font-size: 2.5rem;
    font-weight: 700;
    color: #2c3e50;
    display: block;
    margin-bottom: 0.5rem;
}

.metric-label {
    color: #7f8c8d;
    font-size: 1rem;
    font-weight: 500;
}

.upload-section {
    background: linear-gradient(135deg, #f8f9fa, #ffffff);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    border: 2px dashed #bdc3c7;
    transition: all 0.3s ease;
}

.upload-section:hover {
    border-color: #3498db;
    background: linear-gradient(135deg, #ffffff, #f8f9fa);
}

.search-container {
    background: linear-gradient(135deg, #ecf0f1, #ffffff);
    padding: 2rem;
    border-radius: 15px;
    margin: 2rem 0;
    border-left: 4px solid #3498db;
}

.color-filter-section {
    background: linear-gradient(135deg, #f1c40f, #f39c12);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin: 2rem 0;
    text-align: center;
}

.color-chip {
    display: inline-block;
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    margin: 0.25rem;
    font-size: 0.9rem;
    font-weight: 500;
}

.match-type-info {
    background: linear-gradient(135deg, #e8f5e8, #d4edda);
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #27ae60;
}

.success-message {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    color: #155724;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border-left: 4px solid #28a745;
    font-weight: 500;
}

.error-message {
    background: linear-gradient(135deg, #f8d7da, #f5c6cb);
    color: #721c24;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    border-left: 4px solid #dc3545;
    font-weight: 500;
}

.dataframe-container {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.sidebar-content {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 1rem;
}

.search-history {
    background: linear-gradient(135deg, #95a5a6, #7f8c8d);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

/* Frame-wise color styling */
.frame-color-info {
    background: linear-gradient(135deg, #9b59b6, #8e44ad);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: center;
}

.frame-color-display {
    font-family: 'Courier New', monospace;
    font-size: 1.1rem;
    background: rgba(255,255,255,0.2);
    padding: 0.5rem;
    border-radius: 5px;
    margin: 0.5rem 0;
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
            'BLACK', 'WHITE', 'PEARL', 'PLATINUM', 'STONE GREY',
            'COTTON WHITE', 'MINT'  # Added based on your example
        }
    return sorted(list(all_colors))

def get_available_weft_heads(df: pd.DataFrame) -> List[str]:
    """Extract available weft heads from design dataframe"""
    if df is None or df.empty:
        return []
    
    weft_columns = [col for col in df.columns if 'weft' in col.lower()]
    all_weft_heads = set()
    
    for col in weft_columns:
        for value in df[col].dropna():
            weft_heads = extract_colors_from_text(str(value))
            all_weft_heads.update(weft_heads)
    
    return sorted(list(all_weft_heads)) if all_weft_heads else []

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
        <p>5️⃣ View Frame-wise Colors</p>
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
    show_frame_colors = st.checkbox("🎨 Frame-wise Colors", value=True)
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
    <h3>🎨 Enhanced Multi-Filter Design Search</h3>
    <p style="color: white; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Select multiple colors, construction, frames, and weft heads to find aviation carpet designs with frame-wise color analysis.
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
    available_weft_heads = get_available_weft_heads(df)

if not available_colors:
    available_colors = [
        'NAVY BLUE', 'ROYAL BLUE', 'DEEP BLUE', 'SKY BLUE',
        'BURGUNDY', 'WINE RED', 'CRIMSON', 'MAROON',
        'FOREST GREEN', 'EMERALD', 'SAGE GREEN', 'OLIVE',
        'CHARCOAL GREY', 'SILVER GREY', 'LIGHT GREY', 'STEEL GREY',
        'BEIGE', 'CREAM', 'IVORY', 'CHAMPAGNE',
        'GOLD', 'BRONZE', 'COPPER', 'AMBER',
        'BLACK', 'WHITE', 'PEARL', 'PLATINUM',
        'COTTON WHITE', 'MINT'
    ]

# --- Enhanced Filter UI ---
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
with col1:
    selected_colors = st.multiselect(
        "🎨 Select Colors",
        options=available_colors,
        help="Select one or more colors that should be present in the carpet design.",
        key="color_multiselect"
    )
with col2:
    selected_construction = st.selectbox(
        "🏗️ Construction",
        options=["Any"] + available_constructions if available_constructions else ["Any"],
        help="Filter by construction type"
    )
with col3:
    selected_frames = st.selectbox(
        "🖼️ No. of Frames",
        options=["Any"] + available_frames if available_frames else ["Any"],
        help="Filter by number of frames"
    )
with col4:
    selected_weft_head = st.selectbox(
        "🧵 Weft Head",
        options=["Any"] + available_weft_heads if available_weft_heads else ["Any"],
        help="Filter by weft head type"
    )
with col5:
    match_type = st.radio(
        "Match Type:",
        options=["All Colors (AND)", "Any Color (OR)"],
        help="All Colors: Design must contain ALL selected colors\nAny Color: Design must contain AT LEAST ONE selected color",
        key="match_type"
    )

# Search button
color_search_button = st.button("🔍 SEARCH WITH ENHANCED FILTERS", type="primary")

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

            # Clean column names
            design_df.columns = design_df.columns.str.strip()
            yarn_df.columns = yarn_df.columns.str.strip()
            
            # Store in session state
            st.session_state.design_df = design_df
            st.session_state.yarn_df = yarn_df
            
            # Add frame-wise color analysis if both dataframes are available
            if show_frame_colors:
                st.session_state.design_df = add_frame_wise_color_column(design_df, yarn_df)
            
            st.markdown("""
            <div class="success-message">
                ✅ <strong>Database Successfully Loaded!</strong><br>
                Design Records: <strong>{}</strong> | Yarn Records: <strong>{}</strong><br>
                Ready for aviation carpet design search with frame-wise color analysis.
            </div>
            """.format(len(design_df), len(yarn_df)), unsafe_allow_html=True)
            
            # Display metrics
            if show_analytics:
                metrics = {
                    "Total Designs": len(design_df),
                    "Yarn Records": len(yarn_df),
                    "Unique Designs": design_df['Design Name'].nunique() if 'Design Name' in design_df.columns else 0,
                    "Available Colors": len(get_available_colors(design_df))
                }
                display_metrics_cards(metrics)
    
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ <strong>Error Loading Files:</strong><br>
            {str(e)}<br>
            Please check your Excel files and try again.
        </div>
        """, unsafe_allow_html=True)

# --- Enhanced Search with Frame-wise Colors ---
if color_search_button and st.session_state.design_df is not None:
    if not selected_colors and selected_construction == "Any" and selected_frames == "Any" and selected_weft_head == "Any":
        st.warning("⚠️ Please select at least one filter option (color, construction, frames, or weft head) to search.")
    else:
        # Add search to history
        search_description = f"Colors: {', '.join(selected_colors) if selected_colors else 'Any'}"
        if selected_construction != "Any":
            search_description += f" | Construction: {selected_construction}"
        if selected_frames != "Any":
            search_description += f" | Frames: {selected_frames}"
        if selected_weft_head != "Any":
            search_description += f" | Weft: {selected_weft_head}"
        
        if search_description not in st.session_state.search_history:
            st.session_state.search_history.append(search_description)
        
        with st.spinner('🔍 Searching aviation carpet designs with frame-wise color analysis...'):
            df = st.session_state.design_df.copy()
            
            # Apply filters
            filtered_df = df.copy()
            
            # Color filter
            if selected_colors:
                color_columns = [col for col in df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
                
                if match_type == "All Colors (AND)":
                    # All selected colors must be present
                    for color in selected_colors:
                        color_mask = pd.Series([False] * len(df))
                        for col in color_columns:
                            color_mask |= df[col].astype(str).str.upper().str.contains(color, case=False, na=False)
                        filtered_df = filtered_df[color_mask]
                else:
                    # Any selected color must be present
                    color_mask = pd.Series([False] * len(df))
                    for color in selected_colors:
                        for col in color_columns:
                            color_mask |= df[col].astype(str).str.upper().str.contains(color, case=False, na=False)
                    filtered_df = filtered_df[color_mask]
            
            # Construction filter
            if selected_construction != "Any":
                construction_col = None
                for col in df.columns:
                    if 'construction' in col.lower():
                        construction_col = col
                        break
                if construction_col:
                    filtered_df = filtered_df[filtered_df[construction_col].astype(str).str.contains(selected_construction, case=False, na=False)]
            
            # Frames filter
            if selected_frames != "Any":
                frames_col = None
                for col in df.columns:
                    if 'frame' in col.lower():
                        frames_col = col
                        break
                if frames_col:
                    filtered_df = filtered_df[filtered_df[frames_col].astype(str) == selected_frames]
            
            # Weft head filter
            if selected_weft_head != "Any":
                weft_columns = [col for col in df.columns if 'weft' in col.lower()]
                if weft_columns:
                    weft_mask = pd.Series([False] * len(filtered_df))
                    for col in weft_columns:
                        weft_mask |= filtered_df[col].astype(str).str.upper().str.contains(selected_weft_head, case=False, na=False)
                    filtered_df = filtered_df[weft_mask]
            
            # Display results
            if not filtered_df.empty:
                st.markdown(f"""
                <div class="success-message">
                    🎯 <strong>Search Results:</strong> Found <strong>{len(filtered_df)}</strong> aviation carpet designs matching your criteria with frame-wise color analysis.
                </div>
                """, unsafe_allow_html=True)
                
                # Show frame-wise color info if available
                if show_frame_colors and 'Frame Wise Colour' in filtered_df.columns:
                    st.markdown("""
                    <div class="frame-color-info">
                        <h4>🎨 Frame-wise Color Analysis Available</h4>
                        <p>The results include frame-wise color information extracted from yarn descriptions, showing the color sequence for each frame in the design.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display results with frame-wise colors highlighted
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                
                # Reorder columns to show Frame Wise Colour prominently
                display_df = filtered_df.copy()
                if 'Frame Wise Colour' in display_df.columns:
                    cols = display_df.columns.tolist()
                    cols.remove('Frame Wise Colour')
                    # Insert Frame Wise Colour after Design Name
                    if 'Design Name' in cols:
                        design_name_idx = cols.index('Design Name')
                        cols.insert(design_name_idx + 1, 'Frame Wise Colour')
                    else:
                        cols.insert(0, 'Frame Wise Colour')
                    display_df = display_df[cols]
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    height=400
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Export options
                if show_export:
                    st.markdown("---")
                    st.subheader("📥 Export Options")
                    
                    export_cols = st.columns(3)
                    with export_cols[0]:
                        if st.button("📊 Export to Excel"):
                            export_data = {
                                'Search Results': filtered_df,
                                'Search Criteria': pd.DataFrame({
                                    'Filter': ['Colors', 'Construction', 'Frames', 'Weft Head', 'Match Type'],
                                    'Value': [
                                        ', '.join(selected_colors) if selected_colors else 'Any',
                                        selected_construction,
                                        selected_frames,
                                        selected_weft_head,
                                        match_type
                                    ]
                                })
                            }
                            excel_data = create_export_excel(export_data, "aviation_carpet_search")
                            st.download_button(
                                label="⬇️ Download Excel Report",
                                data=excel_data,
                                file_name=f"aviation_carpet_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    
                    with export_cols[1]:
                        if st.button("📋 Export to CSV"):
                            csv_data = filtered_df.to_csv(index=False)
                            st.download_button(
                                label="⬇️ Download CSV Report",
                                data=csv_data,
                                file_name=f"aviation_carpet_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
                    
                    with export_cols[2]:
                        if st.button("🎨 Export Frame Colors Only"):
                            if 'Frame Wise Colour' in filtered_df.columns:
                                frame_color_df = filtered_df[['Design Name', 'Frame Wise Colour']].copy()
                                frame_color_csv = frame_color_df.to_csv(index=False)
                                st.download_button(
                                    label="⬇️ Download Frame Colors",
                                    data=frame_color_csv,
                                    file_name=f"frame_wise_colors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )
                            else:
                                st.warning("Frame-wise color data not available. Please enable frame-wise colors in the sidebar.")
                
                # Analytics Dashboard
                if show_analytics:
                    st.markdown("---")
                    st.subheader("📈 Search Analytics")
                    
                    analytics_cols = st.columns(2)
                    
                    with analytics_cols[0]:
                        # Color distribution chart
                        if selected_colors:
                            color_counts = {}
                            color_columns = [col for col in filtered_df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
                            
                            for col in color_columns:
                                for _, row in filtered_df.iterrows():
                                    if pd.notna(row[col]):
                                        colors_in_row = extract_colors_from_text(str(row[col]))
                                        for color in colors_in_row:
                                            if color in selected_colors:
                                                color_counts[color] = color_counts.get(color, 0) + 1
                            
                            if color_counts:
                                fig = px.bar(
                                    x=list(color_counts.keys()),
                                    y=list(color_counts.values()),
                                    title="Color Distribution in Results",
                                    labels={'x': 'Colors', 'y': 'Count'}
                                )
                                fig.update_layout(height=400)
                                st.plotly_chart(fig, use_container_width=True)
                    
                    with analytics_cols[1]:
                        # Frame-wise color analysis
                        if 'Frame Wise Colour' in filtered_df.columns:
                            frame_color_stats = {}
                            for _, row in filtered_df.iterrows():
                                if pd.notna(row['Frame Wise Colour']) and row['Frame Wise Colour']:
                                    colors = row['Frame Wise Colour'].split(' - ')
                                    num_colors = len(colors)
                                    frame_color_stats[f"{num_colors} Colors"] = frame_color_stats.get(f"{num_colors} Colors", 0) + 1
                            
                            if frame_color_stats:
                                fig = px.pie(
                                    values=list(frame_color_stats.values()),
                                    names=list(frame_color_stats.keys()),
                                    title="Frame Color Complexity Distribution"
                                )
                                fig.update_layout(height=400)
                                st.plotly_chart(fig, use_container_width=True)
                
                # Frame-wise color details
                if show_frame_colors and 'Frame Wise Colour' in filtered_df.columns:
                    st.markdown("---")
                    st.subheader("🎨 Frame-wise Color Details")
                    
                    for _, row in filtered_df.head(5).iterrows():  # Show first 5 designs
                        if pd.notna(row['Frame Wise Colour']) and row['Frame Wise Colour']:
                            with st.expander(f"🎯 {row['Design Name']} - Frame Color Analysis"):
                                frame_colors = row['Frame Wise Colour'].split(' - ')
                                
                                st.markdown(f"""
                                <div class="frame-color-display">
                                    <strong>Design:</strong> {row['Design Name']}<br>
                                    <strong>Total Frames:</strong> {len(frame_colors)}<br>
                                    <strong>Frame Sequence:</strong> {' → '.join(frame_colors)}
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Show frame-by-frame breakdown
                                frame_cols = st.columns(len(frame_colors))
                                for i, color in enumerate(frame_colors):
                                    with frame_cols[i]:
                                        st.markdown(f"""
                                        <div style="background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                                            <strong>Frame {i+1}</strong><br>
                                            <span style="font-size: 1.1rem;">{color}</span>
                                        </div>
                                        """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div class="error-message">
                    ❌ <strong>No Results Found</strong><br>
                    No aviation carpet designs match your search criteria. Try adjusting your filters or search terms.
                </div>
                """, unsafe_allow_html=True)
                
                # Suggestions
                st.markdown("### 💡 Search Suggestions:")
                suggestions = st.columns(3)
                with suggestions[0]:
                    st.info("🎨 **Try fewer colors** - Use 1-2 colors instead of many")
                with suggestions[1]:
                    st.info("🔄 **Change match type** - Try 'Any Color' instead of 'All Colors'")
                with suggestions[2]:
                    st.info("📋 **Check filters** - Ensure construction/frames/weft values exist")

# --- Text Search Section ---
st.markdown("---")
st.markdown("""
<div class="search-container">
    <h3>🔍 Text-based Design Search</h3>
    <p style="color: #7f8c8d; font-family: 'Inter', sans-serif;">Search for specific aviation carpet designs by name, pattern, or specifications</p>
</div>
""", unsafe_allow_html=True)

search_input = st.text_input(
    "Enter design name, pattern, or specifications:",
    placeholder="e.g., SERA-SAGE, aviation carpet, wool pattern, etc.",
    help="Search across all design fields including names, patterns, and specifications",
    key="search_input"
)

text_search_button = st.button("🔍 SEARCH DESIGNS", type="secondary")

if text_search_button and search_input and st.session_state.design_df is not None:
    if search_input not in st.session_state.search_history:
        st.session_state.search_history.append(search_input)
    
    with st.spinner('🔍 Searching aviation carpet database...'):
        df = st.session_state.design_df
        
        # Search across all text columns
        search_cols = df.select_dtypes(include=['object']).columns
        mask = pd.Series([False] * len(df))
        
        for col in search_cols:
            if not case_sensitive:
                mask |= df[col].astype(str).str.upper().str.contains(search_input.upper(), na=False)
            else:
                mask |= df[col].astype(str).str.contains(search_input, na=False)
        
        results = df[mask]
        
        if not results.empty:
            st.markdown(f"""
            <div class="success-message">
                🎯 <strong>Search Results:</strong> Found <strong>{len(results)}</strong> aviation carpet designs matching "<strong>{search_input}</strong>"
            </div>
            """, unsafe_allow_html=True)
            
            # Display results with frame-wise colors
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            
            # Reorder columns for better display
            display_df = results.copy()
            if 'Frame Wise Colour' in display_df.columns:
                cols = display_df.columns.tolist()
                cols.remove('Frame Wise Colour')
                if 'Design Name' in cols:
                    design_name_idx = cols.index('Design Name')
                    cols.insert(design_name_idx + 1, 'Frame Wise Colour')
                else:
                    cols.insert(0, 'Frame Wise Colour')
                display_df = display_df[cols]
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.markdown(f"""
            <div class="error-message">
                ❌ <strong>No Results Found</strong><br>
                No aviation carpet designs match your search for "<strong>{search_input}</strong>". Try different keywords or check spelling.
            </div>
            """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #2c3e50, #34495e); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-top: 3rem;">
    <h3 style="margin-bottom: 1rem;">✈️ WILTON WEAVERS - AVIATION EXCELLENCE</h3>
    <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 1rem;">
        <div>🏭 <strong>Manufacturing Since 1982</strong></div>
        <div>✈️ <strong>Aviation Carpet Specialists</strong></div>
        <div>🧶 <strong>Fine Wool Broadloom</strong></div>
        <div>🇮🇳 <strong>Kerala, India</strong></div>
    </div>
    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">
        Proudly serving the aviation industry with premium quality carpets and innovative solutions.<br>
        Visit us at <strong>wilton.in</strong> | Email: <strong>info@wilton.in</strong>
    </p>
</div>
""", unsafe_allow_html=True)


            
             
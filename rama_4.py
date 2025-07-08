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
    """Clean and standardize design name"""
    if pd.isna(name):
        return ""
    return str(name).strip().upper()

def extract_colors_from_text(text: str) -> List[str]:
    """Extract colors from text using various separators"""
    if pd.isna(text) or not text:
        return []
    
    # Common separators used in color descriptions
    separators = [',', ';', '/', '|', '+', '&', '-', '\n', '\t']
    colors = [str(text)]
    
    # Split by each separator
    for sep in separators:
        new_colors = []
        for color in colors:
            new_colors.extend(color.split(sep))
        colors = new_colors
    
    # Clean and filter colors
    cleaned_colors = []
    for color in colors:
        color = str(color).strip().upper()
        if color and color != 'NAN' and len(color) > 1:
            cleaned_colors.append(color)
    
    return list(set(cleaned_colors))

def extract_frame_colors_from_yarn_description(yarn_desc: str) -> str:
    """Extract frame-wise colors from yarn description"""
    if pd.isna(yarn_desc) or not yarn_desc:
        return ""
    
    try:
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
    except Exception as e:
        st.error(f"Error extracting frame colors: {str(e)}")
        return ""

def get_available_colors(df: pd.DataFrame) -> List[str]:
    """Get all available colors from the dataframe"""
    if df is None or df.empty:
        return []
    
    try:
        color_columns = [col for col in df.columns if 
                        any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye', 'hue'])]
        
        all_colors = set()
        for col in color_columns:
            for value in df[col].dropna():
                colors = extract_colors_from_text(str(value))
                all_colors.update(colors)
        
        # If no colors found, return default aviation carpet colors
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
    except Exception as e:
        st.error(f"Error getting available colors: {str(e)}")
        return []

def get_available_weft_heads(df: pd.DataFrame) -> List[str]:
    """Extract available weft head options from the dataframe"""
    if df is None or df.empty:
        return []
    
    try:
        weft_head_col = None
        for col in df.columns:
            if 'weft' in col.lower() and 'head' in col.lower():
                weft_head_col = col
                break
        
        if weft_head_col:
            return sorted(df[weft_head_col].dropna().astype(str).str.strip().unique())
        return []
    except Exception as e:
        st.error(f"Error getting weft heads: {str(e)}")
        return []

def safe_color_search(df: pd.DataFrame, selected_colors: List[str], match_type: str) -> pd.DataFrame:
    """Safely search for colors in the dataframe with proper error handling"""
    if df is None or df.empty or not selected_colors:
        return df
    
    try:
        # Reset index to ensure proper alignment
        df_reset = df.reset_index(drop=True)
        
        color_columns = [col for col in df_reset.columns if 
                        any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
        
        if not color_columns:
            st.warning("No color columns found in the data")
            return df_reset
        
        # Initialize result mask
        if match_type == "All Colors (AND)":
            # All selected colors must be present
            result_mask = pd.Series([True] * len(df_reset))
            
            for color in selected_colors:
                color_found_mask = pd.Series([False] * len(df_reset))
                
                for col in color_columns:
                    try:
                        # Safe string conversion and search
                        col_mask = df_reset[col].astype(str).str.upper().str.contains(color, na=False, regex=False)
                        color_found_mask = color_found_mask | col_mask
                    except Exception as e:
                        st.warning(f"Error searching color '{color}' in column '{col}': {str(e)}")
                        continue
                
                # For AND operation, all colors must be found
                result_mask = result_mask & color_found_mask
        else:
            # At least one selected color must be present (OR)
            result_mask = pd.Series([False] * len(df_reset))
            
            for color in selected_colors:
                for col in color_columns:
                    try:
                        # Safe string conversion and search
                        col_mask = df_reset[col].astype(str).str.upper().str.contains(color, na=False, regex=False)
                        result_mask = result_mask | col_mask
                    except Exception as e:
                        st.warning(f"Error searching color '{color}' in column '{col}': {str(e)}")
                        continue
        
        # Apply the mask safely
        filtered_df = df_reset[result_mask]
        return filtered_df
        
    except Exception as e:
        st.error(f"Error in color search: {str(e)}")
        return df

def safe_filter_by_column(df: pd.DataFrame, column_pattern: str, filter_value: str) -> pd.DataFrame:
    """Safely filter dataframe by column pattern and value"""
    if df is None or df.empty or not filter_value or filter_value == "Any":
        return df
    
    try:
        # Reset index to ensure proper alignment
        df_reset = df.reset_index(drop=True)
        
        # Find column matching pattern
        target_col = None
        for col in df_reset.columns:
            if column_pattern.lower() in col.lower():
                target_col = col
                break
        
        if target_col:
            # Safe string conversion and filtering
            mask = df_reset[target_col].astype(str).str.contains(filter_value, na=False, case=False, regex=False)
            return df_reset[mask]
        else:
            st.warning(f"Column with pattern '{column_pattern}' not found")
            return df_reset
            
    except Exception as e:
        st.error(f"Error filtering by {column_pattern}: {str(e)}")
        return df

def create_export_excel(data_dict: Dict[str, pd.DataFrame], filename_prefix: str) -> bytes:
    """Create Excel file with multiple sheets"""
    try:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"Error creating Excel file: {str(e)}")
        return b""

def display_metrics_cards(metrics: Dict[str, int]):
    """Display metrics in card format"""
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
        
        if 'Design Name' in st.session_state.design_df.columns:
            unique_designs = st.session_state.design_df['Design Name'].nunique()
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

# --- Multi-Filter Section ---
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
    available_colors = get_available_colors(df)
    
    # Construction
    construction_cols = [col for col in df.columns if 'construction' in col.lower()]
    if construction_cols:
        available_constructions = sorted(df[construction_cols[0]].dropna().astype(str).str.strip().unique())
    
    # No. of Frames
    frames_cols = [col for col in df.columns if 'frame' in col.lower()]
    if frames_cols:
        available_frames = sorted(df[frames_cols[0]].dropna().astype(str).str.strip().unique())
    
    # Weft Head
    available_weft_heads = get_available_weft_heads(df)

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
            # Read Excel files
            design_df = pd.read_excel(design_file)
            yarn_df = pd.read_excel(yarn_file)
            
            # Store in session state
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
            yarn_desc_cols = [col for col in yarn_df.columns if 'yarn' in col.lower() and 'description' in col.lower()]
            if yarn_desc_cols:
                yarn_df['Frame_Colors'] = yarn_df[yarn_desc_cols[0]].apply(extract_frame_colors_from_yarn_description)
            
            st.markdown("""
            <div class="success-message">
                ✅ Files processed successfully! Aviation carpet database ready for analysis.
            </div>
            """, unsafe_allow_html=True)
            
            # Display summary metrics
            metrics = {
                "Design Records": len(design_df),
                "Yarn Records": len(yarn_df),
                "Unique Designs": design_df['Design Name'].nunique() if 'Design Name' in design_df.columns else 0,
                "Data Columns": len(design_df.columns) + len(yarn_df.columns)
            }
            display_metrics_cards(metrics)
            
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error processing files: {str(e)}. Please check your Excel file format and try again.
        </div>
        """, unsafe_allow_html=True)
        st.error(f"Detailed error: {str(e)}")

# --- Search and Filter Logic ---
filtered_design_df = None
filtered_yarn_df = None

if st.session_state.design_df is not None and st.session_state.yarn_df is not None:
    # Apply filters
    current_design_df = st.session_state.design_df.copy()
    current_yarn_df = st.session_state.yarn_df.copy()
    
    # Reset index to ensure proper alignment
    current_design_df = current_design_df.reset_index(drop=True)
    current_yarn_df = current_yarn_df.reset_index(drop=True)
    
    # Filter by colors
    if selected_colors and color_search_button:
        try:
            # Color search with fixed indexing
            color_columns = [col for col in current_design_df.columns if 
                           any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
            
            if color_columns:
                if match_type == "All Colors (AND)":
                    # All selected colors must be present
                    result_indices = set(current_design_df.index)
                    
                    for color in selected_colors:
                        color_indices = set()
                        for col in color_columns:
                            try:
                                mask = current_design_df[col].astype(str).str.upper().str.contains(color, na=False, regex=False)
                                color_indices.update(current_design_df.index[mask])
                            except Exception:
                                continue
                        
                        # For AND operation, keep only rows that contain this color
                        result_indices = result_indices.intersection(color_indices)
                else:
                    # At least one selected color must be present (OR)
                    result_indices = set()
                    
                    for color in selected_colors:
                        for col in color_columns:
                            try:
                                mask = current_design_df[col].astype(str).str.upper().str.contains(color, na=False, regex=False)
                                result_indices.update(current_design_df.index[mask])
                            except Exception:
                                continue
                
                # Filter dataframe using indices
                current_design_df = current_design_df.loc[list(result_indices)]
                
                # Filter yarn dataframe based on matching design names
                if 'Design Name' in current_design_df.columns and 'Design Name' in current_yarn_df.columns:
                    matching_designs = current_design_df['Design Name'].unique()
                    yarn_mask = current_yarn_df['Design Name'].isin(matching_designs)
                    current_yarn_df = current_yarn_df[yarn_mask]
                
        except Exception as e:
            st.error(f"Error in color filtering: {str(e)}")
    
    # Filter by construction
    if selected_construction and selected_construction != "Any":
        try:
            construction_cols = [col for col in current_design_df.columns if 'construction' in col.lower()]
            if construction_cols:
                mask = current_design_df[construction_cols[0]].astype(str).str.contains(selected_construction, na=False, case=False, regex=False)
                current_design_df = current_design_df[mask]
        except Exception as e:
            st.error(f"Error filtering by construction: {str(e)}")
    
    # Filter by frames
    if selected_frames and selected_frames != "Any":
        try:
            frames_cols = [col for col in current_design_df.columns if 'frame' in col.lower()]
            if frames_cols:
                mask = current_design_df[frames_cols[0]].astype(str).str.contains(selected_frames, na=False, case=False, regex=False)
                current_design_df = current_design_df[mask]
        except Exception as e:
            st.error(f"Error filtering by frames: {str(e)}")
    
    # Filter by weft head
    if selected_weft_head and selected_weft_head != "Any":
        try:
            weft_head_cols = [col for col in current_design_df.columns if 'weft' in col.lower() and 'head' in col.lower()]
            if weft_head_cols:
                mask = current_design_df[weft_head_cols[0]].astype(str).str.contains(selected_weft_head, na=False, case=False, regex=False)
                current_design_df = current_design_df[mask]
        except Exception as e:
            st.error(f"Error filtering by weft head: {str(e)}")
    
    filtered_design_df = current_design_df
    filtered_yarn_df = current_yarn_df

# --- Results Display ---
if filtered_design_df is not None and filtered_yarn_df is not None:
    if not filtered_design_df.empty:
        st.markdown("---")
        st.markdown("## 🎯 Search Results")
        
        # Results metrics
        result_metrics = {
            "Matching Designs": len(filtered_design_df),
            "Yarn Entries": len(filtered_yarn_df),
            "Unique Patterns": filtered_design_df['Design Name'].nunique() if 'Design Name' in filtered_design_df.columns else 0
        }
        display_metrics_cards(result_metrics)
        
        # Display frame colors if available
        if 'Frame_Colors' in filtered_yarn_df.columns:
            unique_frame_colors = []
            for colors in filtered_yarn_df['Frame_Colors'].dropna():
                if colors:
                    unique_frame_colors.extend(colors.split(' ; '))
            
            if unique_frame_colors:
                unique_frame_colors = sorted(set(unique_frame_colors))
                st.markdown(f"""
                <div class="frame-colors-display">
                    <h4>🎨 Frame-wise Colors Found:</h4>
                    {''.join([f'<span class="frame-color-item">{color}</span>' for color in unique_frame_colors])}
                </div>
                """, unsafe_allow_html=True)
        
        # Display results in tabs
        tab1, tab2, tab3 = st.tabs(["📋 Design Details", "🧶 Yarn Specifications", "📊 Analytics"])
        
        with tab1:
            st.markdown("""
            <div class="dataframe-container">
                <h4>Design Master Results</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Display design dataframe
            st.dataframe(
                filtered_design_df,
                use_container_width=True,
                height=400
            )
            
            # Export options
            if show_export:
                col1, col2 = st.columns(2)
                with col1:
                    csv_data = filtered_design_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Design CSV",
                        data=csv_data,
                        file_name=f"wilton_designs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    if not filtered_design_df.empty:
                        excel_data = create_export_excel(
                            {"Design_Master": filtered_design_df, "Yarn_Specifications": filtered_yarn_df},
                            "wilton_aviation_carpets"
                        )
                        if excel_data:
                            st.download_button(
                                label="📥 Download Excel Report",
                                data=excel_data,
                                file_name=f"wilton_aviation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
        
        with tab2:
            st.markdown("""
            <div class="dataframe-container">
                <h4>Yarn Specifications Results</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Display yarn dataframe
            st.dataframe(
                filtered_yarn_df,
                use_container_width=True,
                height=400
            )
            
            # Export yarn data
            if show_export:
                yarn_csv = filtered_yarn_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Yarn CSV",
                    data=yarn_csv,
                    file_name=f"wilton_yarn_specs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with tab3:
            if show_analytics:
                st.markdown("### 📊 Analytics Dashboard")
                
                # Analytics charts
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'Design Name' in filtered_design_df.columns:
                        # Design name frequency
                        design_counts = filtered_design_df['Design Name'].value_counts().head(10)
                        if not design_counts.empty:
                            fig = px.bar(
                                x=design_counts.index,
                                y=design_counts.values,
                                title="Top 10 Design Patterns",
                                labels={'x': 'Design Name', 'y': 'Count'},
                                color=design_counts.values,
                                color_continuous_scale='viridis'
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Construction type analysis
                    construction_cols = [col for col in filtered_design_df.columns if 'construction' in col.lower()]
                    if construction_cols:
                        construction_counts = filtered_design_df[construction_cols[0]].value_counts()
                        if not construction_counts.empty:
                            fig = px.pie(
                                values=construction_counts.values,
                                names=construction_counts.index,
                                title="Construction Type Distribution"
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                
                # Color analysis
                color_columns = [col for col in filtered_design_df.columns if 
                               any(word in col.lower() for word in ['color', 'colour', 'shade'])]
                
                if color_columns:
                    st.markdown("#### 🎨 Color Analysis")
                    all_colors = []
                    for col in color_columns:
                        for value in filtered_design_df[col].dropna():
                            colors = extract_colors_from_text(str(value))
                            all_colors.extend(colors)
                    
                    if all_colors:
                        color_counts = pd.Series(all_colors).value_counts().head(15)
                        fig = px.bar(
                            x=color_counts.values,
                            y=color_counts.index,
                            orientation='h',
                            title="Most Common Colors in Aviation Carpets",
                            labels={'x': 'Frequency', 'y': 'Color'},
                            color=color_counts.values,
                            color_continuous_scale='rainbow'
                        )
                        fig.update_layout(height=500)
                        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.markdown("""
        <div class="error-message">
            🔍 No matching designs found with the selected criteria. Try adjusting your filters or search terms.
        </div>
        """, unsafe_allow_html=True)
        
        # Suggestions
        st.markdown("### 💡 Search Suggestions:")
        st.markdown("- Try selecting fewer colors for broader results")
        st.markdown("- Use 'Any Color (OR)' instead of 'All Colors (AND)'")
        st.markdown("- Check if your color names match the database format")
        st.markdown("- Try different construction types or remove construction filter")

# --- Design Name Search ---
if st.session_state.design_df is not None:
    st.markdown("---")
    st.markdown("""
    <div class="search-container">
        <h3>🔍 Quick Design Name Search</h3>
        <p>Enter a design name or pattern to find specific aviation carpet designs</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Enter Design Name or Pattern:",
            placeholder="e.g., AV-2024-001, BOEING-BLUE, AIRBUS-CLASSIC",
            help="Search for specific design names or patterns in your aviation carpet database",
            key="search_input"
        )
    
    with col2:
        search_button = st.button("🔍 SEARCH", type="primary")
    
    if search_query and search_button:
        # Add to search history
        if search_query not in st.session_state.search_history:
            st.session_state.search_history.append(search_query)
            if len(st.session_state.search_history) > 10:
                st.session_state.search_history.pop(0)
        
        # Search in design dataframe
        search_results_design = st.session_state.design_df[
            st.session_state.design_df['Design Name'].str.contains(search_query, case=not case_sensitive, na=False)
        ]
        
        # Search in yarn dataframe
        search_results_yarn = st.session_state.yarn_df[
            st.session_state.yarn_df['Design Name'].str.contains(search_query, case=not case_sensitive, na=False)
        ]
        
        if not search_results_design.empty or not search_results_yarn.empty:
            st.markdown(f"### 🎯 Search Results for: '{search_query}'")
            
            # Display metrics
            search_metrics = {
                "Design Matches": len(search_results_design),
                "Yarn Matches": len(search_results_yarn),
                "Total Results": len(search_results_design) + len(search_results_yarn)
            }
            display_metrics_cards(search_metrics)
            
            # Display results in tabs
            tab1, tab2 = st.tabs(["📋 Design Results", "🧶 Yarn Results"])
            
            with tab1:
                if not search_results_design.empty:
                    st.dataframe(search_results_design, use_container_width=True)
                    
                    # Export option
                    if show_export:
                        csv_data = search_results_design.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Search Results (CSV)",
                            data=csv_data,
                            file_name=f"search_results_{search_query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                else:
                    st.info("No design results found for this search query.")
            
            with tab2:
                if not search_results_yarn.empty:
                    st.dataframe(search_results_yarn, use_container_width=True)
                    
                    # Show frame colors if available
                    if 'Frame_Colors' in search_results_yarn.columns:
                        frame_colors = []
                        for colors in search_results_yarn['Frame_Colors'].dropna():
                            if colors:
                                frame_colors.extend(colors.split(' ; '))
                        
                        if frame_colors:
                            unique_frame_colors = sorted(set(frame_colors))
                            st.markdown(f"""
                            <div class="frame-colors-display">
                                <h4>🎨 Frame Colors for '{search_query}':</h4>
                                {''.join([f'<span class="frame-color-item">{color}</span>' for color in unique_frame_colors])}
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No yarn results found for this search query.")
        else:
            st.markdown(f"""
            <div class="error-message">
                🔍 No results found for: '{search_query}'. Please check the spelling or try a different search term.
            </div>
            """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #2c3e50, #3498db); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
    <h4>✈️ WILTON WEAVERS - Aviation Carpet Specialists</h4>
    <p style="margin: 0.5rem 0;">🏭 <strong>Since 1982</strong> • Kerala, India • Private Family Business</p>
    <p style="margin: 0.5rem 0;">🌟 <strong>Specialization:</strong> Aviation Carpets & Fine Wool Broadloom</p>
    <p style="margin: 0.5rem 0;">📞 <strong>Contact:</strong> <a href="https://www.wilton.in" target="_blank" style="color: #ffeaa7;">www.wilton.in</a></p>
    <p style="margin: 1rem 0 0 0; font-size: 0.9rem; color: #bdc3c7;">
        Quality Floor Coverings • Innovators Par Excellence • 40+ Years of Collective Expertise
    </p>
</div>
""", unsafe_allow_html=True)

# --- Auto-refresh logic ---
if auto_refresh:
    st.rerun()

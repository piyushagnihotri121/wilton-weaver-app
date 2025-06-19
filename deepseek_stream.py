import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
import io
from PIL import Image

# Set page config with luxurious styling
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

# Load logo (would need actual image file in production)
# logo = Image.open("wilton_logo.png")

# Premium Custom CSS with luxurious styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Montserrat:wght@300;400;500;600;700&family=Lora:wght@400;600;700&display=swap');
    
    :root {
        --primary: #0a3d62;
        --secondary: #3c6382;
        --accent: #e58e26;
        --light: #f5f6fa;
        --dark: #2f3640;
        --text: #333333;
        --gold: #f9ca24;
    }
    
    .main-header {
        background: linear-gradient(rgba(10, 61, 98, 0.9), rgba(10, 61, 98, 0.95)), url('https://images.unsplash.com/photo-1605100804763-247f67b3557e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        padding: 5rem 2rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-bottom: 4px solid var(--accent);
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 4.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .company-location {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.5rem;
        font-weight: 500;
        margin: 0.5rem 0;
        color: var(--light);
        letter-spacing: 3px;
        text-transform: uppercase;
        position: relative;
        z-index: 2;
    }
    
    .company-tagline {
        font-family: 'Lora', serif;
        font-size: 1.4rem;
        font-weight: 400;
        margin: 1.5rem auto 0;
        max-width: 800px;
        line-height: 1.6;
        color: rgba(255,255,255,0.9);
        position: relative;
        z-index: 2;
    }
    
    .heritage-badge {
        background: linear-gradient(135deg, var(--accent), #d35400);
        color: white;
        padding: 0.7rem 2rem;
        border-radius: 50px;
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        margin: 1.5rem auto;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(229, 142, 38, 0.4);
        position: relative;
        z-index: 2;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 1.5rem;
        position: relative;
        display: inline-block;
    }
    
    .section-title:after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 60px;
        height: 4px;
        background: var(--accent);
        border-radius: 2px;
    }
    
    .upload-section {
        background: white;
        padding: 2.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border-left: 5px solid var(--accent);
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        padding: 1.5rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(10, 61, 98, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(10, 61, 98, 0.3);
    }
    
    .metric-number {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    .dataframe-container {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--accent), #d35400);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(229, 142, 38, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(229, 142, 38, 0.4);
        background: linear-gradient(135deg, #d35400, var(--accent));
    }
    
    .footer {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 4rem 2rem;
        text-align: center;
        margin-top: 4rem;
        font-family: 'Montserrat', sans-serif;
    }
    
    .footer h4 {
        font-family: 'Playfair Display', serif;
        color: white;
        margin-bottom: 1.5rem;
        font-size: 1.3rem;
    }
    
    .footer a {
        color: var(--gold);
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .footer a:hover {
        color: white;
        text-decoration: underline;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        margin: 1rem;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        color: var(--accent);
        margin-bottom: 1rem;
    }
    
    .feature-card h4 {
        font-family: 'Playfair Display', serif;
        color: var(--primary);
        margin-bottom: 1rem;
    }
    
    .feature-card p {
        font-family: 'Lora', serif;
        color: var(--text);
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        font-family: 'Montserrat', sans-serif;
    }
    
    .sidebar-content h3 {
        font-family: 'Playfair Display', serif;
        color: white;
        margin-bottom: 1rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #27ae60, #2ecc71);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        box-shadow: 0 5px 15px rgba(39, 174, 96, 0.2);
    }
    
    .error-message {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        box-shadow: 0 5px 15px rgba(231, 76, 60, 0.2);
    }
    
    .stTextInput>div>div>input {
        font-family: 'Lora', serif;
    }
    
    .stSelectbox>div>div>div {
        font-family: 'Lora', serif;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.5rem 1.5rem !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(10, 61, 98, 0.1) !important;
    }
    
    .stTabs [aria-selected="true"]:hover {
        background: var(--primary) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: var(--accent) !important;
    }
</style>
""", unsafe_allow_html=True)

# Luxurious Header with company branding
st.markdown("""
<div class="main-header">
    <h1>WILTON WEAVERS</h1>
    <div class="company-location">KERALA • INDIA</div>
    <div class="heritage-badge">Established 1982 • 40+ Years of Excellence</div>
    <div class="company-tagline">
        Specialists in the manufacture of Aviation Carpets & Fine Wool Broadloom.<br>
        Manufacturers of Quality Floor Coverings, we are an innovator par excellence.
    </div>
</div>
""", unsafe_allow_html=True)

# Luxurious Sidebar
with st.sidebar:
    # st.image(logo, use_column_width=True)  # Would use actual logo in production
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="font-family: 'Playfair Display', serif; color: var(--primary);">✈️ WILTON WEAVERS</h2>
        <p style="font-family: 'Lora', serif; color: var(--text);">Aviation Carpets & Fine Wool Broadloom</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-content">
        <h3>BOM Search Platform</h3>
        <p><strong>Quick Start Guide:</strong></p>
        <p>1. Upload Design Master Excel</p>
        <p>2. Upload Yarn Specifications</p>
        <p>3. Search Aviation Carpet Designs</p>
        <p>4. Analyze Quality Metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
        <h4 style="font-family: 'Playfair Display', serif; color: var(--primary); margin-bottom: 1rem;">🏭 Company Info</h4>
        <p style="font-family: 'Lora', serif; margin: 0.5rem 0;"><strong>Specialization:</strong> Aviation Carpets & Fine Wool</p>
        <p style="font-family: 'Lora', serif; margin: 0.5rem 0;"><strong>Experience:</strong> 250+ Years Collective Expertise</p>
        <p style="font-family: 'Lora', serif; margin: 0.5rem 0;"><strong>Location:</strong> Kerala, India</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload statistics
    if 'design_df' in st.session_state and 'yarn_df' in st.session_state:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
            <h4 style="font-family: 'Playfair Display', serif; color: var(--primary); margin-bottom: 1rem;">📊 Database Statistics</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Design Records", len(st.session_state.design_df), delta="Active")
        with col2:
            st.metric("Yarn Records", len(st.session_state.yarn_df), delta="Active")
        
        unique_designs = st.session_state.design_df['Design Name'].nunique() if 'Design Name' in st.session_state.design_df.columns else 0
        st.metric("Unique Designs", unique_designs, delta="Available")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <a href="https://www.wilton.in" target="_blank" style="font-family: 'Montserrat', sans-serif; color: var(--accent); text-decoration: none; font-weight: 500;">
            Visit Our Website →
        </a>
    </div>
    """, unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="upload-section">
        <h3 class="section-title">📋 Design Master Database</h3>
        <p style="font-family: 'Lora', serif; color: var(--text);">
            Upload your comprehensive design master Excel file containing aviation carpet specifications and patterns
        </p>
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
        <h3 class="section-title">🧶 Yarn Specifications</h3>
        <p style="font-family: 'Lora', serif; color: var(--text);">
            Upload your yarn database containing fine wool specifications, aviation-grade materials, and quality standards
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    yarn_file = st.file_uploader(
        "Choose Yarn Specifications Excel File",
        type=["xlsx", "xls"],
        help="Upload your yarn specifications file containing wool grades, aviation compliance, and material properties",
        key="yarn_upload"
    )

# File processing with enhanced feedback
if design_file is not None and yarn_file is not None:
    try:
        with st.spinner('🔄 Processing Aviation Carpet Database...'):
            # Load DataFrames
            design_df = pd.read_excel(design_file)
            yarn_df = pd.read_excel(yarn_file)
            
            # Store in session state
            st.session_state.design_df = design_df
            st.session_state.yarn_df = yarn_df
            
            # Clean up columns and values
            design_df.columns = design_df.columns.str.strip().str.title()
            yarn_df.columns = yarn_df.columns.str.strip().str.title()
            
            if 'Design Name' in design_df.columns:
                design_df['Design Name'] = design_df['Design Name'].astype(str).str.strip().str.upper()
            if 'Design Name' in yarn_df.columns:
                yarn_df['Design Name'] = yarn_df['Design Name'].astype(str).str.strip().str.upper()
        
        st.markdown("""
        <div class="success-message">
            ✅ Aviation Carpet Database Successfully Loaded! Ready for Professional Design Search.
        </div>
        """, unsafe_allow_html=True)
        
        # Luxurious metrics display
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
        
        # Luxurious search section
        st.markdown("""
        <div style="background: white; padding: 2.5rem; border-radius: 8px; margin: 2rem 0; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
            <h3 class="section-title">🔍 Aviation Carpet Design Search</h3>
            <p style="font-family: 'Lora', serif; color: var(--text); font-size: 1.1rem;">
                Search across our comprehensive database of aviation-grade carpet designs and fine wool specifications
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Luxurious search input
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
        
        # Enhanced search functionality
        if design_input or search_button:
            if design_input:
                design_input_clean = design_input.strip().upper()
                
                with st.spinner('🔍 Searching Aviation Carpet Database...'):
                    design_matches = design_df[design_df['Design Name'].str.contains(design_input_clean, na=False)] if 'Design Name' in design_df.columns else pd.DataFrame()
                    yarn_matches = yarn_df[yarn_df['Design Name'].str.contains(design_input_clean, na=False)] if 'Design Name' in yarn_df.columns else pd.DataFrame()
                
                # Luxurious results display
                if not design_matches.empty and not yarn_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Perfect Match Found! Design and Yarn Specifications Located in Database
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Merge data
                    merged = pd.merge(design_matches, yarn_matches, on='Design Name', how='left')
                    
                    # Luxurious results in tabs
                    tab1, tab2, tab3 = st.tabs([
                        "📊 Complete Specification", 
                        "🎨 Design Details", 
                        "🧶 Yarn & Material"
                    ])
                    
                    with tab1:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🔧 Complete Aviation Carpet Specification")
                        st.markdown("*Combined design and yarn specifications for aviation-grade floor coverings*")
                        st.dataframe(merged, use_container_width=True, height=400)
                        
                        # Export functionality
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
                        
                        # Design insights
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
                        
                        # Yarn insights
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
                    
                    # Enhanced suggestions for similar designs
                    if 'Design Name' in design_df.columns:
                        # Try broader search
                        partial_matches = design_df[design_df['Design Name'].str.contains(design_input_clean[:3], na=False)]['Design Name'].unique()[:8]
                        if len(partial_matches) > 0:
                            st.markdown("""
                            <div style="background: rgba(229, 142, 38, 0.1); padding: 1.5rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid var(--accent);">
                                <h4 style="font-family: 'Playfair Display', serif; color: var(--primary); margin-bottom: 1rem;">💡 Similar Aviation Carpet Designs Found:</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display suggestions in a nice format
                            cols = st.columns(min(4, len(partial_matches)))
                            for i, suggestion in enumerate(partial_matches):
                                with cols[i % len(cols)]:
                                    if st.button(f"🔍 {suggestion}", key=f"suggestion_{i}"):
                                        st.session_state.search_input = suggestion
                                        st.experimental_rerun()
            else:
                st.markdown("""
                <div class="error-message">
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

else:
    # Luxurious welcome section
    st.markdown("""
    <div style="background: white; padding: 4rem 2rem; border-radius: 8px; margin: 2rem 0; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
        <h2 style="font-family: 'Playfair Display', serif; color: var(--primary); margin-bottom: 1.5rem;">👋 Welcome to Wilton Weavers</h2>
        <p style="font-family: 'Lora', serif; font-size: 1.3rem; color: var(--text); margin-bottom: 3rem;">
            Specialists in the manufacture of Aviation Carpets & Fine Wool Broadloom.<br>
            Manufacturers of Quality Floor Coverings, we are an innovator par excellence.
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 3rem;">
            <div class="feature-card">
                <div class="feature-icon">✈️</div>
                <h4>Aviation Carpets</h4>
                <p>Premium aviation-grade floor coverings meeting international airline standards</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧶</div>
                <h4>Fine Wool Broadloom</h4>
                <p>Luxury fine wool broadloom carpets with superior craftsmanship</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🏭</div>
                <h4>40+ Years Experience</h4>
                <p>Established in 1982 with 250+ years of collective expertise</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h4>Advanced BOM Search</h4>
                <p>Intelligent search across design specifications and material databases</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Company heritage section
    st.markdown("""
    <div style="background: linear-gradient(rgba(10, 61, 98, 0.9), rgba(10, 61, 98, 0.95)), url('https://images.unsplash.com/photo-1602872030490-4a484a7b3ba6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        padding: 4rem 2rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h2 style="font-family: 'Playfair Display', serif; margin-bottom: 1.5rem;">Our Heritage</h2>
        <p style="font-family: 'Lora', serif; font-size: 1.2rem; max-width: 800px; margin: 0 auto 2rem;">
            Since 1982, Wilton Weavers has been crafting premium aviation carpets and fine wool broadloom, 
            combining traditional craftsmanship with modern innovation.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: center;">
            <div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 0.5rem;">40+</h3>
                <p style="font-family: 'Lora', serif;">Years of Excellence</p>
            </div>
            <div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 0.5rem;">250+</h3>
                <p style="font-family: 'Lora', serif;">Years Collective Expertise</p>
            </div>
            <div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 0.5rem;">1000+</h3>
                <p style="font-family: 'Lora', serif;">Aviation Designs</p>
            </div>
            <div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 0.5rem;">50+</h3>
                <p style="font-family: 'Lora', serif;">Global Clients</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Luxurious Footer
st.markdown("""
<div class="footer">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 3rem; text-align: left;">
        <div>
            <h4>✈️ Wilton Weavers</h4>
            <p>Aviation Carpets & Fine Wool Broadloom</p>
            <p>Kerala, India • Est. 1982</p>
            <p>Manufacturers of Quality Floor Coverings</p>
        </div>
        <div>
            <h4>🌐 Connect With Us</h4>
            <p>Website: <a href="https://www.wilton.in" target="_blank">www.wilton.in</a></p>
            <p>Email: info@wilton.in</p>
            <p>Phone: +91 484 1234567</p>
        </div>
        <div>
            <h4>🏭 Our Expertise</h4>
            <p>• Aviation Grade Carpets</p>
            <p>• Fine Wool Broadloom</p>
            <p>• Custom Design Solutions</p>
        </div>
    </div>
    
    <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 2rem;">
        <p style="margin: 0; font-family: 'Montserrat', sans-serif;">
            © 2024 <strong>Wilton Weavers</strong> - All Rights Reserved
        </p>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.8""")

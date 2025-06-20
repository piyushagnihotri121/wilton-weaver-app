import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import base64
import io
import time

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
    
    .footer-section {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: #ecf0f1;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-top: 4rem;
        font-family: 'Inter', sans-serif;
        text-align: center;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
    }
    
    .footer-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
        text-align: left;
    }
    
    .footer-section h4 {
        color: #3498db;
        margin-bottom: 1rem;
        font-family: 'Playfair Display', serif;
        font-weight: 600;
    }
    
    .footer-section p {
        margin: 0.5rem 0;
        opacity: 0.9;
    }
    
    .footer-section a {
        color: #3498db;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .footer-section a:hover {
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
    
    # Company Information
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2c3e50, #34495e); color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
        <h4 style="color: #ecf0f1; margin-bottom: 1rem;">🏭 Company Info</h4>
        <p style="margin: 0.5rem 0;"><strong>Specialization:</strong><br>Aviation Carpets & Fine Wool</p>
        <p style="margin: 0.5rem 0;"><strong>Experience:</strong><br>250+ Years Collective Expertise</p>
        <p style="margin: 0.5rem 0;"><strong>Type:</strong><br>Private Family Business</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload statistics
    if 'design_df' in st.session_state and 'yarn_df' in st.session_state:
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
    
    st.markdown("---")
    
    # Advanced features
    st.subheader("🎯 Advanced Features")
    show_analytics = st.checkbox("📈 Analytics Dashboard", value=True)
    show_export = st.checkbox("📥 Export Options", value=True)
    auto_refresh = st.checkbox("🔄 Auto-refresh Results", value=False)
    
    st.markdown("---")
    
    # Contact Information
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
        <h5 style="margin-bottom: 0.5rem;">📞 Need Support?</h5>
        <p style="margin: 0; font-size: 0.9rem;">Visit: <a href="https://www.wilton.in" target="_blank" style="color: #ffeaa7;">wilton.in</a></p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
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
        
        # Enhanced metrics display
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
        
        # Enhanced search section
        st.markdown("""
        <div class="search-container">
            <h3>🔍 Aviation Carpet Design Search</h3>
            <p style="color: #7f8c8d; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
                Search across our comprehensive database of aviation-grade carpet designs and fine wool specifications
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced search input
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
                
                # Enhanced results display
                if not design_matches.empty and not yarn_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Perfect Match Found! Design and Yarn Specifications Located in Database
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Merge data
                    merged = pd.merge(design_matches, yarn_matches, on='Design Name', how='left')
                    
                    # Enhanced results in tabs
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
                            # Enhanced export functionality
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                merged.to_excel(writer, sheet_name='Complete_Specification', index=False)
                                design_matches.to_excel(writer, sheet_name='Design_Details', index=False)
                                yarn_matches.to_excel(writer, sheet_name='Yarn_Specifications', index=False)
                            
                            st.download_button(
                                label="📥 Download Complete Specification",
                                data=buffer.getvalue(),
                                file_name=f"Wilton_Weavers_Specification_{design_input_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                help="Download complete specifications in Excel format"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tab2:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🎨 Aviation Carpet Design Details")
                        st.markdown("*Comprehensive design specifications and pattern information*")
                        
                        # Enhanced design details display
                        if not design_matches.empty:
                            st.dataframe(design_matches, use_container_width=True, height=350)
                            
                            # Design metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Design Variants", len(design_matches))
                            with col2:
                                if 'Pattern Type' in design_matches.columns:
                                    st.metric("Pattern Types", design_matches['Pattern Type'].nunique())
                            with col3:
                                if 'Quality Grade' in design_matches.columns:
                                    st.metric("Quality Grades", design_matches['Quality Grade'].nunique())
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tab3:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🧶 Yarn & Material Specifications")
                        st.markdown("*Fine wool specifications and aviation-grade material properties*")
                        
                        if not yarn_matches.empty:
                            st.dataframe(yarn_matches, use_container_width=True, height=350)
                            
                            # Yarn analytics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Yarn Specifications", len(yarn_matches))
                            with col2:
                                if 'Wool Grade' in yarn_matches.columns:
                                    st.metric("Wool Grades", yarn_matches['Wool Grade'].nunique())
                            with col3:
                                if 'Aviation Standard' in yarn_matches.columns:
                                    st.metric("Aviation Standards", yarn_matches['Aviation Standard'].nunique())
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tab4:
                        if show_analytics:
                            st.subheader("📈 Quality Analytics Dashboard")
                            
                            # Create visualizations if numeric columns exist
                            numeric_cols = merged.select_dtypes(include=['number']).columns
                            
                            if len(numeric_cols) > 0:
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    # Quality distribution chart
                                    if 'Quality Grade' in merged.columns:
                                        quality_dist = merged['Quality Grade'].value_counts()
                                        fig_quality = px.pie(
                                            values=quality_dist.values,
                                            names=quality_dist.index,
                                            title="Quality Grade Distribution",
                                            color_discrete_sequence=px.colors.qualitative.Set3
                                        )
                                        fig_quality.update_traces(textposition='inside', textinfo='percent+label')
                                        st.plotly_chart(fig_quality, use_container_width=True)
                                
                                with col2:
                                    # Yarn composition chart
                                    if 'Yarn Weight' in merged.columns:
                                        yarn_data = merged.groupby('Design Name')['Yarn Weight'].mean().reset_index()
                                        fig_yarn = px.bar(
                                            yarn_data,
                                            x='Design Name',
                                            y='Yarn Weight',
                                            title="Average Yarn Weight by Design",
                                            color='Yarn Weight',
                                            color_continuous_scale='Blues'
                                        )
                                        fig_yarn.update_layout(xaxis_title="Design Name", yaxis_title="Yarn Weight")
                                        st.plotly_chart(fig_yarn, use_container_width=True)
                                
                                # Detailed metrics table
                                st.subheader("📊 Detailed Quality Metrics")
                                if len(numeric_cols) > 0:
                                    metrics_summary = merged[numeric_cols].describe()
                                    st.dataframe(metrics_summary, use_container_width=True)
                            else:
                                st.info("📊 No numeric data available for advanced analytics visualization.")
                        else:
                            st.info("📈 Enable Analytics Dashboard in the sidebar to view quality metrics.")
                
                elif not design_matches.empty and yarn_matches.empty:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #f39c12, #e67e22); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center;">
                        ⚠️ Partial Match: Design Found but Yarn Specifications Missing
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("🎨 Available Design Information")
                    st.dataframe(design_matches, use_container_width=True)
                    
                    st.info("💡 Yarn specifications not found for this design. Please check yarn database or contact technical support.")
                
                elif design_matches.empty and not yarn_matches.empty:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #f39c12, #e67e22); color: white; padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center;">
                        ⚠️ Partial Match: Yarn Specifications Found but Design Details Missing
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("🧶 Available Yarn Information")
                    st.dataframe(yarn_matches, use_container_width=True)
                    
                    st.info("💡 Design details not found for this yarn specification. Please check design database or contact technical support.")
                
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ No Matching Records Found in Aviation Carpet Database
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Suggestion system
                    st.subheader("🔍 Search Suggestions")
                    
                    # Get available design names for suggestions
                    if 'Design Name' in design_df.columns:
                        available_designs = design_df['Design Name'].unique()[:10]  # Top 10 suggestions
                        
                        st.markdown("**Available Design Names (Sample):**")
                        for design in available_designs:
                            if pd.notna(design):
                                st.markdown(f"• {design}")
                    
                    st.info("💡 Try searching with partial names, aircraft models, or pattern types. Contact support for assistance.")
            else:
                st.warning("⚠️ Please enter a design name to search the database.")
        
        # Enhanced data preview section
        st.markdown("---")
        st.subheader("👀 Database Preview")
        
        preview_tab1, preview_tab2 = st.tabs(["📋 Design Master Preview", "🧶 Yarn Specifications Preview"])
        
        with preview_tab1:
            st.markdown("**Design Master Database Sample (First 10 Records)**")
            st.dataframe(design_df.head(10), use_container_width=True)
            
            if 'Design Name' in design_df.columns:
                st.markdown("**Available Design Names (Sample):**")
                sample_designs = design_df['Design Name'].dropna().unique()[:15]
                cols = st.columns(3)
                for i, design in enumerate(sample_designs):
                    with cols[i % 3]:
                        st.markdown(f"• {design}")
        
        with preview_tab2:
            st.markdown("**Yarn Specifications Database Sample (First 10 Records)**")
            st.dataframe(yarn_df.head(10), use_container_width=True)
            
            if 'Design Name' in yarn_df.columns:
                st.markdown("**Available Yarn Specifications (Sample):**")
                sample_yarns = yarn_df['Design Name'].dropna().unique()[:15]
                cols = st.columns(3)
                for i, yarn in enumerate(sample_yarns):
                    with cols[i % 3]:
                        st.markdown(f"• {yarn}")
        
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error Processing Files: {str(e)}
        </div>
        """, unsafe_allow_html=True)
        st.error("Please ensure your Excel files are properly formatted with the correct column names.")
        
        # Debug information
        with st.expander("🔧 Debug Information"):
            st.write("File processing error details:")
            st.write(f"Error type: {type(e).__name__}")
            st.write(f"Error message: {str(e)}")

# Welcome section when no files are uploaded
elif design_file is None or yarn_file is None:
    st.markdown("""
    <div class="welcome-section">
        <h2>🌟 Welcome to Wilton Weavers BOM Search Platform</h2>
        <p style="font-size: 1.2rem; color: #7f8c8d; margin-bottom: 2rem; position: relative; z-index: 2;">
            Your comprehensive solution for aviation carpet design and yarn specification management
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✈️</div>
            <h4>Aviation Grade Carpets</h4>
            <p>Specialized manufacturing of aviation-grade floor coverings meeting international standards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧶</div>
            <h4>Fine Wool Broadloom</h4>
            <p>Premium quality wool specifications with comprehensive material property database</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4>Advanced Analytics</h4>
            <p>Real-time quality metrics and design analysis with export capabilities</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Getting started instructions
    st.subheader("🚀 Getting Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📋 Step 1: Upload Design Master**
        - Prepare your Excel file with design specifications
        - Include columns: Design Name, Pattern Type, Quality Grade
        - Ensure aviation carpet details are complete
        """)
        
        st.markdown("""
        **📊 Step 3: Search & Analyze**
        - Use the search functionality to find specific designs
        - View comprehensive specifications and analytics
        - Export results for further processing
        """)
    
    with col2:
        st.markdown("""
        **🧶 Step 2: Upload Yarn Specifications**
        - Include yarn database with material properties
        - Specify wool grades and aviation standards
        - Maintain consistent Design Name format
        """)
        
        st.markdown("""
        **💼 Step 4: Professional Output**
        - Generate detailed BOM reports
        - Quality metrics and compliance data
        - Ready for manufacturing use
        """)

# Enhanced Footer
st.markdown("""
<div class="footer-section">
    <div class="footer-content">
        <div>
            <h4>🏭 Wilton Weavers</h4>
            <p><strong>Established:</strong> 1982</p>
            <p><strong>Specialization:</strong> Aviation Carpets & Fine Wool Broadloom</p>
            <p><strong>Location:</strong> Kerala, India</p>
            <p><strong>Experience:</strong> 40+ Years of Excellence</p>
        </div>
        
        <div>
            <h4>✈️ Aviation Division</h4>
            <p>Boeing Certified Supplier</p>
            <p>Airbus Approved Manufacturer</p>
            <p>FAA Compliant Materials</p>
            <p>International Aviation Standards</p>
        </div>
        
        <div>
            <h4>🧶 Wool Expertise</h4>
            <p>Premium Fine Wool Processing</p>
            <p>Custom Broadloom Manufacturing</p>
            <p>Quality Yarn Specifications</p>
            <p>Sustainable Material Sourcing</p>
        </div>
        
        <div>
            <h4>📞 Contact Information</h4>
            <p><strong>Website:</strong> <a href="https://www.wilton.in" target="_blank">www.wilton.in</a></p>
            <p><strong>Email:</strong> info@wilton.in</p>
            <p><strong>Support:</strong> support@wilton.in</p>
            <p><strong>Phone:</strong> +91-XXX-XXX-XXXX</p>
        </div>
    </div>
    
    <div style="text-align: center; border-top: 1px solid #4a5568; padding-top: 2rem; margin-top: 2rem;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">
            © 2024 Wilton Weavers • Aviation Carpets & Fine Wool Broadloom • Kerala, India<br>
            Powered by Advanced BOM Search Technology • Built with Streamlit
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Auto-refresh functionality
if auto_refresh and 'design_df' in st.session_state:
    time.sleep(5)  # Refresh every 5 seconds
    st.rerun()
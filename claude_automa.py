import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import base64
import io

# Set page config with enhanced styling
st.set_page_config(
    page_title="Wilton Weavers BOM Search App",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://wiltonweavers.com/help',
        'Report a bug': "https://wiltonweavers.com/bug",
        'About': "# Wilton Weavers BOM Search App\nSearch and analyze your textile designs efficiently!"
    }
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px dashed #4a90e2;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #4a90e2;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
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
    
    .success-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    .error-message {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    .dataframe-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid #eee;
    }
    
    .stSelectbox > label, .stTextInput > label {
        font-weight: 600;
        color: #333;
        font-size: 1.1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧵 Wilton Weavers</h1>
    <p>Advanced BOM Search & Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🚀 Quick Start Guide</h3>
        <p>1. Upload your Design Master Excel file</p>
        <p>2. Upload your Yarn Excel file</p>
        <p>3. Search for designs using the search box</p>
        <p>4. View detailed analytics and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # File upload statistics
    if 'design_df' in st.session_state and 'yarn_df' in st.session_state:
        st.subheader("📊 File Statistics")
        st.metric("Design Records", len(st.session_state.design_df))
        st.metric("Yarn Records", len(st.session_state.yarn_df))
        st.metric("Unique Designs", st.session_state.design_df['Design Name'].nunique() if 'Design Name' in st.session_state.design_df.columns else 0)
    
    st.markdown("---")
    
    # Additional features
    st.subheader("🎯 Advanced Features")
    show_analytics = st.checkbox("Show Analytics Dashboard", value=True)
    show_export = st.checkbox("Enable Export Options", value=True)
    auto_refresh = st.checkbox("Auto-refresh Results", value=False)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="upload-section">
        <h3>📋 Upload Design Master File</h3>
        <p>Upload your Excel file containing design information</p>
    </div>
    """, unsafe_allow_html=True)
    
    design_file = st.file_uploader(
        "Choose Design Master Excel file",
        type=["xlsx", "xls"],
        help="Upload your design master Excel file here",
        key="design_upload"
    )

with col2:
    st.markdown("""
    <div class="upload-section">
        <h3>🧶 Upload Yarn File</h3>
        <p>Upload your Excel file containing yarn information</p>
    </div>
    """, unsafe_allow_html=True)
    
    yarn_file = st.file_uploader(
        "Choose Yarn Excel file",
        type=["xlsx", "xls"],
        help="Upload your yarn Excel file here",
        key="yarn_upload"
    )

# File processing
if design_file is not None and yarn_file is not None:
    try:
        with st.spinner('🔄 Processing files...'):
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
            ✅ Files uploaded successfully! Ready to search designs.
        </div>
        """, unsafe_allow_html=True)
        
        # Display file information
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
                <div class="metric-label">Yarn Records</div>
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
                <div class="metric-label">Total Columns</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Search section
        st.markdown("""
        <div class="search-container">
            <h3>🔍 Design Search</h3>
            <p>Enter the design name to search across both files</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Search input with enhanced styling
        col1, col2 = st.columns([3, 1])
        
        with col1:
            design_input = st.text_input(
                "Design Name",
                placeholder="Enter design name to search...",
                help="Search is case-insensitive and supports partial matches",
                key="search_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
            search_button = st.button("🔍 Search", type="primary")
        
        # Search functionality
        if design_input or search_button:
            if design_input:
                design_input_clean = design_input.strip().upper()
                
                with st.spinner('🔍 Searching...'):
                    design_matches = design_df[design_df['Design Name'].str.contains(design_input_clean, na=False)] if 'Design Name' in design_df.columns else pd.DataFrame()
                    yarn_matches = yarn_df[yarn_df['Design Name'].str.contains(design_input_clean, na=False)] if 'Design Name' in yarn_df.columns else pd.DataFrame()
                
                # Results display
                if not design_matches.empty and not yarn_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Found matching records in both files!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Merge data
                    merged = pd.merge(design_matches, yarn_matches, on='Design Name', how='left')
                    
                    # Display results in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["📊 Combined View", "🎨 Design Details", "🧶 Yarn Details", "📈 Analytics"])
                    
                    with tab1:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("Combined Design & Yarn Information")
                        st.dataframe(merged, use_container_width=True, height=400)
                        
                        if show_export:
                            # Export functionality
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                merged.to_excel(writer, sheet_name='Combined_Data', index=False)
                            
                            st.download_button(
                                label="📥 Download Combined Data",
                                data=buffer.getvalue(),
                                file_name=f"combined_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tab2:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("Design Details")
                        st.dataframe(design_matches, use_container_width=True, height=400)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tab3:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("Yarn Details")
                        st.dataframe(yarn_matches, use_container_width=True, height=400)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with tab4:
                        if show_analytics:
                            st.subheader("📈 Search Analytics")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Create a simple chart showing record counts
                                fig = go.Figure(data=[
                                    go.Bar(name='Records Found', x=['Design Records', 'Yarn Records'], 
                                          y=[len(design_matches), len(yarn_matches)],
                                          marker_color=['#667eea', '#764ba2'])
                                ])
                                fig.update_layout(
                                    title="Records Found by Category",
                                    xaxis_title="Category",
                                    yaxis_title="Count",
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                # Display search statistics
                                st.metric("Total Matches", len(design_matches) + len(yarn_matches))
                                st.metric("Design Matches", len(design_matches))
                                st.metric("Yarn Matches", len(yarn_matches))
                                st.metric("Combined Records", len(merged))
                
                elif not design_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Found matches in Design file only
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.subheader("🎨 Design Details")
                    st.dataframe(design_matches, use_container_width=True, height=400)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                elif not yarn_matches.empty:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Found matches in Yarn file only
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.subheader("🧶 Yarn Details")
                    st.dataframe(yarn_matches, use_container_width=True, height=400)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                else:
                    st.markdown("""
                    <div class="error-message">
                        ❌ No matching designs found in either file
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Suggestion for similar designs
                    if 'Design Name' in design_df.columns:
                        similar_designs = design_df[design_df['Design Name'].str.contains(design_input_clean[:3], na=False)]['Design Name'].unique()[:5]
                        if len(similar_designs) > 0:
                            st.info(f"💡 Did you mean: {', '.join(similar_designs)}")
            else:
                st.warning("⚠️ Please enter a design name to search")
    
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error processing files: {str(e)}
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome message when no files are uploaded
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; margin: 2rem 0;">
        <h2>👋 Welcome to Wilton Weavers BOM Search</h2>
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
            Upload your Excel files to get started with powerful design search and analytics
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
                <h4>Design Master</h4>
                <p>Upload your design information</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧶</div>
                <h4>Yarn Details</h4>
                <p>Upload your yarn specifications</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                <h4>Smart Search</h4>
                <p>Find designs instantly</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 Wilton Weavers BOM Search App | Built with ❤️ using Streamlit</p>
    <p>For support, contact: support@wiltonweavers.com</p>
</div>
""", unsafe_allow_html=True)
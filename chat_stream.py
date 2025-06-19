# ✅ Wilton Weavers Streamlit App — Clean, Contrast-Fixed, and Polished Version

import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import io

# Set page config
st.set_page_config(
    page_title="Wilton Weavers | Aviation Carpets",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling — clean, legible, flawless contrast
st.markdown("""
    <style>
        body { background-color: #f7f7f7; }
        .main-header {
            background: linear-gradient(#072f5f, #0a3d62);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            border-bottom: 4px solid #e58e26;
        }
        .main-header h1 { font-size: 3.5rem; margin: 0; }
        .tagline { font-size: 1.2rem; margin-top: 0.8rem; }
        .metric-card {
            background: #0a3d62;
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
        }
        .metric-card h2 { font-size: 2.2rem; margin: 0; }
        .metric-card p { margin: 0.5rem 0 0 0; font-size: 0.9rem; }
        .upload-box {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #e58e26;
        }
        .footer {
            background: #0a3d62;
            color: white;
            text-align: center;
            padding: 2rem 1rem;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='main-header'>
        <h1>Wilton Weavers</h1>
        <div class='tagline'>Aviation Carpets & Fine Wool Broadloom | Kerala, India</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.title("📊 BOM Search")
    st.markdown("Upload Excel files to begin:")
    design_file = st.file_uploader("Upload Design Master", type=['xlsx'])
    yarn_file = st.file_uploader("Upload Yarn Specifications", type=['xlsx'])

# Process files if both uploaded
if design_file and yarn_file:
    design_df = pd.read_excel(design_file)
    yarn_df = pd.read_excel(yarn_file)

    # Clean columns
    design_df.columns = design_df.columns.str.strip().str.title()
    yarn_df.columns = yarn_df.columns.str.strip().str.title()

    if 'Design Name' in design_df.columns:
        design_df['Design Name'] = design_df['Design Name'].astype(str).str.upper().str.strip()
    if 'Design Name' in yarn_df.columns:
        yarn_df['Design Name'] = yarn_df['Design Name'].astype(str).str.upper().str.strip()

    # Metrics display
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div class='metric-card'><h2>{len(design_df)}</h2><p>Design Records</p></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card'><h2>{len(yarn_df)}</h2><p>Yarn Specifications</p></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-card'><h2>{design_df['Design Name'].nunique()}</h2><p>Unique Designs</p></div>", unsafe_allow_html=True)

    # Search section
    st.subheader("🔍 Search Carpet Designs")
    query = st.text_input("Enter Design Name")
    if query:
        query_clean = query.upper().strip()
        design_matches = design_df[design_df['Design Name'].str.contains(query_clean, na=False)]
        yarn_matches = yarn_df[yarn_df['Design Name'].str.contains(query_clean, na=False)]

        if not design_matches.empty:
            st.success(f"✅ {len(design_matches)} Design record(s) found.")
            st.dataframe(design_matches)

        if not yarn_matches.empty:
            st.success(f"✅ {len(yarn_matches)} Yarn specification(s) found.")
            st.dataframe(yarn_matches)

        if design_matches.empty and yarn_matches.empty:
            st.error("❌ No matches found.")
else:
    st.markdown("""
        <div class='upload-box'>
            <h4>Please upload both Design Master and Yarn Specification Excel files to proceed.</h4>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class='footer'>
        <h4>Wilton Weavers | Kerala, India</h4>
        <p>Specialists in Aviation Grade Carpets & Fine Wool Broadloom since 1982.</p>
        <p>© 2024 Wilton Weavers. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)

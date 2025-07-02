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

# Professional Aviation Carpet Manufacturing Dashboard CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600&family=Merriweather:wght@300;400;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Main Header - Aviation Carpet Heritage */
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 25%, #2563eb 50%, #3b82f6 75%, #60a5fa 100%);
        background-size: 400% 400%;
        animation: aviationGradient 12s ease infinite;
        padding: 4rem 3rem;
        border-radius: 25px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 
            0 25px 50px rgba(30, 58, 138, 0.2),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    @keyframes aviationGradient {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 25%; }
        50% { background-position: 100% 50%; }
        75% { background-position: 0% 75%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Aviation Pattern Overlay */
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs><pattern id="aviation-weave" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse"><rect fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.5" width="40" height="40"/><path d="M0,20 Q10,10 20,20 Q30,30 40,20" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/><path d="M20,0 Q30,10 20,20 Q10,30 20,40" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.04)"/></pattern></defs><rect width="200" height="200" fill="url(%23aviation-weave)"/></svg>');
        opacity: 0.6;
    }
    
    /* Company Logo Accent */
    .main-header::after {
        content: '✈️';
        position: absolute;
        top: 20px;
        right: 30px;
        font-size: 2.5rem;
        opacity: 0.7;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 4.8rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.3),
            0 0 20px rgba(255,255,255,0.2);
        letter-spacing: -2px;
        position: relative;
        z-index: 3;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .company-location {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1rem 0;
        color: #e0e7ff;
        letter-spacing: 3px;
        text-transform: uppercase;
        position: relative;
        z-index: 3;
    }
    
    .company-location::before {
        content: '🌴';
        margin-right: 10px;
    }
    
    .company-location::after {
        content: '🌴';
        margin-left: 10px;
    }
    
    .company-tagline {
        font-family: 'Merriweather', serif;
        font-size: 1.4rem;
        font-weight: 300;
        margin: 2rem auto 0;
        max-width: 900px;
        line-height: 1.7;
        color: #cbd5e1;
        font-style: italic;
        position: relative;
        z-index: 3;
    }
    
    .heritage-badge {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #991b1b 100%);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        margin: 1.5rem auto;
        display: inline-block;
        box-shadow: 
            0 6px 20px rgba(220, 38, 38, 0.4),
            0 0 0 1px rgba(255,255,255,0.1);
        position: relative;
        z-index: 3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .aviation-badge {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-left: 1rem;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Professional Section Containers */
    .upload-section, .search-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.8);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    /* Carpet Weave Pattern for Sections */
    .upload-section::before, .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, 
            #1e40af 0%, 
            #dc2626 25%, 
            #f59e0b 50%, 
            #059669 75%, 
            #1e40af 100%);
        border-radius: 20px 20px 0 0;
    }
    
    .upload-section::after, .search-container::after {
        content: '';
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 60px;
        height: 60px;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="mini-weave" x="0" y="0" width="10" height="10" patternUnits="userSpaceOnUse"><rect fill="none" stroke="rgba(30,64,175,0.1)" stroke-width="0.5" width="10" height="10"/><circle cx="5" cy="5" r="1" fill="rgba(30,64,175,0.08)"/></pattern></defs><rect width="100" height="100" fill="url(%23mini-weave)"/></svg>');
        opacity: 0.3;
        border-radius: 10px;
    }
    
    .upload-section:hover, .search-container:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.2);
    }
    
    .upload-section h3, .search-container h3 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    .upload-section h3::after, .search-container h3::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #1e40af, #dc2626);
        border-radius: 2px;
    }
    
    /* Enhanced Metric Cards - Professional Aviation Style */
    .metric-card {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 50%, #1e293b 100%);
        padding: 2.5rem 2rem;
        border-radius: 18px;
        color: white;
        text-align: center;
        margin: 0.8rem;
        box-shadow: 
            0 15px 35px rgba(30, 64, 175, 0.25),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #3b82f6, #ef4444, #f59e0b, #10b981);
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover::before {
        opacity: 0.8;
        animation: borderRotate 2s linear infinite;
    }
    
    @keyframes borderRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .metric-card::after {
        content: '📊';
        position: absolute;
        top: 15px;
        right: 15px;
        font-size: 1.5rem;
        opacity: 0.6;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 
            0 25px 50px rgba(30, 64, 175, 0.35),
            0 0 50px rgba(30, 64, 175, 0.2);
    }
    
    .metric-number {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        display: block;
        margin-bottom: 0.8rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Professional Status Messages */
    .success-message {
        background: linear-gradient(135deg, #059669 0%, #047857 50%, #065f46 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 18px;
        margin: 2rem 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 
            0 12px 30px rgba(5, 150, 105, 0.3),
            0 0 0 1px rgba(255,255,255,0.1);
        animation: slideInSuccess 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
    }
    
    .success-message::before {
        content: '✅';
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 2rem;
        background: rgba(255,255,255,0.2);
        padding: 8px;
        border-radius: 50%;
    }
    
    @keyframes slideInSuccess {
        0% { transform: translateY(-30px) scale(0.9); opacity: 0; }
        100% { transform: translateY(0) scale(1); opacity: 1; }
    }
    
    .error-message {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #991b1b 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 18px;
        margin: 2rem 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 
            0 12px 30px rgba(220, 38, 38, 0.3),
            0 0 0 1px rgba(255,255,255,0.1);
        position: relative;
    }
    
    .error-message::before {
        content: '⚠️';
        position: absolute;
        top: -10px;
        right: 20px;
        font-size: 2rem;
        background: rgba(255,255,255,0.2);
        padding: 8px;
        border-radius: 50%;
    }
    
    /* Professional Data Display */
    .dataframe-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.2),
            inset 0 1px 0 rgba(255,255,255,0.8);
        margin: 2rem 0;
        border: 1px solid rgba(226, 232, 240, 0.8);
        position: relative;
    }
    
    .dataframe-container::before {
        content: '📋';
        position: absolute;
        top: -12px;
        left: 25px;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        padding: 8px 12px;
        border-radius: 50%;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
    }
    
    /* Sidebar Professional Styling */
    .sidebar-content {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 
            0 12px 30px rgba(30, 64, 175, 0.3),
            0 0 0 1px rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="sidebar-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><rect fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.5" width="20" height="20"/><circle cx="10" cy="10" r="1" fill="rgba(255,255,255,0.03)"/></pattern></defs><rect width="100" height="100" fill="url(%23sidebar-pattern)"/></svg>');
        opacity: 0.4;
    }
    
    .sidebar-content h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 2;
    }
    
    /* Welcome Section - Heritage Inspired */
    .welcome-section {
        text-align: center;
        padding: 5rem 3rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
        border-radius: 25px;
        margin: 3rem 0;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .welcome-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs><pattern id="welcome-weave" x="0" y="0" width="50" height="50" patternUnits="userSpaceOnUse"><rect fill="none" stroke="rgba(30,64,175,0.06)" stroke-width="1" width="50" height="50"/><path d="M0,25 Q12.5,12.5 25,25 Q37.5,37.5 50,25" fill="none" stroke="rgba(30,64,175,0.04)" stroke-width="1.5"/><path d="M25,0 Q37.5,12.5 25,25 Q12.5,37.5 25,50" fill="none" stroke="rgba(30,64,175,0.04)" stroke-width="1.5"/><circle cx="25" cy="25" r="3" fill="rgba(30,64,175,0.03)"/></pattern></defs><rect width="200" height="200" fill="url(%23welcome-weave)"/></svg>');
        opacity: 0.7;
    }
    
    .welcome-section h2 {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 2;
    }
    
    /* Feature Cards - Aviation Industry Style */
    .feature-card {
        text-align: center;
        padding: 2.5rem 2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 1.5rem;
        position: relative;
        z-index: 2;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .feature-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 0 50px rgba(30, 64, 175, 0.1);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .feature-card h4 {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 1rem;
    }
    
    /* Professional Footer */
    .footer {
        text-align: center;
        padding: 4rem 3rem;
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
        margin-top: 5rem;
        border-radius: 25px 25px 0 0;
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e40af, #dc2626, #f59e0b, #059669);
    }
    
    .footer a {
        color: #60a5fa;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .footer a:hover {
        color: #93c5fd;
        text-decoration: underline;
    }
    
    /* Enhanced Form Controls */
    .stSelectbox > label, .stTextInput > label {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #1e40af;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 50%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 1rem 3rem;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 8px 25px rgba(30, 64, 175, 0.3),
            0 0 0 1px rgba(255,255,255,0.1);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 
            0 15px 40px rgba(30, 64, 175, 0.4),
            0 0 30px rgba(30, 64, 175, 0.2);
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 50%, #2563eb 100%);
    }
    
    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 0.8rem;
        box-shadow: 
            0 8px 25px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        border-radius: 15px;
        color: #1e40af;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 64, 175, 0.1);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        border-radius: 10px;
        border: 2px solid #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 3rem;
        }
        
        .main-header {
            padding: 2.5rem 1.5rem;
        }
        
        .upload-section, .search-container {
            padding: 2rem 1.5rem;
        }
        
        .feature-card {
            margin: 1rem 0.5rem;
        }
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
                            # Use the robust color extraction function if available
                            # Otherwise, split by all common delimiters and clean
                            text = str(row[col]).upper()
                            for delimiter in [',', ';', '/', '|', '-', '+', '&']:
                                text = text.replace(delimiter, ',')
                            color_parts = [c.strip().replace(' ', '') for c in text.split(',') if c.strip()]
                            row_colors.extend([c for c in color_parts if len(c) > 1])
                    
                    # Remove duplicates and normalize
                    row_colors = list(set(row_colors))
                    
                    # Check color matching based on match type
                    if match_type == "All Colors (AND)":
                        # Strict: Only designs that use exactly the selected colors (no more, no less)
                        normalized_row_colors = sorted([c.upper() for c in row_colors])
                        normalized_selected_colors = sorted([c.upper().replace(' ', '') for c in selected_colors])
                        if normalized_row_colors == normalized_selected_colors:
                            design_color_matches = pd.concat([design_color_matches, row.to_frame().T], ignore_index=True)
                    else:
                        # Any selected color must be present (OR logic)
                        if any(selected_color.replace(' ', '').upper() in [c.upper() for c in row_colors] for selected_color in selected_colors):
                            design_color_matches = pd.concat([design_color_matches, row.to_frame().T], ignore_index=True)
                
                # Find matching yarn data
                yarn_color_matches = pd.DataFrame()
                if (st.session_state.yarn_df is not None and 
                    not design_color_matches.empty and 
                    'Design Name' in design_color_matches.columns):
                    
                    design_names = design_color_matches['Design Name'].unique()
                    yarn_color_matches = st.session_state.yarn_df[
                        st.session_state.yarn_df['Design Name'].isin(design_names)
                    ] if 'Design Name' in st.session_state.yarn_df.columns else pd.DataFrame()
                
                # Display results
                if not design_color_matches.empty:
                    st.success(f"Found {len(design_color_matches)} designs matching your color criteria:")
                    st.dataframe(design_color_matches)
                    
                    if not yarn_color_matches.empty:
                        st.info(f"Related yarn information ({len(yarn_color_matches)} entries):")
                        st.dataframe(yarn_color_matches)
                    
                    # Show metrics and tabs for results
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


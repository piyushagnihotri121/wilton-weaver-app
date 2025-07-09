# Final rama_4.py code with all requested features

import streamlit as st
import pandas as pd
import re
import io
from typing import List, Dict

st.set_page_config(page_title="Wilton Carpet Design Filter", layout="wide")
st.title("🧶 Wilton Carpet Design Smart Filter System")

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

def extract_frame_colors_from_yarn(yarn_lines: List[str]) -> str:
    """
    Custom logic: Only use WOOL BBs, ignore CN if BB exists
    """
    wool_bb_lines = []
    seen_yarns = set()

    for line in yarn_lines:
        line = line.strip()
        if not line.startswith("WOOL"):
            continue

        base = re.sub(r'-[A-Z]{2}$', '', line)
        suffix = line.split('-')[-1]

        if suffix == 'CN' and base + '-BB' in yarn_lines:
            continue  # Skip CN if BB exists

        if suffix == 'BB':
            color_match = re.search(r'WOOL\s+(.+?)-DW-', line)
            if color_match:
                color = color_match.group(1).strip().upper()
                wool_bb_lines.append(color)

    return ' - '.join(wool_bb_lines) if wool_bb_lines else ""

def get_framewise_color_column(df: pd.DataFrame, yarn_df: pd.DataFrame) -> pd.DataFrame:
    frame_colors = []
    for design in df['Design Name']:
        yarn_rows = yarn_df[yarn_df['Design Name'] == design]
        lines = []
        for desc in yarn_rows['Yarn Description']:
            lines.extend(str(desc).split('\n'))
        frame_color = extract_frame_colors_from_yarn(lines)
        frame_colors.append(frame_color)
    df['Frame-wise Color'] = frame_colors
    return df

def get_available_weft_heads(df: pd.DataFrame) -> List[str]:
    col = next((c for c in df.columns if 'weft' in c.lower() and 'head' in c.lower()), None)
    return sorted(df[col].dropna().unique()) if col else []

# --- File Upload ---
design_file = st.file_uploader("Upload Design Excel File", type=["xlsx"])
yarn_file = st.file_uploader("Upload Yarn Description Excel File", type=["xlsx"])

if design_file and yarn_file:
    design_df = pd.read_excel(design_file)
    yarn_df = pd.read_excel(yarn_file)

    # Standardize column names
    design_df.columns = design_df.columns.str.strip().str.title()
    yarn_df.columns = yarn_df.columns.str.strip().str.title()

    # Clean Design Name
    if 'Design Name' in design_df.columns:
        design_df['Design Name'] = design_df['Design Name'].astype(str).str.strip().str.upper()
    if 'Design Name' in yarn_df.columns:
        yarn_df['Design Name'] = yarn_df['Design Name'].astype(str).str.strip().str.upper()

    # --- Filters ---
    color_col = next((col for col in design_df.columns if 'color' in col.lower()), None)
    construction_col = next((col for col in design_df.columns if 'construction' in col.lower()), None)
    frame_col = next((col for col in design_df.columns if 'frame' in col.lower()), None)
    weft_col = next((col for col in design_df.columns if 'weft' in col.lower() and 'head' in col.lower()), None)

    unique_colors = sorted(set(design_df[color_col].dropna().astype(str).str.upper().tolist())) if color_col else []
    unique_constructions = sorted(set(design_df[construction_col].dropna())) if construction_col else []
    unique_frames = sorted(set(design_df[frame_col].dropna())) if frame_col else []
    unique_wefts = get_available_weft_heads(design_df)

    st.sidebar.subheader("🔍 Apply Filters")
    selected_colors = st.sidebar.multiselect("Select Color(s)", unique_colors)
    match_type = st.sidebar.radio("Match Type", ["All Colors (AND)", "Any Color (OR)"])
    selected_construction = st.sidebar.selectbox("Construction", ["Any"] + unique_constructions)
    selected_frame = st.sidebar.selectbox("No. of Frames", ["Any"] + unique_frames)
    selected_weft = st.sidebar.selectbox("Weft Head", ["Any"] + unique_wefts)

    filtered_df = design_df.copy()

    # Filter logic
    if selected_colors and color_col:
        def match_colors(row):
            row_colors = extract_colors_from_text(str(row[color_col]))
            if match_type == "All Colors (AND)":
                return all(color in row_colors for color in selected_colors)
            else:
                return any(color in row_colors for color in selected_colors)
        mask = filtered_df.apply(match_colors, axis=1)
        filtered_df = filtered_df[mask]

    if selected_construction != "Any" and construction_col:
        filtered_df = filtered_df[filtered_df[construction_col] == selected_construction]

    if selected_frame != "Any" and frame_col:
        filtered_df = filtered_df[filtered_df[frame_col] == selected_frame]

    if selected_weft != "Any" and weft_col:
        filtered_df = filtered_df[filtered_df[weft_col] == selected_weft]

    # Add Frame-wise Color Column
    filtered_df = get_framewise_color_column(filtered_df, yarn_df)

    st.subheader("📋 Filtered Carpet Designs")
    st.dataframe(filtered_df[['Design Name', 'Frame-wise Color']], use_container_width=True)

    st.success(f"Found {len(filtered_df)} matching designs.")

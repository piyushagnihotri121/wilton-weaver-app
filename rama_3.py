import streamlit as st
import pandas as pd
import re

def extract_frame_colors_from_yarn_description(yarn_desc: str) -> str:
    """
    Extract frame-wise colors from yarn description.
    Logic:
    - Remove entries ending with 'CN' if a corresponding 'BB' or 'BM' exists for the same base.
    - Only keep 'BB' or 'BM' entries that start with 'WOOL'.
    - Extract color between "WOOL " and "-DW-".
    - Return as ' ; ' separated string.
    """
    if pd.isna(yarn_desc) or not yarn_desc:
        return ""
    lines = [line.strip() for line in str(yarn_desc).split('\n') if line.strip()]
    # Group by base (everything before last - and suffix)
    base_map = {}
    for line in lines:
        # Find the suffix (BB, BM, CN, etc.)
        m = re.match(r"(.+)-([A-Z]{2,})$", line)
        if m:
            base, suffix = m.group(1), m.group(2)
            base_map.setdefault(base, set()).add(suffix)
    # Now, filter lines: remove CN if BB or BM exists for same base
    filtered_lines = []
    for line in lines:
        m = re.match(r"(.+)-([A-Z]{2,})$", line)
        if m:
            base, suffix = m.group(1), m.group(2)
            if suffix == "CN" and ("BB" in base_map.get(base, set()) or "BM" in base_map.get(base, set())):
                continue
            filtered_lines.append(line)
        else:
            filtered_lines.append(line)
    # Only keep 'WOOL ... -BB' or 'WOOL ... -BM'
    frame_lines = [l for l in filtered_lines if (l.startswith("WOOL") and (l.endswith("-BB") or l.endswith("-BM")))]
    # Extract color between "WOOL " and "-DW-"
    frame_colors = []
    for entry in frame_lines:
        match = re.search(r'WOOL\s+(.+?)-DW-', entry)
        if match:
            color = match.group(1).strip()
            frame_colors.append(color)
    return ' ; '.join(frame_colors) if frame_colors else ""

# Streamlit app
st.title("Wilton Weavers | Aviation Carpets & Fine Wool Broadloom")

st.write("Upload your Design Master and Yarn Specification Excel files:")

design_file = st.file_uploader("Design Master Excel", type=["xlsx", "xls"], key="design_upload")
yarn_file = st.file_uploader("Yarn Specifications Excel", type=["xlsx", "xls"], key="yarn_upload")

if design_file and yarn_file:
    try:
        design_df = pd.read_excel(design_file)
        yarn_df = pd.read_excel(yarn_file)

        # Clean column names
        design_df.columns = design_df.columns.str.strip().str.title()
        yarn_df.columns = yarn_df.columns.str.strip().str.title()

        # Find yarn description column
        yarn_desc_col = None
        for col in yarn_df.columns:
            if 'yarn' in col.lower() and 'description' in col.lower():
                yarn_desc_col = col
                break

        # Add 'Frame Wise Colours' column
        if yarn_desc_col:
            yarn_df['Frame Wise Colours'] = yarn_df[yarn_desc_col].apply(extract_frame_colors_from_yarn_description)
        else:
            yarn_df['Frame Wise Colours'] = ""

        st.success("Files loaded successfully!")

        st.subheader("Yarn Specifications with Frame Wise Colours")
        st.dataframe(yarn_df[['Design Name', 'Frame Wise Colours'] + [c for c in yarn_df.columns if c not in ['Design Name', 'Frame Wise Colours']]].head(20), use_container_width=True)

        # Merge frame wise colours into design_df for display
        if 'Design Name' in design_df.columns and 'Design Name' in yarn_df.columns:
            design_df['Design Name'] = design_df['Design Name'].astype(str).str.strip().str.upper()
            yarn_df['Design Name'] = yarn_df['Design Name'].astype(str).str.strip().str.upper()
            frame_color_map = yarn_df.set_index('Design Name')['Frame Wise Colours'].to_dict()
            design_df['Frame Wise Colours'] = design_df['Design Name'].map(frame_color_map)
            st.subheader("Design Master with Frame Wise Colours")
            st.dataframe(design_df[['Design Name', 'Frame Wise Colours'] + [c for c in design_df.columns if c not in ['Design Name', 'Frame Wise Colours']]].head(20), use_container_width=True)
        else:
            st.warning("Design Name column missing in one of the files.")

    except Exception as e:
        st.error(f"Error processing files: {e}")

else:
    st.info("Please upload both Design Master and Yarn Specifications Excel files to proceed.")

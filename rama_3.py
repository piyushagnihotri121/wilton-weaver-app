import streamlit as st
import pandas as pd
import io
import re
from datetime import datetime

st.set_page_config(
    page_title="Wilton Weavers | Aviation Carpets & Fine Wool Broadloom | Kerala, India",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("✈️ Wilton Weavers - Aviation Carpets & Fine Wool Broadloom")
st.markdown("#### Multi-Filter Design Search with Frame-wise Colour Extraction")

st.markdown("""
Upload your **Design Master Excel** and **Yarn Specification Excel** files below.  
You can then filter by **Colours**, **Construction**, **Weft Head**, and **No. of Frames**.  
For each design, you'll also see a column for **Frame-wise Colour** (e.g. `COTTON WHITE - COTTON WHITE - MINT`).
""")

# --- File Uploads ---
col1, col2 = st.columns(2)
with col1:
    design_file = st.file_uploader("📋 Upload Design Master Excel", type=["xlsx", "xls"], key="design_upload")
with col2:
    yarn_file = st.file_uploader("🧶 Upload Yarn Specification Excel", type=["xlsx", "xls"], key="yarn_upload")

# --- Helper Functions ---

def extract_framewise_colours(yarn_df, design_name):
    """
    For a given design, extract the frame-wise colour string as per the business logic.
    """
    # Filter yarn rows for this design
    rows = yarn_df[yarn_df['Design Name'].astype(str).str.upper() == design_name.upper()]
    if rows.empty:
        return ""
    # Get all yarn descriptions for this design
    yarn_desc_col = None
    for col in rows.columns:
        if 'yarn' in col.lower() and 'desc' in col.lower():
            yarn_desc_col = col
            break
    if not yarn_desc_col:
        # Try fallback: first column with 'desc'
        for col in rows.columns:
            if 'desc' in col.lower():
                yarn_desc_col = col
                break
    if not yarn_desc_col:
        return ""
    yarn_descs = rows[yarn_desc_col].dropna().astype(str).tolist()
    # Remove duplicates, strip whitespace
    yarn_descs = [desc.strip() for desc in yarn_descs if desc.strip()]
    # Group by base yarn (ignoring BB/CN at end)
    base_to_endings = {}
    for desc in yarn_descs:
        # Find ending (BB/CN/other)
        m = re.match(r"^(.*?)(?:-([A-Z]{2,3}))?$", desc)
        if m:
            base = m.group(1).strip()
            ending = m.group(2) if m.group(2) else ""
            if base not in base_to_endings:
                base_to_endings[base] = set()
            base_to_endings[base].add(ending)
    # Now, for each yarn, ignore CN if BB exists for same base
    filtered_descs = []
    for base, endings in base_to_endings.items():
        if "BB" in endings:
            filtered_descs.extend([f"{base}-BB"] * list(endings).count("BB"))
        elif "CN" in endings:
            filtered_descs.extend([f"{base}-CN"] * list(endings).count("CN"))
        else:
            # If neither BB nor CN, just add base
            filtered_descs.extend([base])
    # Now, for frame-wise, only keep those ending with BB (or CN if only CN exists)
    framewise_descs = []
    for desc in filtered_descs:
        if desc.endswith("-BB"):
            framewise_descs.append(desc)
    # If no -BB, use -CN
    if not framewise_descs:
        for desc in filtered_descs:
            if desc.endswith("-CN"):
                framewise_descs.append(desc)
    # If still empty, fallback to all filtered_descs
    if not framewise_descs:
        framewise_descs = filtered_descs
    # Now, extract the colour name from each framewise_desc
    # Heuristic: take the last word before -DW or -[number] or -BB/-CN
    frame_colours = []
    for desc in framewise_descs:
        # Remove trailing -BB/-CN
        desc_main = re.sub(r'-BB$|-CN$', '', desc)
        # Try to extract colour: look for last word before -DW or -[number] or -X or -BM etc.
        # e.g. "WOOL COTTON WHITE-DW-4.20/3-BB" -> "COTTON WHITE"
        #      "WOOL MINT-DW-8.33/2 X 3-BB" -> "MINT"
        # Remove "WOOL", "COTTON", "PP", "JUTE", "POLYESTER", etc. (common material prefixes)
        material_prefixes = [
            "WOOL", "COTTON", "PP", "JUTE", "POLYESTER", "CHEMICAL", "EVA", "LATEX", "THICKENER"
        ]
        # Remove all material prefixes
        desc_main = re.sub(r'\b(?:' + '|'.join(material_prefixes) + r')\b', '', desc_main, flags=re.IGNORECASE)
        # Remove numbers, dashes, slashes, X, BM, etc.
        desc_main = re.sub(r'[-/XBM0-9\.]+', ' ', desc_main, flags=re.IGNORECASE)
        # Remove extra spaces
        desc_main = re.sub(r'\s+', ' ', desc_main).strip()
        # Take last 1 or 2 words as colour
        words = desc_main.split()
        if len(words) >= 2:
            colour = " ".join(words[-2:]).upper()
        elif words:
            colour = words[-1].upper()
        else:
            colour = desc.upper()
        frame_colours.append(colour)
    # Join with " - "
    return " - ".join(frame_colours)

def get_unique_values(df, col_keywords):
    """
    Get unique values from columns whose name contains any of the col_keywords.
    """
    if df is None:
        return []
    cols = [col for col in df.columns if any(k in col.lower() for k in col_keywords)]
    vals = []
    for col in cols:
        vals.extend(df[col].dropna().astype(str).str.strip().unique())
    return sorted(list(set([v for v in vals if v and v != 'NAN'])))

# --- Main Logic ---
if design_file is not None and yarn_file is not None:
    try:
        design_df = pd.read_excel(design_file)
        yarn_df = pd.read_excel(yarn_file)
        # Standardize column names
        design_df.columns = design_df.columns.str.strip().str.title()
        yarn_df.columns = yarn_df.columns.str.strip().str.title()
        # Ensure 'Design Name' exists
        if 'Design Name' not in design_df.columns or 'Design Name' not in yarn_df.columns:
            st.error("Both files must have a 'Design Name' column.")
        else:
            # --- Filter UI ---
            available_colours = get_unique_values(design_df, ['color', 'colour', 'shade', 'dye'])
            available_constructions = get_unique_values(design_df, ['construction'])
            available_frames = get_unique_values(design_df, ['frame'])
            available_weft_heads = get_unique_values(design_df, ['weft head', 'wefthead', 'weft'])
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                selected_colours = st.multiselect("🎨 Colours", available_colours)
            with col2:
                selected_construction = st.selectbox("🏗️ Construction", ["Any"] + available_constructions)
            with col3:
                selected_frames = st.selectbox("🖼️ No. of Frames", ["Any"] + available_frames)
            with col4:
                selected_weft_head = st.selectbox("🧵 Weft Head", ["Any"] + available_weft_heads)
            search_btn = st.button("🔍 Search Designs")
            # --- Filtering ---
            filtered_df = design_df.copy()
            if selected_colours:
                # Check if any colour column contains all selected colours
                def row_has_colours(row):
                    row_colours = []
                    for col in design_df.columns:
                        if any(k in col.lower() for k in ['color', 'colour', 'shade', 'dye']):
                            val = str(row[col]).upper() if pd.notna(row[col]) else ""
                            for sep in [',', ';', '/', '|', '+', '&', '-']:
                                val = val.replace(sep, ',')
                            row_colours.extend([c.strip() for c in val.split(',') if c.strip()])
                    return all(col.upper() in [c.upper() for c in row_colours] for col in selected_colours)
                filtered_df = filtered_df[filtered_df.apply(row_has_colours, axis=1)]
            if selected_construction and selected_construction != "Any":
                construction_col = next((col for col in design_df.columns if 'construction' in col.lower()), None)
                if construction_col:
                    filtered_df = filtered_df[filtered_df[construction_col].astype(str).str.strip() == selected_construction]
            if selected_frames and selected_frames != "Any":
                frames_col = next((col for col in design_df.columns if 'frame' in col.lower()), None)
                if frames_col:
                    filtered_df = filtered_df[filtered_df[frames_col].astype(str).str.strip() == selected_frames]
            if selected_weft_head and selected_weft_head != "Any":
                weft_col = next((col for col in design_df.columns if 'weft head' in col.lower() or 'wefthead' in col.lower() or 'weft' in col.lower()), None)
                if weft_col:
                    filtered_df = filtered_df[filtered_df[weft_col].astype(str).str.strip() == selected_weft_head]
            # --- Add Frame-wise Colour Column ---
            if not filtered_df.empty:
                st.success(f"Found {len(filtered_df)} matching designs.")
                # Add Frame-wise Colour column
                filtered_df = filtered_df.copy()
                filtered_df['Frame-wise Colour'] = filtered_df['Design Name'].apply(
                    lambda dn: extract_framewise_colours(yarn_df, dn)
                )
                # Show only relevant columns for clarity
                show_cols = ['Design Name']
                # Try to add main columns if present
                for k in ['Construction', 'No. Of Frames', 'Weft Head']:
                    c = next((col for col in filtered_df.columns if k.lower() in col.lower()), None)
                    if c and c not in show_cols:
                        show_cols.append(c)
                # Add all colour columns
                show_cols += [col for col in filtered_df.columns if any(k in col.lower() for k in ['color', 'colour', 'shade', 'dye'])]
                # Add frame-wise colour at end
                if 'Frame-wise Colour' not in show_cols:
                    show_cols.append('Frame-wise Colour')
                # Remove duplicates, keep order
                seen = set()
                show_cols = [x for x in show_cols if not (x in seen or seen.add(x))]
                st.dataframe(filtered_df[show_cols], use_container_width=True)
                # Download option
                buffer = io.BytesIO()
                filtered_df[show_cols].to_excel(buffer, index=False)
                st.download_button(
                    label="📥 Download Filtered Designs (with Frame-wise Colour)",
                    data=buffer.getvalue(),
                    file_name=f"WiltonWeavers_Filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                # Show example output
                st.markdown("##### Example Output:")
                st.markdown("""
| Design Name | Frame-wise Colour |
|-------------|------------------|
| SERA-SAGE   | COTTON WHITE - COTTON WHITE - MINT |
                """)
            else:
                st.warning("No matching designs found for the selected filters.")
    except Exception as e:
        st.error(f"Error processing files: {e}")
else:
    st.info("Please upload both the Design Master and Yarn Specification Excel files to begin.")

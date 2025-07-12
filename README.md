# 🧶 Carpet Design Automation Tool — Wilton Weavers

A Streamlit-based web application that simplifies and automates the selection of compatible **carpet designs**, **colors**, **yarn types**, **structures**, **looms**, **weft heads**, and **frame-wise color assignments** using uploaded Excel files.

---

## 📌 Project Objective

At Wilton Weavers, design selection for carpets was done **manually** using large design specification sheets and individual expertise (e.g., by Ma’am Saijama). This process:

- Was **time-consuming**
- Required **manual cross-checking**
- Became difficult when **experienced persons were unavailable**
- Lacked a **central searchable system**

This app solves that by enabling anyone to get **automated**, **searchable**, and **filterable** access to design data using simple filters.

---

## 🔧 Features

✅ Upload your **Design Info** and **Yarn Info** Excel files  
✅ Filter by:
- 🎨 Colors (multi-color with AND/OR logic)
- 🧵 No. of Frames
- 🏗️ Construction
- 🧷 Weft Head

✅ Automatically detect:
- Matching designs using selected filters
- 🧠 **Frame-wise Color Assignment** using yarn description logic
- 🧹 Ignore unnecessary yarns like chemicals, non-WOOL types, and CN duplicates
- 📤 Export results as downloadable Excel

---

## 🧠 Logic Highlights

- **Colors are extracted** from yarn description or color columns, even if written with separators like `/`, `+`, `,`, `-`, `&`.
- **Yarn Descriptions** ending with `-CN` are ignored if a `-BB` or `-BM` version exists for the same yarn.
- Only **WOOL** yarns with `-BB` endings are used to extract **frame-wise colors**.
- Total BB entries = number of frames → Each BB color represents a frame color.


---

## 🚀 How to Use

1. Go to 👉 [https://wilton-weaver-app-aydujmzmfp6r43wxp34fgk.streamlit.app]
2. Upload:
   - `Design_Master_Database excel file` (design structure, frame info, etc.)
   - `Yarn_Specifications excel file` (yarn descriptions)
3. Apply filters from the sidebar
4. View results with:
   - Full design details
   - Frame-wise colors
   - Yarn details
5. Download filtered results as Excel

---

## 📂 Files Needed

- ✅ `Design_Master_Database.xlsx`  
- ✅ `Yarn_Specifications.xlsx`

These can be updated as per new projects or batches.

---

## 🛠️ Technologies Used

- **Python 3.11**
- **Streamlit** for web UI
- **Pandas** for Excel data handling
- **Regex** for extracting patterns
- **OpenPyXL** for Excel export

---

## 🧑‍💻 Developed By

**Piyush Agnihotri**  
*Data Science Intern, Wilton Weavers*  
Project Duration: `May 2025 – July 2025`  
Role: Complete development of carpet design automation system — from raw data to deployment.

---

## 📎 Optional Enhancements (Future Scope)

- 🔍 Add search by **Design Name** directly
- 📸 Show matching **carpet images** (if dataset available)
- 📊 Usage Analytics (design frequency, popular combinations)
- 🔒 Admin access control for data uploads

---



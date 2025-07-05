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

 

#!/usr/bin/env python3

# Aviation Carpet Manufacturing Dashboard
# Save this as a .py file and run it to serve the HTML

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aviation Carpet Manufacturing Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        *,
        *::before,
        *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            font-size: 62.5%;
        }

        body {
            font-family: 'Open Sans', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, hsl(270, 50%, 15%), hsl(290, 60%, 25%), hsl(240, 50%, 20%));
            min-height: 100vh;
            color: hsl(0, 0%, 95%);
            overflow-x: hidden;
        }

        .dashboard {
            background: hsl(270, 50%, 8%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 50px hsla(270, 30%, 5%, 0.8);
        }

        /* Header Section */
        .header {
            height: 8rem;
            background: linear-gradient(135deg, hsl(270, 50%, 12%), hsl(270, 50%, 15%));
            display: flex;
            align-items: center;
            padding: 0 3rem;
            box-shadow: 0 4px 20px hsla(270, 30%, 3%, 0.5);
            border-bottom: 1px solid hsla(270, 50%, 25%, 0.3);
        }

        .header__logo {
            font-size: 2.4rem;
            font-weight: 800;
            color: hsl(220, 80%, 70%);
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-right: 4rem;
        }

        .header__search {
            flex-grow: 1;
            max-width: 50rem;
            position: relative;
        }

        .header__search-input {
            width: 100%;
            padding: 1.5rem 2rem;
            background: hsl(270, 50%, 18%);
            border: 2px solid hsl(270, 50%, 25%);
            border-radius: 12px;
            color: hsl(0, 0%, 90%);
            font-size: 1.4rem;
            outline: none;
            transition: all 0.3s ease;
        }

        .header__search-input:focus {
            border-color: hsl(220, 80%, 60%);
            box-shadow: 0 0 0 3px hsla(220, 80%, 60%, 0.2);
        }

        .header__search-input::placeholder {
            color: hsl(0, 0%, 60%);
        }

        .header__nav {
            display: flex;
            align-items: center;
            gap: 3rem;
        }

        .header__button {
            background: linear-gradient(135deg, hsl(220, 80%, 60%), hsl(220, 80%, 70%));
            color: white;
            border: none;
            padding: 1.2rem 2.4rem;
            border-radius: 8px;
            font-size: 1.3rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .header__button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px hsla(220, 80%, 60%, 0.4);
        }

        .header__link {
            color: hsl(0, 0%, 80%);
            text-decoration: none;
            font-size: 1.4rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .header__link:hover {
            color: hsl(220, 80%, 70%);
        }

        /* Main Content Area */
        .main {
            flex: 1;
            display: flex;
            background: linear-gradient(135deg, 
                hsla(270, 50%, 8%, 0.9), 
                hsla(270, 50%, 12%, 0.8) 30%, 
                hsla(270, 50%, 6%, 0.9) 70%);
        }

        /* Sidebar */
        .sidebar {
            width: 10rem;
            background: linear-gradient(180deg, hsl(270, 50%, 10%), hsl(270, 50%, 8%));
            border-right: 1px solid hsla(270, 50%, 25%, 0.3);
            padding: 3rem 0;
            box-shadow: 2px 0 15px hsla(270, 30%, 3%, 0.4);
        }

        .sidebar__icon {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
            color: hsl(0, 0%, 60%);
        }

        .sidebar__icon:hover {
            color: hsl(220, 80%, 70%);
            background: hsla(220, 80%, 60%, 0.1);
        }

        .sidebar__icon.active {
            color: hsl(220, 80%, 70%);
            background: hsla(220, 80%, 60%, 0.2);
        }

        .sidebar__icon svg {
            width: 2.4rem;
            height: 2.4rem;
            margin-bottom: 0.8rem;
        }

        .sidebar__label {
            font-size: 1rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Content Area */
        .content {
            flex: 1;
            padding: 4rem;
            overflow-y: auto;
        }

        .content__header {
            margin-bottom: 4rem;
        }

        .content__title {
            font-size: 4rem;
            font-weight: 300;
            color: hsl(0, 0%, 95%);
            margin-bottom: 1rem;
        }

        .content__subtitle {
            font-size: 1.6rem;
            color: hsl(0, 0%, 70%);
            font-weight: 400;
        }

        /* Cards Section */
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(30rem, 1fr));
            gap: 3rem;
            margin-bottom: 4rem;
        }

        .card {
            background: linear-gradient(135deg, hsl(270, 50%, 12%), hsl(270, 50%, 15%));
            border-radius: 16px;
            padding: 3rem;
            box-shadow: 0 10px 30px hsla(270, 30%, 3%, 0.4);
            border: 1px solid hsla(270, 50%, 25%, 0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, hsl(220, 80%, 60%), hsl(280, 60%, 60%));
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 50px hsla(270, 30%, 3%, 0.6);
        }

        .card__header {
            display: flex;
            align-items: center;
            margin-bottom: 2rem;
        }

        .card__icon {
            width: 4rem;
            height: 4rem;
            background: linear-gradient(135deg, hsl(220, 80%, 60%), hsl(220, 80%, 70%));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 1.5rem;
        }

        .card__icon svg {
            width: 2rem;
            height: 2rem;
            color: white;
        }

        .card__title {
            font-size: 1.8rem;
            font-weight: 600;
            color: hsl(0, 0%, 95%);
        }

        .card__value {
            font-size: 3.2rem;
            font-weight: 700;
            color: hsl(220, 80%, 70%);
            margin-bottom: 1rem;
        }

        .card__description {
            font-size: 1.4rem;
            color: hsl(0, 0%, 70%);
            line-height: 1.6;
        }

        /* Production Timeline */
        .timeline {
            background: linear-gradient(135deg, hsl(270, 50%, 12%), hsl(270, 50%, 15%));
            border-radius: 16px;
            padding: 3rem;
            margin-bottom: 4rem;
            border: 1px solid hsla(270, 50%, 25%, 0.3);
            box-shadow: 0 10px 30px hsla(270, 30%, 3%, 0.4);
        }

        .timeline__header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 3rem;
        }

        .timeline__title {
            font-size: 2.4rem;
            font-weight: 600;
            color: hsl(0, 0%, 95%);
        }

        .timeline__filter {
            display: flex;
            gap: 1rem;
        }

        .timeline__filter-btn {
            padding: 0.8rem 1.6rem;
            background: hsl(270, 50%, 18%);
            border: 1px solid hsl(270, 50%, 25%);
            border-radius: 8px;
            color: hsl(0, 0%, 80%);
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1.2rem;
        }

        .timeline__filter-btn:hover,
        .timeline__filter-btn.active {
            background: hsl(220, 80%, 60%);
            color: white;
            border-color: hsl(220, 80%, 60%);
        }

        .timeline__list {
            position: relative;
            padding-left: 3rem;
        }

        .timeline__list::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, hsl(220, 80%, 60%), hsl(280, 60%, 60%));
        }

        .timeline__item {
            position: relative;
            margin-bottom: 3rem;
            padding-left: 2rem;
        }

        .timeline__item::before {
            content: '';
            position: absolute;
            left: -2.5rem;
            top: 0.5rem;
            width: 8px;
            height: 8px;
            background: hsl(220, 80%, 60%);
            border-radius: 50%;
            box-shadow: 0 0 0 3px hsl(270, 50%, 12%);
        }

        .timeline__item-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }

        .timeline__item-time {
            font-size: 1.2rem;
            color: hsl(0, 0%, 60%);
            margin-right: 2rem;
        }

        .timeline__item-title {
            font-size: 1.6rem;
            font-weight: 600;
            color: hsl(0, 0%, 95%);
        }

        .timeline__item-description {
            font-size: 1.4rem;
            color: hsl(0, 0%, 70%);
            line-height: 1.6;
        }

        /* Status Badges */
        .status {
            display: inline-block;
            padding: 0.4rem 1.2rem;
            border-radius: 20px;
            font-size: 1.1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .status--active {
            background: hsla(120, 60%, 50%, 0.2);
            color: hsl(120, 60%, 70%);
        }

        .status--pending {
            background: hsla(45, 90%, 50%, 0.2);
            color: hsl(45, 90%, 70%);
        }

        .status--completed {
            background: hsla(220, 80%, 60%, 0.2);
            color: hsl(220, 80%, 70%);
        }

        /* Responsive Design */
        @media (max-width: 1200px) {
            .cards {
                grid-template-columns: repeat(auto-fit, minmax(25rem, 1fr));
            }
        }

        @media (max-width: 768px) {
            html {
                font-size: 55%;
            }
            
            .header {
                flex-direction: column;
                height: auto;
                padding: 2rem;
                gap: 2rem;
            }
            
            .header__nav {
                flex-direction: column;
                gap: 1rem;
            }
            
            .main {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: auto;
                display: flex;
                justify-content: center;
                gap: 2rem;
                padding: 2rem;
            }
            
            .sidebar__icon {
                flex-direction: row;
                padding: 1rem;
            }
            
            .content {
                padding: 2rem;
            }
            
            .content__title {
                font-size: 3rem;
            }
            
            .cards {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <!-- Header -->
        <header class="header">
            <div class="header__logo">AVICRAFT</div>
            <div class="header__search">
                <input type="text" class="header__search-input" placeholder="Search production data, orders, analytics...">
            </div>
            <nav class="header__nav">
                <button class="header__button">Pro Dashboard</button>
                <a href="#" class="header__link">Reports</a>
                <a href="#" class="header__link">Analytics</a>
                <a href="#" class="header__link">Settings</a>
            </nav>
        </header>

        <!-- Main Content -->
        <main class="main">
            <!-- Sidebar -->
            <aside class="sidebar">
                <div class="sidebar__icon active">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                    </svg>
                    <span class="sidebar__label">Dashboard</span>
                </div>
                <div class="sidebar__icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                    </svg>
                    <span class="sidebar__label">Analytics</span>
                </div>
                <div class="sidebar__icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 6h-2.18c.11-.31.18-.65.18-1a2.996 2.996 0 0 0-5.5-1.65l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1z"/>
                    </svg>
                    <span class="sidebar__label">Production</span>
                </div>
                <div class="sidebar__icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    <span class="sidebar__label">Quality</span>
                </div>
            </aside>

            <!-- Content Area -->
            <div class="content">
                <div class="content__header">
                    <h1 class="content__title">Aviation Carpet Manufacturing</h1>
                    <p class="content__subtitle">Premium quality carpets for commercial aviation - Real-time production monitoring</p>
                </div>

                <!-- Metrics Cards -->
                <div class="cards">
                    <div class="card">
                        <div class="card__header">
                            <div class="card__icon">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
                                </svg>
                            </div>
                            <h3 class="card__title">Daily Production</h3>
                        </div>
                        <div class="card__value">1,247</div>
                        <p class="card__description">Square meters of premium aviation carpet produced today. <span class="status status--active">+12% from yesterday</span></p>
                    </div>

                    <div class="card">
                        <div class="card__header">
                            <div class="card__icon">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                                </svg>
                            </div>
                            <h3 class="card__title">Quality Score</h3>
                        </div>
                        <div class="card__value">99.7%</div>
                        <p class="card__description">Current quality control rating for all production lines. <span class="status status--completed">Exceeding targets</span></p>
                    </div>

                    <div class="card">
                        <div class="card__header">
                            <div class="card__icon">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M20 6h-2.18c.11-.31.18-.65.18-1a2.996 2.996 0 0 0-5.5-1.65l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1z"/>
                                </svg>
                            </div>
                            <h3 class="card__title">Active Orders</h3>
                        </div>
                        <div class="card__value">23</div>
                        <p class="card__description">Current orders in production across all manufacturing lines. <span class="status status--pending">4 urgent</span></p>
                    </div>
                </div>

                <!-- Production Timeline -->
                <div class="timeline">
                    <div class="timeline__header">
                        <h2 class="timeline__title">Production Timeline</h2>
                        <div class="timeline__filter">
                            <button class="timeline__filter-btn active">Today</button>
                            <button class="timeline__filter-btn">This Week</button>
                            <button class="timeline__filter-btn">This Month</button>
                        </div>
                    </div>
                    <div class="timeline__list">
                        <div class="timeline__item">
                            <div class="timeline__item-header">
                                <span class="timeline__item-time">14:32</span>
                                <h4 class="timeline__item-title">Boeing 787 Carpet Set - Completed</h4>
                            </div>
                            <p class="timeline__item-description">Premium class cabin carpet installation set for Boeing 787 successfully completed quality inspection. Ready for shipment to assembly facility.</p>
                        </div>
                        <div class="timeline__item">
                            <div class="timeline__item-header">
                                <span class="timeline__item-time">12:15</span>
                                <h4 class="timeline__item-title">Airbus A350 Order - In Progress</h4>
                            </div>
                            <p class="timeline__item-description">Business class carpet production for Airbus A350 fleet. Currently 67% complete with expected delivery in 2 days.</p>
                        </div>
                        <div class="timeline__item">
                            <div class="timeline__item-header">
                                <span class="timeline__item-time">09:45</span>
                                <h4 class="timeline__item-title">Quality Control Inspection</h4>
                            </div>
                            <p class="timeline__item-description">Routine quality control inspection completed for production line 3. All standards met with 99.8% pass rate.</p>
                        </div>
                        <div class="timeline__item">
                            <div class="timeline__item-header">
                                <span class="timeline__item-time">08:30</span>
                                <h4 class="timeline__item-title">Material Delivery</h4>
                            </div>
                            <p class="timeline__item-description">Premium aviation-grade materials delivered and inspected. Fire-resistant fibers and specialized backing materials now in inventory.</p>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Add interactivity
        document.addEventListener('DOMContentLoaded', function() {
            // Sidebar navigation
            const sidebarIcons = document.querySelectorAll('.sidebar__icon');
            sidebarIcons.forEach(icon => {
                icon.addEventListener('click', function() {
                    sidebarIcons.forEach(i => i.classList.remove('active'));
                    this.classList.add('active');
                });
            });

            // Timeline filter buttons
            const filterBtns = document.querySelectorAll('.timeline__filter-btn');
            filterBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    filterBtns.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                });
            });

            // Add some animation to cards
            const cards = document.querySelectorAll('.card');
            cards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.1}s`;
            });

            // Search functionality
            const searchInput = document.querySelector('.header__search-input');
            searchInput.addEventListener('focus', function() {
                this.style.transform = 'scale(1.02)';
            });
            searchInput.addEventListener('blur', function() {
                this.style.transform = 'scale(1)';
            });
        });
    </script>
</body>
</html>"""

def create_html_file():
    """Create the HTML file from the string content"""
    with open('aviation_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Dashboard HTML file created successfully!")

def serve_dashboard():
    """Simple HTTP server to serve the dashboard"""
    import http.server
    import socketserver
    import webbrowser
    import os
    
    PORT = 8000
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Dashboard running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        webbrowser.open(f'http://localhost:{PORT}/aviation_dashboard.html')
        httpd.serve_forever()

if __name__ == "__main__":
    create_html_file()
    serve_dashboard()

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

def get_available_colors(df: pd.DataFrame) -> List[str]:
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
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for sheet_name, df in data_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    return buffer.getvalue()

def display_metrics_cards(metrics: Dict[str, int]):
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

# --- Multi-Filter Section (Color, Construction, No. of Frames) ---
st.markdown("""
<div class="color-filter-section">
    <h3>🎨 Multi-Filter Design Search</h3>
    <p style="color: #7f8c8d; font-family: 'Inter', sans-serif; font-size: 1.1rem;">
        Select multiple colors, construction, and number of frames to find aviation carpet designs that match your criteria.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Filter Option Preparation ---
available_colors = []
available_constructions = []
available_frames = []

if st.session_state.design_df is not None:
    df = st.session_state.design_df
    # Colors
    color_columns = [col for col in df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
    for col in color_columns:
        colors_in_col = df[col].dropna().astype(str).str.split(',|;|/|\\|').explode().str.strip().str.upper().unique()
        available_colors.extend(colors_in_col)
    available_colors = sorted(list(set([color for color in available_colors if color and color != 'NAN'])))
    # Construction
    construction_col = None
    for col in df.columns:
        if 'construction' in col.lower():
            construction_col = col
            break
    if construction_col:
        available_constructions = sorted(df[construction_col].dropna().astype(str).str.strip().unique())
    # No. of Frames
    frames_col = None
    for col in df.columns:
        if 'frame' in col.lower():
            frames_col = col
            break
    if frames_col:
        available_frames = sorted(df[frames_col].dropna().astype(str).str.strip().unique())

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
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
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
    match_type = st.radio(
        "Match Type:",
        options=["All Colors (AND)", "Any Color (OR)"],
        help="All Colors: Design must contain ALL selected colors\nAny Color: Design must contain AT LEAST ONE selected color",
        key="match_type"
    )
    color_search_button = st.button("🔍 SEARCH BY FILTERS", type="secondary")

# --- Display Selected Filters ---
if selected_colors or (selected_construction and selected_construction != "Any") or (selected_frames and selected_frames != "Any"):
    st.markdown("**Selected Filters:**")
    chips = ""
    for color in selected_colors:
        chips += f'<span class="color-chip">{color}</span> '
    if selected_construction and selected_construction != "Any":
        chips += f'<span class="color-chip" style="background:#1e40af;">{selected_construction}</span> '
    if selected_frames and selected_frames != "Any":
        chips += f'<span class="color-chip" style="background:#8b4513;">{selected_frames} Frames</span> '
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

# --- Multi-Filter Search (Color, Construction, No. of Frames) ---
if (selected_colors or (selected_construction and selected_construction != "Any") or (selected_frames and selected_frames != "Any")) and (color_search_button or auto_refresh):
    if st.session_state.design_df is not None:
        df = st.session_state.design_df
        with st.spinner('🎨 Searching designs by selected filters...'):
            # Prepare color columns
            color_columns = [col for col in df.columns if any(word in col.lower() for word in ['color', 'colour', 'shade', 'dye'])]
            construction_col = None
            for col in df.columns:
                if 'construction' in col.lower():
                    construction_col = col
                    break
            frames_col = None
            for col in df.columns:
                if 'frame' in col.lower():
                    frames_col = col
                    break

            matches = []
            for idx, row in df.iterrows():
                # --- Color Matching ---
                row_colors = []
                for col in color_columns:
                    if pd.notna(row[col]):
                        text = str(row[col]).upper()
                        for delimiter in [',', ';', '/', '|', '-', '+', '&']:
                            text = text.replace(delimiter, ',')
                        color_parts = [c.strip().replace(' ', '') for c in text.split(',') if c.strip()]
                        row_colors.extend([c for c in color_parts if len(c) > 1])
                row_colors = list(set(row_colors))
                color_pass = True
                if selected_colors:
                    if match_type == "All Colors (AND)":
                        normalized_row_colors = sorted([c.upper() for c in row_colors])
                        normalized_selected_colors = sorted([c.upper().replace(' ', '') for c in selected_colors])
                        color_pass = normalized_row_colors == normalized_selected_colors
                    else:
                        color_pass = any(selected_color.replace(' ', '').upper() in [c.upper() for c in row_colors] for selected_color in selected_colors)
                # --- Construction Matching ---
                construction_pass = True
                if selected_construction and selected_construction != "Any" and construction_col:
                    construction_pass = str(row[construction_col]).strip() == selected_construction
                # --- Frames Matching ---
                frames_pass = True
                if selected_frames and selected_frames != "Any" and frames_col:
                    frames_pass = str(row[frames_col]).strip() == selected_frames
                # --- Final Decision ---
                if color_pass and construction_pass and frames_pass:
                    matches.append(idx)
            filtered_df = df.iloc[matches].copy() if matches else pd.DataFrame()

            # Find matching yarn data
            yarn_matches = pd.DataFrame()
            if (st.session_state.yarn_df is not None and 
                not filtered_df.empty and 
                'Design Name' in filtered_df.columns):
                design_names = filtered_df['Design Name'].unique()
                yarn_matches = st.session_state.yarn_df[
                    st.session_state.yarn_df['Design Name'].isin(design_names)
                ] if 'Design Name' in st.session_state.yarn_df.columns else pd.DataFrame()

            # --- Display Results ---
            if not filtered_df.empty:
                st.success(f"Found {len(filtered_df)} designs matching your filter criteria:")
                st.dataframe(filtered_df)
                if not yarn_matches.empty:
                    st.info(f"Related yarn information ({len(yarn_matches)} entries):")
                    st.dataframe(yarn_matches)
                # Show metrics and tabs for results
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="metric-number">{len(filtered_df)}</span>
                        <div class="metric-label">Matching Designs</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    unique_designs = filtered_df['Design Name'].nunique() if 'Design Name' in filtered_df.columns else len(filtered_df)
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
                    yarn_count = len(yarn_matches) if not yarn_matches.empty else 0
                    st.markdown(f"""
                    <div class="metric-card">
                        <span class="metric-number">{yarn_count}</span>
                        <div class="metric-label">Yarn Matches</div>
                    </div>
                    """, unsafe_allow_html=True)
                if not yarn_matches.empty:
                    merged_color = pd.merge(filtered_df, yarn_matches, on='Design Name', how='left')
                    tab1, tab2, tab3 = st.tabs([
                        "🎨 Filtered Designs", 
                        "🧶 Corresponding Yarn Specs", 
                        "📊 Complete Filtered Specification"
                    ])
                    with tab1:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🎨 Designs Matching Your Filters")
                        st.markdown(f"*Found {len(filtered_df)} designs using your filter criteria*")
                        st.dataframe(filtered_df, use_container_width=True, height=400)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with tab2:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("🧶 Yarn Specifications for Filtered Designs")
                        st.dataframe(yarn_matches, use_container_width=True, height=400)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with tab3:
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.subheader("📊 Complete Specification (Design + Yarn)")
                        st.dataframe(merged_color, use_container_width=True, height=400)
                        if show_export:
                            buffer = io.BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                merged_color.to_excel(writer, sheet_name='Filtered_Complete', index=False)
                            st.download_button(
                                label="📥 Download Filtered Specification",
                                data=buffer.getvalue(),
                                file_name=f"WiltonWeavers_Filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-message">
                    ❌ No Matching Aviation Carpet Designs Found for Selected Filters
                </div>
                """, unsafe_allow_html=True)

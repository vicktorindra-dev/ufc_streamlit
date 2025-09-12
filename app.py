import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly
import plotly.graph_objects as go
import plotly.express as px

# Set page configurations
st.set_page_config(
    page_title="UFC Fight Analysis Dashboard",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to add blurred background image
def add_blurred_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url('https://wallpapercave.com/wp/wp2797705.jpg');
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }
        
        /* Create a pseudo-element for the blur effect */
        .stApp::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: inherit;
            filter: blur(8px);
            z-index: -1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to add blurred background
add_blurred_bg()

# Set modern style for plots
plt.style.use('default')
sns.set_palette("viridis")

# Custom styling for modern transparent plots with white text
def set_modern_style(ax, transparent=True):
    """Apply a modern style to matplotlib axes with optional transparency and white text"""
    if transparent:
        ax.set_facecolor('none')
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_alpha(0.3)
    ax.spines['bottom'].set_alpha(0.3)
    
    # Change text color to white
    ax.tick_params(colors='white', which='both')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    
    # Change legend text color to white
    legend = ax.get_legend()
    if legend:
        for text in legend.get_texts():
            text.set_color('white')
    
    return ax

# Load data
@st.cache_data
def load_data():
    # Ganti dengan path file Excel Anda
    url = "https://github.com/vicktorindra-dev/ufc_streamlit/raw/refs/heads/main/data.xlsx"
    #df = pd.read_excel(r"C:\Users\Indra\Desktop\ufc\data3.xlsx")
    df = pd.read_excel(url)
    return df
    
df = load_data()

# Custom CSS for styling with blurred background
st.markdown("""
<style>
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header styling */
    .css-18e3th9 {
        padding-top: 0;
        padding-bottom: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        backdrop-filter: blur(5px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Metric card styling */
       .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        color: white;
        backdrop-filter: blur(5px);
        transition: transform 0.3s ease;
    }         
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    
    .stMetric label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stMetric div {
        color: white !important;
        font-weight: 700 !important;
        font-size: 24px !important;
    }
    /* Different colors for each metric card */

    div[data-testid="metric-container"]:nth-child(1) {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%) !important;
    }
    
    div[data-testid="metric-container"]:nth-child(2) {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%) !important;
    }
    
    div[data-testid="metric-container"]:nth-child(3) {
        background: linear-gradient(135deg, #ffd166 0%, #ffb347 100%) !important;
    }
    
    /* Style for metric values */
    .stMetric [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: white !important;
    }
    
    
    /* Style for metric labels */
    .stMetric [data-testid="stMetricLabel"] {
        opacity: 0.9;
        font-size: 14px !important;
        color: white !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px 8px 0 0;
        padding: 10px 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        color: #333;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-bottom: 3px solid #ff6b6b !important;
        color: #ff6b6b !important;
        font-weight: 600;
    }
        .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 107, 107, 0.1) !important;
        color: #ff6b6b !important;
    }
    
    /* Warna indikator tab aktif */
    .stTabs [data-baseweb="tab"]:focus {
        color: #ff6b6b !important;
    }
            
    
    /* Title styling */
    h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    
    /* Text styling */
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Footer styling */
    .css-1q1n0ol {
        color: white;
    }
    
    /* Mengubah warna teks dalam chart menjadi putih */
    .stChart text {
        fill: white !important;
        color: white !important;
    }
    
    /* Mengubah warna teks dalam tabel menjadi putih */
    .stDataFrame td, .stDataFrame th, .stDataFrame span, .stDataFrame div {
        color: white !important;
    }
    
    /* Mengubah warna latar belakang tabel untuk kontras yang lebih baik */
    .stDataFrame [data-testid="stDataFrame"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Mengubah warna header tabel */
    .stDataFrame thead tr th {
        background-color: rgba(255, 107, 107, 0.7) !important;
        color: white !important;
    }
    
    /* Mengubah warna baris tabel */
    .stDataFrame tbody tr {
        background-color: rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Efek hover pada baris tabel */
    .stDataFrame tbody tr:hover {
        background-color: rgba(255, 107, 107, 0.2) !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🥊 UFC Fight Analysis Dashboard")
st.markdown("""
This dashboard provides insights into UFC fights based on historical data.
Explore fight statistics, trends, and performance metrics.
"""                                 )

# Sidebar filters
st.sidebar.header("Filters")
events = st.sidebar.multiselect(
    "Select Events",
    options=df['event_name'].unique(),
    default=df['event_name'].unique()
)

divisions = st.sidebar.multiselect(
    "Select Divisions",
    options=df['division'].unique(),
    default=df['division'].unique()
)

df['date'] = pd.to_datetime(df['date'], errors='coerce')
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min().date(), df['date'].max().date()),
    min_value=df['date'].min().date(),
    max_value=df['date'].max().date()
)

# Filter data based on selections
start_date = pd.to_datetime(date_range[0])
end_date   = pd.to_datetime(date_range[1])
filtered_df = df[
    (df['event_name'].isin(events)) &
    (df['division'].isin(divisions)) &
    (df['date'] >= start_date) &
    (df['date'] <= end_date)
]

# Main content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Fights", len(filtered_df))
    
with col2:
    win_method = filtered_df['method'].value_counts()
    most_common = win_method.index[0] if len(win_method) > 0 else "N/A"
    st.metric("Most Common Finish", most_common)
    
with col3:
    unique_fighters = len(pd.concat([filtered_df['r_name'], filtered_df['b_name']]).unique())
    st.metric("Unique Fighters", unique_fighters)
    
with col4:
    ko_percentage = (filtered_df['method'].str.contains('KO/TKO').sum() / len(filtered_df)) * 100
    st.metric("KO/TKO Percentage", f"{ko_percentage:.1f}%")

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Fight Overview", "Winning Factor", "Additional Information", 
    "Fighter Comparison", "Custom Analysis", "Data Overview"
])

with tab1:
    st.header("Fight Overview")
    
    # Tambahkan CSS untuk menyelaraskan chart
    st.markdown("""
    <style>
    .chart-container {
        display: flex;
        flex-direction: column;
        height: 500px; /* Tinggi tetap untuk semua container chart */
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Winner bar chart
        st.subheader("The Winner")
        winner_counts = filtered_df['winner'].value_counts().head(5)

        # Gunakan container dengan class khusus
        with st.container():
            fig, ax = plt.subplots(figsize=(10, 5))  # Kurangi tinggi sedikit
            fig.patch.set_facecolor('none')

            bars = ax.bar(range(len(winner_counts)), winner_counts.values, 
                        color=plt.cm.viridis(np.linspace(0, 1, len(winner_counts))),
                        alpha=0.8, edgecolor='white', linewidth=1)

            ax.set_xticks(range(len(winner_counts)))
            ax.set_xticklabels(winner_counts.index, rotation=45, ha='right')
            ax.set_xlabel('Fighters', color='white')
            ax.set_ylabel('Number of Wins', color='white')
            ax.set_title('Top 5 Winners', fontweight='bold', color='white')

            for bar, value in zip(bars, winner_counts.values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value}', ha='center', va='bottom', color='white', fontweight='bold')

            ax = set_modern_style(ax)
            st.pyplot(fig, use_container_width=True)

    with col2:
        st.subheader("Winners by KO/TKO")
                
        ko_tko_fights = filtered_df[filtered_df['method'].str.contains('KO/TKO', na=False)]
        ko_tko_winners = ko_tko_fights['winner'].value_counts().head(5)
                        
        if len(ko_tko_winners) > 0:
            fig2, ax2 = plt.subplots(figsize=(10, 6))  # Tinggi sama dengan col1
            fig2.patch.set_facecolor('none')
            
            # Buat donut chart yang lebih compact
            colors = plt.cm.viridis(np.linspace(0, 1, len(ko_tko_winners)))
            wedges, texts, autotexts = ax2.pie(
                ko_tko_winners.values,
                labels=None,  # Hilangkan label di pie, gunakan legend
                autopct=lambda p: f'{int(p * sum(ko_tko_winners.values) / 100)}',
                colors=colors,
                startangle=90,
                textprops={'fontsize': 9},
                wedgeprops=dict(width=0.5),  # Buat donut chart
                pctdistance=0.75
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Tambahkan legend di luar chart
            ax2.legend(wedges, ko_tko_winners.index,
                    title="Fighters",
                    loc="center left",
                    bbox_to_anchor=(1, 0, 0.5, 1),
                    frameon=False,
                    labelcolor='white')
            
            # Tambahkan total di tengah
            total_ko = sum(ko_tko_winners.values)
            ax2.text(0, 0, f'Total\n{total_ko}', 
                    ha='center', va='center', 
                    fontsize=12, fontweight='bold', color='white')
            
            ax2.set_title('Top 5 KO/TKO Winners', fontweight='bold', color='white', pad=20)
            ax2.axis('equal')
            
            ax2 = set_modern_style(ax2)
            st.pyplot(fig2, use_container_width=True)
        else:
            st.info("No KO/TKO wins found in the selected filters.")
    
    # Baris kedua pada tab1
    st.subheader("Number of Fights by Year")
    # Pastikan kolom date dalam format datetime
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])
    # Ekstrak tahun dari tanggal
    filtered_df['year'] = filtered_df['date'].dt.year
    # Hitung jumlah pertandingan per tahun
    fights_by_year = filtered_df['year'].value_counts().sort_index()

    # Buat time series chart
    fig, ax = plt.subplots(figsize=(18, 6))
    fig.patch.set_facecolor('none')

    # Plot garis time series
    ax.plot(fights_by_year.index, fights_by_year.values, 
            marker='o', linewidth=3, markersize=8, color='#ff6b6b')

    # Isi area di bawah garis
    ax.fill_between(fights_by_year.index, fights_by_year.values, 
                    alpha=0.3, color='#ff6b6b')

    # Atur label dan judul
    ax.set_xlabel('Year', color='white', fontweight='bold')
    ax.set_ylabel('Number of Fights', color='white', fontweight='bold')


    # Tambahkan grid untuk readability
    ax.grid(True, alpha=0.3, linestyle='--')

    # Tambahkan nilai di setiap titik data
    for year, count in zip(fights_by_year.index, fights_by_year.values):
        ax.text(year, count + 0.5, f'{count}', 
                ha='center', va='bottom', color='white', fontweight='bold', fontsize=10)

    # Atur batas x-axis untuk menghindari titik data terpotong
    ax.set_xlim(fights_by_year.index.min() - 0.5, fights_by_year.index.max() + 0.5)

    # Atur style modern dengan teks putih
    ax = set_modern_style(ax)
    st.pyplot(fig, use_container_width=True)


    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Top 8 Most Active Divisions Since Beginning")
        
        # Pastikan kolom date dalam format datetime
        filtered_df['date'] = pd.to_datetime(filtered_df['date'])
        
        # Filter data dari tahun 2010 ke atas
        df_since_2010 = filtered_df[(filtered_df['date'].dt.year >= 1994) & (filtered_df['date'].dt.year <= 2024)].copy()
        
        # Hitung total jumlah pertandingan per division sejak 2010
        division_totals = df_since_2010['division'].value_counts()
        
        # Ambil top 8 divisions berdasarkan total pertandingan
        top_8_divisions = division_totals.head(5).index
        
        # Ekstrak tahun dari tanggal
        df_since_2010['year'] = df_since_2010['date'].dt.year
        
        # Hitung jumlah pertandingan per division per tahun
        division_growth = df_since_2010.groupby(['year', 'division']).size().unstack(fill_value=0)
        
        # Filter hanya top 8 divisions
        division_growth_top8 = division_growth[top_8_divisions]
        
        # Plot time series untuk top 8 divisions
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('none')
        
        # Warna untuk setiap division
        colors = plt.cm.viridis(np.linspace(0, 1, len(division_growth_top8.columns)))
        
        # Plot setiap division
        for i, division in enumerate(division_growth_top8.columns):
            ax.plot(division_growth_top8.index, division_growth_top8[division], 
                    marker='o', linewidth=3, markersize=6, 
                    color=colors[i], label=f'{division}')
        
        # Atur label dan judul
        ax.set_xlabel('Year', color='white', fontweight='bold', fontsize=12)
        ax.set_ylabel('Number of Fights', color='white', fontweight='bold', fontsize=12)

        
        # Tambahkan legend di luar chart
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1), frameon=False, labelcolor='white', fontsize=9)
        
        # Tambahkan grid
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Format x-axis untuk menampilkan tahun sebagai integer
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        
        # Atur batas y-axis untuk memberikan sedikit ruang di atas
        max_value = division_growth_top8.max().max()
        ax.set_ylim(0, max_value * 1.1)
        
        # Atur style modern dengan teks putih
        ax = set_modern_style(ax)
        st.pyplot(fig, use_container_width=True)


    with col4:
        st.subheader("Top 8 Most Active Fighters Since Beginning")
        
        # Gabungkan semua nama fighter dari red corner dan blue corner
        all_fighters = pd.concat([filtered_df['r_name'], filtered_df['b_name']])
        
        # Hitung total jumlah pertandingan per fighter
        fighter_totals = all_fighters.value_counts().head(8)
        
        # Buat bar chart horizontal
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('none')
        
        # Buat bar chart horizontal
        bars = ax.barh(range(len(fighter_totals)), fighter_totals.values,
                    color=plt.cm.viridis(np.linspace(0, 1, len(fighter_totals))),
                    alpha=0.8, edgecolor='white', linewidth=1)
        
        # Atur label dan judul
        ax.set_yticks(range(len(fighter_totals)))
        ax.set_yticklabels(fighter_totals.index)
        ax.set_xlabel('Total Number of Fights', color='white', fontweight='bold', fontsize=12)
        ax.set_ylabel('Fighters', color='white', fontweight='bold', fontsize=12)
        ax.set_title('Top 8 Most Active Fighters', fontweight='bold', color='white', fontsize=16, pad=20)
        
        # Tambahkan nilai di ujung setiap bar
        for i, (bar, value) in enumerate(zip(bars, fighter_totals.values)):
            ax.text(value + 0.1, i, f'{value}', va='center', color='white', fontweight='bold', fontsize=10)
        
        # Membalik urutan agar yang tertinggi di atas
        ax.invert_yaxis()
        
        # Tambahkan grid
        ax.grid(True, alpha=0.3, linestyle='--', axis='x')
        
        # Atur style modern dengan teks putih
        ax = set_modern_style(ax)
        st.pyplot(fig, use_container_width=True)



with tab2:
    st.header("Winning Factor")
       
    st.subheader("Distribution of Fighter Stances")
        
        # Gabungkan semua stance dari red corner dan blue corner
    all_stances = pd.concat([filtered_df['r_stance'], filtered_df['b_stance']])
        
        # Hitung frekuensi setiap stance
    stance_counts = all_stances.value_counts()
        
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    fig1.patch.set_facecolor('none')
        
        # Buat bar chart untuk stance
    bars = ax1.bar(range(len(stance_counts)), stance_counts.values,
                    color=plt.cm.viridis(np.linspace(0, 1, len(stance_counts))),
                    alpha=0.8, edgecolor='white', linewidth=1)
        
        # Atur label dan judul
    ax1.set_xticks(range(len(stance_counts)))
    ax1.set_xticklabels(stance_counts.index, rotation=45, ha='right')
    ax1.set_xlabel('Fighting Stance', color='white', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Frequency', color='white', fontweight='bold', fontsize=12)
    ax1.set_title('Distribution of Fighter Stances', fontweight='bold', color='white', fontsize=12, pad=20)
        
        # Tambahkan nilai di atas setiap bar
    for bar, value in zip(bars, stance_counts.values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value}', ha='center', va='bottom', color='white', fontweight='bold', fontsize=10)
        
        # Atur style modern dengan teks putih
    ax1 = set_modern_style(ax1)
    st.pyplot(fig1, use_container_width=True)


    col1, col2 = st.columns(2)
    
    with col1:

        st.subheader("Strike Part Accuracy by Winner")
        
        # Buat kolom baru untuk accuracy pemenang
        winner_accuracy_data = []
        
        for _, row in filtered_df.iterrows():
            if row['winner'] == row['r_name']:
                # Jika pemenang adalah red corner
                winner_accuracy_data.append({
                    'head_accuracy': row['r_landed_head_per'],
                    'body_accuracy': row['r_landed_body_per'],
                    'leg_accuracy': row['r_landed_leg_per']
                })
            elif row['winner'] == row['b_name']:
                # Jika pemenang adalah blue corner
                winner_accuracy_data.append({
                    'head_accuracy': row['b_landed_head_per'],
                    'body_accuracy': row['b_landed_body_per'],
                    'leg_accuracy': row['b_landed_leg_per']

                })
        
        # Convert to DataFrame
        winner_accuracy_df = pd.DataFrame(winner_accuracy_data)
        
        # Hanya ambil kolom yang diinginkan (head, body, leg)
        selected_columns = ['head_accuracy', 'body_accuracy', 'leg_accuracy']
        filtered_accuracy_df = winner_accuracy_df[selected_columns]
        
        # Hitung rata-rata untuk setiap kategori yang dipilih
        avg_accuracy = filtered_accuracy_df.mean()
        
        # Buat bar chart
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        fig2.patch.set_facecolor('none')
        
        # Kategori dan nilai (hanya head, body, leg)
        categories = ['Head Strikes', 'Body Strikes', 'Leg Strikes']
        values = avg_accuracy.values
        
        # Buat bar chart
        bars = ax2.bar(range(len(categories)), values,
                    color=plt.cm.viridis(np.linspace(0, 1, len(categories))),
                    alpha=0.8, edgecolor='white', linewidth=1)
        
        # Atur label dan judul
        ax2.set_xticks(range(len(categories)))
        ax2.set_xticklabels(categories, rotation=45, ha='right')
        ax2.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
        ax2.set_title('Average Part Strike Accuracy of Winners', fontweight='bold', color='white', fontsize=14, pad=20)
        
        # Tambahkan nilai di atas setiap bar
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{value:.1f}%', ha='center', va='bottom', 
                    color='white', fontweight='bold', fontsize=10)
        
        # Tambahkan grid
        ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        # Atur batas y-axis
        ax2.set_ylim(0, max(values) * 1.15)
        
        # Atur style modern dengan teks putih
        ax2 = set_modern_style(ax2)
        st.pyplot(fig2, use_container_width=True)

    with col2:

        st.subheader("Strike Position Accuracy by Winner")
        
        # Buat kolom baru untuk accuracy pemenang
        winner_accuracy_data = []
        
        for _, row in filtered_df.iterrows():
            if row['winner'] == row['r_name']:
                # Jika pemenang adalah red corner
                winner_accuracy_data.append({
                    'dist_accuracy': row['r_landed_dist_per'],
                    'clinch_accuracy': row['r_landed_clinch_per'],
                    'ground_accuracy': row['r_landed_ground_per']
                })
            elif row['winner'] == row['b_name']:
                # Jika pemenang adalah blue corner
                winner_accuracy_data.append({
                    'dist_accuracy': row['b_landed_dist_per'],
                    'clinch_accuracy': row['b_landed_clinch_per'],
                    'ground_accuracy': row['b_landed_ground_per']
                })
        
        # Convert to DataFrame
        winner_accuracy_df = pd.DataFrame(winner_accuracy_data)
        
        # Hanya ambil kolom yang diinginkan (head, body, leg)
        selected_columns = ['dist_accuracy', 'clinch_accuracy', 'ground_accuracy']
        filtered_accuracy_df = winner_accuracy_df[selected_columns]
        
        # Hitung rata-rata untuk setiap kategori yang dipilih
        avg_accuracy = filtered_accuracy_df.mean()
        
        # Buat bar chart
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        fig2.patch.set_facecolor('none')
        
        # Kategori dan nilai (hanya head, body, leg)
        categories = ['Distance', 'Clinch', 'Ground']
        values = avg_accuracy.values
        
        # Buat bar chart
        bars = ax2.bar(range(len(categories)), values,
                    color=plt.cm.viridis(np.linspace(0, 1, len(categories))),
                    alpha=0.8, edgecolor='white', linewidth=1)
        
        # Atur label dan judul
        ax2.set_xticks(range(len(categories)))
        ax2.set_xticklabels(categories, rotation=45, ha='right')
        ax2.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
        ax2.set_title('Average Position Strike Accuracy of Winners', fontweight='bold', color='white', fontsize=14, pad=20)
        
        # Tambahkan nilai di atas setiap bar
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{value:.1f}%', ha='center', va='bottom', 
                    color='white', fontweight='bold', fontsize=10)
        
        # Tambahkan grid
        ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        # Atur batas y-axis
        ax2.set_ylim(0, max(values) * 1.15)
        
        # Atur style modern dengan teks putih
        ax2 = set_modern_style(ax2)
        st.pyplot(fig2, use_container_width=True)
#_____________________________________________________________________
    col3, col4 = st.columns(2)
        
    with col3:
        st.subheader("Strike Accuracy Part: Winners vs Losers")
        
        # Kumpulkan data accuracy untuk winners dan losers
        winner_data = []
        loser_data = []
        
        for _, row in filtered_df.iterrows():
            if row['winner'] == row['r_name']:
                # Winner adalah red corner, loser adalah blue corner
                winner_data.append({
                    'head': row['r_landed_head_per'],
                    'body': row['r_landed_body_per'],
                    'leg': row['r_landed_leg_per']
                })
                loser_data.append({
                    'head': row['b_landed_head_per'],
                    'body': row['b_landed_body_per'],
                    'leg': row['b_landed_leg_per']
                })
            else:
                # Winner adalah blue corner, loser adalah red corner
                winner_data.append({
                    'head': row['b_landed_head_per'],
                    'body': row['b_landed_body_per'],
                    'leg': row['b_landed_leg_per']
                })
                loser_data.append({
                    'head': row['r_landed_head_per'],
                    'body': row['r_landed_body_per'],
                    'leg': row['r_landed_leg_per']
                })
        
        # Convert to DataFrames dan hitung rata-rata
        winner_avg = pd.DataFrame(winner_data).mean()
        loser_avg = pd.DataFrame(loser_data).mean()
        
        # Buat grouped bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('none')
        
        # Posisi bar
        x = np.arange(len(winner_avg))
        width = 0.35
        
        # Categories (hanya Head, Body, Leg)
        categories = ['Head', 'Body', 'Leg']
        
        # Plot bars
        bars1 = ax.bar(x - width/2, winner_avg.values, width, 
                    label='Winners', alpha=0.8, color='#4ecdc4', edgecolor='white')
        
        bars2 = ax.bar(x + width/2, loser_avg.values, width, 
                    label='Losers', alpha=0.8, color='#ff6b6b', edgecolor='white')
        
        # Atur label dan judul
        ax.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
        ax.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
        ax.set_title('Strike Accuracy: Winners vs Losers', fontweight='bold', color='white', fontsize=14, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        # Tambahkan legend
        ax.legend(frameon=False, labelcolor='white')
        
        # Tambahkan nilai di atas setiap bar
        def add_value_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}%', ha='center', va='bottom', 
                    color='white', fontweight='bold', fontsize=10)
        
        add_value_labels(bars1)
        add_value_labels(bars2)
        
        # Tambahkan grid
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        # Atur batas y-axis
        max_value = max(max(winner_avg.values), max(loser_avg.values))
        ax.set_ylim(0, max_value * 1.15)
        
        # Atur style modern dengan teks putih
        ax = set_modern_style(ax)
        st.pyplot(fig, use_container_width=True)

    with col4:
        st.subheader("Strike Accuracy Position: Winners vs Losers")
        
        # Kumpulkan data accuracy untuk winners dan losers
        winner_data = []
        loser_data = []
        
        for _, row in filtered_df.iterrows():
            if row['winner'] == row['r_name']:
                # Winner adalah red corner, loser adalah blue corner
                winner_data.append({
                    'dist': row['r_landed_dist_per'],
                    'clinch': row['r_landed_clinch_per'],
                    'ground': row['r_landed_ground_per']
                })
                loser_data.append({
                    'dist': row['b_landed_dist_per'],
                    'clinch': row['b_landed_clinch_per'],
                    'ground': row['b_landed_ground_per']
                })
            else:
                # Winner adalah blue corner, loser adalah red corner
                winner_data.append({
                    'dist': row['r_landed_dist_per'],
                    'clinch': row['r_landed_clinch_per'],
                    'ground': row['r_landed_ground_per']
                })
                loser_data.append({
                    'dist': row['r_landed_dist_per'],
                    'clinch': row['r_landed_clinch_per'],
                    'ground': row['r_landed_ground_per']
                })
        
        # Convert to DataFrames dan hitung rata-rata
        winner_avg = pd.DataFrame(winner_data).mean()
        loser_avg = pd.DataFrame(loser_data).mean()
        
        # Buat grouped bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('none')
        
        # Posisi bar
        x = np.arange(len(winner_avg))
        width = 0.35
        
        # Categories (hanya Head, Body, Leg)
        categories = ['Distance', 'Clinch', 'Ground']
        
        # Plot bars
        bars1 = ax.bar(x - width/2, winner_avg.values, width, 
                    label='Winners', alpha=0.8, color='#4ecdc4', edgecolor='white')
        
        bars2 = ax.bar(x + width/2, loser_avg.values, width, 
                    label='Losers', alpha=0.8, color='#ff6b6b', edgecolor='white')
        
        # Atur label dan judul
        ax.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
        ax.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
        ax.set_title('Strike Accuracy: Winners vs Losers', fontweight='bold', color='white', fontsize=14, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        
        # Tambahkan legend
        ax.legend(frameon=False, labelcolor='white')
        
        # Tambahkan nilai di atas setiap bar
        def add_value_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}%', ha='center', va='bottom', 
                    color='white', fontweight='bold', fontsize=10)
        
        add_value_labels(bars1)
        add_value_labels(bars2)
        
        # Tambahkan grid
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        # Atur batas y-axis
        max_value = max(max(winner_avg.values), max(loser_avg.values))
        ax.set_ylim(0, max_value * 1.15)
        
        # Atur style modern dengan teks putih
        ax = set_modern_style(ax)
        st.pyplot(fig, use_container_width=True)


    col5, col6 = st.columns(2)
        
    with col5:
        st.subheader("Strike Accuracy Part Comparison by Method")
        selected_methods = st.multiselect(
            "Select Methods to Compare to",
            options=list(filtered_df['method'].unique()),
            default=list(filtered_df['method'].value_counts().head(3).index)
        )
        
        if selected_methods:
            # Buat figure untuk semua methods
            fig, ax = plt.subplots(figsize=(14, 8))
            fig.patch.set_facecolor('none')
            
            # Warna untuk setiap method
            colors = plt.cm.viridis(np.linspace(0, 1, len(selected_methods)))
            
            # Posisi bar
            x = np.arange(3)  # 6 kategori strike
            width = 0.8 / len(selected_methods)  # Lebar bar disesuaikan dengan jumlah methods
            
            # Plot untuk setiap method
            for i, method in enumerate(selected_methods):
                method_df = filtered_df[filtered_df['method'] == method]
                
                if len(method_df) > 0:
                    # Kumpulkan data accuracy untuk pemenang
                    accuracy_data = []
                    
                    for _, row in method_df.iterrows():
                        if row['winner'] == row['r_name']:
                            accuracy_data.append({
                                'Head': row['r_landed_head_per'],
                                'Body': row['r_landed_body_per'],
                                'Leg': row['r_landed_leg_per']
                            })
                        else:
                            accuracy_data.append({
                                'Head': row['b_landed_head_per'],
                                'Body': row['b_landed_body_per'],
                                'Leg': row['b_landed_leg_per']
                            })
                    
                    # Hitung rata-rata
                    accuracy_df = pd.DataFrame(accuracy_data)
                    avg_accuracy = accuracy_df.mean()
                    
                    # Plot bars
                    bars = ax.bar(x + i * width, avg_accuracy.values, width,
                                label=f'{method} (n={len(method_df)})',
                                color=colors[i], alpha=0.8, edgecolor='white')
            
            # Atur label dan judul
            ax.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
            ax.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
            ax.set_title('Strike Accuracy Comparison by Method', fontweight='bold', color='white', fontsize=16, pad=20)
            ax.set_xticks(x + width * (len(selected_methods) - 1) / 2)
            ax.set_xticklabels(['Head', 'Body', 'Leg'])
            
            # Tambahkan legend
            ax.legend(frameon=False, labelcolor='white', bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Tambahkan grid
            ax.grid(True, alpha=0.3, linestyle='--', axis='y')
            
            # Atur style modern dengan teks putih
            ax = set_modern_style(ax)
            st.pyplot(fig, use_container_width=True)
            
        else:
            st.info("Please select at least one method to compare.")

    with col6:
        st.subheader("Strike Accuracy Position Comparison by Method")
        
        # Pilih multiple methods untuk comparison
        selected_methods = st.multiselect(
            "Select Methods to Compare",
            options=list(filtered_df['method'].unique()),
            default=list(filtered_df['method'].value_counts().head(3).index)
        )
        
        if selected_methods:
            # Buat figure untuk semua methods
            fig, ax = plt.subplots(figsize=(14, 8))
            fig.patch.set_facecolor('none')
            
            # Warna untuk setiap method
            colors = plt.cm.viridis(np.linspace(0, 1, len(selected_methods)))
            
            # Posisi bar
            x = np.arange(3)  # 6 kategori strike
            width = 0.8 / len(selected_methods)  # Lebar bar disesuaikan dengan jumlah methods
            
            # Plot untuk setiap method
            for i, method in enumerate(selected_methods):
                method_df = filtered_df[filtered_df['method'] == method]
                
                if len(method_df) > 0:
                    # Kumpulkan data accuracy untuk pemenang
                    accuracy_data = []
                    
                    for _, row in method_df.iterrows():
                        if row['winner'] == row['r_name']:
                            accuracy_data.append({
                                'Distance': row['r_landed_dist_per'],
                                'Clinch': row['r_landed_clinch_per'],
                                'Ground': row['r_landed_ground_per']
                            })
                        else:
                            accuracy_data.append({
                                'Distance': row['r_landed_dist_per'],
                                'Clinch': row['r_landed_clinch_per'],
                                'Ground': row['r_landed_ground_per']
                            })
                    
                    # Hitung rata-rata
                    accuracy_df = pd.DataFrame(accuracy_data)
                    avg_accuracy = accuracy_df.mean()
                    
                    # Plot bars
                    bars = ax.bar(x + i * width, avg_accuracy.values, width,
                                label=f'{method} (n={len(method_df)})',
                                color=colors[i], alpha=0.8, edgecolor='white')
            
            # Atur label dan judul
            ax.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
            ax.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
            ax.set_title('Strike Accuracy Comparison by Method', fontweight='bold', color='white', fontsize=16, pad=20)
            ax.set_xticks(x + width * (len(selected_methods) - 1) / 2)
            ax.set_xticklabels(['Distance', 'Clinch', 'Ground'])
            
            # Tambahkan legend
            ax.legend(frameon=False, labelcolor='white', bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Tambahkan grid
            ax.grid(True, alpha=0.3, linestyle='--', axis='y')
            
            # Atur style modern dengan teks putih
            ax = set_modern_style(ax)
            st.pyplot(fig, use_container_width=True)
            
        else:
            st.info("Please select at least one method to compare.")
#________________________________________________________________
    col7, col8 = st.columns(2)
    with col7:
        st.subheader("Accuracy Part Comparison by Method and Fight Duration")

        # Pilih multiple methods untuk comparison - TAMBAHKAN KEY UNIK
        selected_methods = st.multiselect(
            "Select Methods to Compare",
            options=list(filtered_df['method'].unique()),
            default=list(filtered_df['method'].value_counts().head(3).index),
            key="method_comparison_multiselect_to"  # KEY UNIK DITAMBAHKAN DI SINI
        )

        # Filter berdasarkan durasi pertandingan
        min_time, max_time = st.slider(
            "Select Fight Duration Range (seconds)",
            min_value=int(filtered_df['match_time_sec'].min()),
            max_value=int(filtered_df['match_time_sec'].max()),
            value=(int(filtered_df['match_time_sec'].min()), int(filtered_df['match_time_sec'].max())),
            key="fight_duration_slider"  # KEY UNIK DITAMBAHKAN DI SINI
        )

        if selected_methods:
            # Filter data berdasarkan metode dan durasi
            filtered_by_method = filtered_df[
                (filtered_df['method'].isin(selected_methods)) &
                (filtered_df['match_time_sec'] >= min_time) &
                (filtered_df['match_time_sec'] <= max_time)
            ]
            
            if len(filtered_by_method) > 0:
                # Buat figure untuk semua methods
                fig, ax = plt.subplots(figsize=(14, 8))
                fig.patch.set_facecolor('none')
                
                # Warna untuk setiap method
                colors = plt.cm.viridis(np.linspace(0, 1, len(selected_methods)))
                
                # Kategori strike
                strike_categories = ['Head', 'Body', 'Leg']
                strike_columns = ['landed_head_per', 'landed_body_per', 'landed_leg_per']
                
                # Posisi bar
                x = np.arange(len(strike_categories))
                width = 0.8 / len(selected_methods)
                
                # Plot untuk setiap method
                for i, method in enumerate(selected_methods):
                    method_df = filtered_by_method[filtered_by_method['method'] == method]
                    
                    if len(method_df) > 0:
                        # Kumpulkan data accuracy untuk pemenang
                        accuracy_data = {category: [] for category in strike_categories}
                        
                        for _, row in method_df.iterrows():
                            # Tentukan apakah pemenang di red atau blue corner
                            if row['winner'] == row['r_name']:
                                # Pemenang adalah red corner
                                prefix = 'r_'
                            else:
                                # Pemenang adalah blue corner
                                prefix = 'b_'
                            
                            # Kumpulkan data accuracy untuk setiap kategori strike
                            for category, column in zip(strike_categories, strike_columns):
                                col_name = prefix + column
                                if col_name in row and pd.notna(row[col_name]):
                                    accuracy_data[category].append(row[col_name])
                        
                        # Hitung rata-rata untuk setiap kategori
                        avg_accuracy = [np.mean(accuracy_data[category]) if accuracy_data[category] else 0 
                                    for category in strike_categories]
                        
                        # Plot bars
                        bars = ax.bar(x + i * width, avg_accuracy, width,
                                    label=f'{method} (n={len(method_df)})',
                                    color=colors[i], alpha=0.8, edgecolor='white')
                        
                        # Tambahkan nilai di atas setiap bar
                        for j, value in enumerate(avg_accuracy):
                            if value > 0:  # Hanya tambahkan teks jika nilai > 0
                                ax.text(x[j] + i * width, value + 0.5, f'{value:.1f}%', 
                                    ha='center', va='bottom', color='white', fontweight='bold', fontsize=8)
                
                # Atur label dan judul
                ax.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
                ax.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
                ax.set_title(f'Strike Accuracy Comparison by Method\n(Fight Duration: {min_time}-{max_time} seconds)', 
                            fontweight='bold', color='white', fontsize=16, pad=20)
                ax.set_xticks(x + width * (len(selected_methods) - 1) / 2)
                ax.set_xticklabels(strike_categories)
                
                # Tambahkan legend
                ax.legend(frameon=False, labelcolor='white', bbox_to_anchor=(1.05, 1), loc='upper left')
                
                # Tambahkan grid
                ax.grid(True, alpha=0.3, linestyle='--', axis='y')
                
                # Atur batas y-axis
                max_val = 0
                for method in selected_methods:
                    method_df = filtered_by_method[filtered_by_method['method'] == method]
                    if len(method_df) > 0:
                        accuracy_data = {category: [] for category in strike_categories}
                        
                        for _, row in method_df.iterrows():
                            if row['winner'] == row['r_name']:
                                prefix = 'r_'
                            else:
                                prefix = 'b_'
                            
                            for category, column in zip(strike_categories, strike_columns):
                                col_name = prefix + column
                                if col_name in row and pd.notna(row[col_name]):
                                    accuracy_data[category].append(row[col_name])
                        
                        method_max = max([np.mean(accuracy_data[category]) if accuracy_data[category] else 0 
                                        for category in strike_categories])
                        max_val = max(max_val, method_max)
                
                ax.set_ylim(0, max_val * 1.2 if max_val > 0 else 100)
                
                # Atur style modern dengan teks putih
                ax = set_modern_style(ax)
                st.pyplot(fig, use_container_width=True)
                
                # Tampilkan statistik tambahan
                st.write(f"**Analysis Summary:**")
                st.write(f"- Total fights analyzed: {len(filtered_by_method)}")
                st.write(f"- Fight duration range: {min_time} - {max_time} seconds")
                
                # Tabel rata-rata akurasi per metode
                summary_data = []
                for method in selected_methods:
                    method_df = filtered_by_method[filtered_by_method['method'] == method]
                    if len(method_df) > 0:
                        accuracy_data = {category: [] for category in strike_categories}
                        
                        for _, row in method_df.iterrows():
                            if row['winner'] == row['r_name']:
                                prefix = 'r_'
                            else:
                                prefix = 'b_'
                            
                            for category, column in zip(strike_categories, strike_columns):
                                col_name = prefix + column
                                if col_name in row and pd.notna(row[col_name]):
                                    accuracy_data[category].append(row[col_name])
                        
                        avg_values = [np.mean(accuracy_data[category]) if accuracy_data[category] else 0 
                                    for category in strike_categories]
                        summary_data.append([method, len(method_df)] + avg_values)
                
                # Buat DataFrame untuk summary
                summary_df = pd.DataFrame(summary_data, 
                                        columns=['Method', 'Fights'] + strike_categories)
                st.dataframe(summary_df.style.format({
                    'Head': '{:.1f}%',
                    'Body': '{:.1f}%',
                    'Leg': '{:.1f}%',
                }))
                
            else:
                st.warning("No data available for the selected methods and fight duration range.")
        else:
            st.info("Please select at least one method to compare.")


    with col8:
        st.subheader("Accuracy Position Comparison by Method and Fight Duration")

        # Pilih multiple methods untuk comparison - TAMBAHKAN KEY UNIK
        selected_methods_to = st.multiselect(
            "Select Methods to Compare to",
            options=list(filtered_df['method'].unique()),
            default=list(filtered_df['method'].value_counts().head(3).index),
            key="method_comparison_multiselect"  # KEY UNIK DITAMBAHKAN DI SINI
        )

        # Filter berdasarkan durasi pertandingan
        min_time, max_time = st.slider(
            "Select Fight Duration Range (seconds)",
            min_value=int(filtered_df['match_time_sec'].min()),
            max_value=int(filtered_df['match_time_sec'].max()),
            value=(int(filtered_df['match_time_sec'].min()), int(filtered_df['match_time_sec'].max())),
            key="fight_duration_slider_to"  # KEY UNIK DITAMBAHKAN DI SINI
        )

        if selected_methods_to:
            # Filter data berdasarkan metode dan durasi
            filtered_by_method = filtered_df[
                (filtered_df['method'].isin(selected_methods_to)) &
                (filtered_df['match_time_sec'] >= min_time) &
                (filtered_df['match_time_sec'] <= max_time)
            ]
            
            if len(filtered_by_method) > 0:
                # Buat figure untuk semua methods
                fig, ax = plt.subplots(figsize=(14, 8))
                fig.patch.set_facecolor('none')
                
                # Warna untuk setiap method
                colors = plt.cm.viridis(np.linspace(0, 1, len(selected_methods_to)))
                
                # Kategori strike
                strike_categories = ['Distance', 'Clinch', 'Ground']
                strike_columns = ['landed_dist_per', 'landed_clinch_per', 'landed_ground_per']
                
                # Posisi bar
                x = np.arange(len(strike_categories))
                width = 0.8 / len(selected_methods_to)
                
                # Plot untuk setiap method
                for i, method in enumerate(selected_methods_to):
                    method_df = filtered_by_method[filtered_by_method['method'] == method]
                    
                    if len(method_df) > 0:
                        # Kumpulkan data accuracy untuk pemenang
                        accuracy_data = {category: [] for category in strike_categories}
                        
                        for _, row in method_df.iterrows():
                            # Tentukan apakah pemenang di red atau blue corner
                            if row['winner'] == row['r_name']:
                                # Pemenang adalah red corner
                                prefix = 'r_'
                            else:
                                # Pemenang adalah blue corner
                                prefix = 'b_'
                            
                            # Kumpulkan data accuracy untuk setiap kategori strike
                            for category, column in zip(strike_categories, strike_columns):
                                col_name = prefix + column
                                if col_name in row and pd.notna(row[col_name]):
                                    accuracy_data[category].append(row[col_name])
                        
                        # Hitung rata-rata untuk setiap kategori
                        avg_accuracy = [np.mean(accuracy_data[category]) if accuracy_data[category] else 0 
                                    for category in strike_categories]
                        
                        # Plot bars
                        bars = ax.bar(x + i * width, avg_accuracy, width,
                                    label=f'{method} (n={len(method_df)})',
                                    color=colors[i], alpha=0.8, edgecolor='white')
                        
                        # Tambahkan nilai di atas setiap bar
                        for j, value in enumerate(avg_accuracy):
                            if value > 0:  # Hanya tambahkan teks jika nilai > 0
                                ax.text(x[j] + i * width, value + 0.5, f'{value:.1f}%', 
                                    ha='center', va='bottom', color='white', fontweight='bold', fontsize=8)
                
                # Atur label dan judul
                ax.set_xlabel('Strike Type', color='white', fontweight='bold', fontsize=12)
                ax.set_ylabel('Accuracy Percentage (%)', color='white', fontweight='bold', fontsize=12)
                ax.set_title(f'Strike Accuracy Comparison by Method\n(Fight Duration: {min_time}-{max_time} seconds)', 
                            fontweight='bold', color='white', fontsize=16, pad=20)
                ax.set_xticks(x + width * (len(selected_methods_to) - 1) / 2)
                ax.set_xticklabels(strike_categories)
                
                # Tambahkan legend
                ax.legend(frameon=False, labelcolor='white', bbox_to_anchor=(1.05, 1), loc='upper left')
                
                # Tambahkan grid
                ax.grid(True, alpha=0.3, linestyle='--', axis='y')
                
                # Atur batas y-axis
                max_val = 0
                for method in selected_methods_to:
                    method_df = filtered_by_method[filtered_by_method['method'] == method]
                    if len(method_df) > 0:
                        accuracy_data = {category: [] for category in strike_categories}
                        
                        for _, row in method_df.iterrows():
                            if row['winner'] == row['r_name']:
                                prefix = 'r_'
                            else:
                                prefix = 'b_'
                            
                            for category, column in zip(strike_categories, strike_columns):
                                col_name = prefix + column
                                if col_name in row and pd.notna(row[col_name]):
                                    accuracy_data[category].append(row[col_name])
                        
                        method_max = max([np.mean(accuracy_data[category]) if accuracy_data[category] else 0 
                                        for category in strike_categories])
                        max_val = max(max_val, method_max)
                
                ax.set_ylim(0, max_val * 1.2 if max_val > 0 else 100)
                
                # Atur style modern dengan teks putih
                ax = set_modern_style(ax)
                st.pyplot(fig, use_container_width=True)
                
                # Tampilkan statistik tambahan
                st.write(f"**Analysis Summary:**")
                st.write(f"- Total fights analyzed: {len(filtered_by_method)}")
                st.write(f"- Fight duration range: {min_time} - {max_time} seconds")
                
                # Tabel rata-rata akurasi per metode
                summary_data = []
                for method in selected_methods_to:
                    method_df = filtered_by_method[filtered_by_method['method'] == method]
                    if len(method_df) > 0:
                        accuracy_data = {category: [] for category in strike_categories}
                        
                        for _, row in method_df.iterrows():
                            if row['winner'] == row['r_name']:
                                prefix = 'r_'
                            else:
                                prefix = 'b_'
                            
                            for category, column in zip(strike_categories, strike_columns):
                                col_name = prefix + column
                                if col_name in row and pd.notna(row[col_name]):
                                    accuracy_data[category].append(row[col_name])
                        
                        avg_values = [np.mean(accuracy_data[category]) if accuracy_data[category] else 0 
                                    for category in strike_categories]
                        summary_data.append([method, len(method_df)] + avg_values)
                
                # Buat DataFrame untuk summary
                summary_df = pd.DataFrame(summary_data, 
                                        columns=['Method', 'Fights'] + strike_categories)
                st.dataframe(summary_df.style.format({
                    'Distance': '{:.1f}%',
                    'Clinch': '{:.1f}%',
                    'Ground': '{:.1f}%',
                }))
                
            else:
                st.warning("No data available for the selected methods and fight duration range.")
        else:
            st.info("Please select at least one method to compare.")

with tab3:
    st.header("Additional Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 5 Most Frequent Referees")
        
        # Hitung frekuensi referee dan ambil top 5
        referee_counts = filtered_df['referee'].value_counts().head(5)
        
        fig1, ax1 = plt.subplots(figsize=(8, 6))  # Reduced width for better proportion
        fig1.patch.set_facecolor('none')
        
        # Buat donut chart dengan jumlah (bukan persentase)
        colors = plt.cm.viridis(np.linspace(0, 1, len(referee_counts)))
        
        # Gunakan autopct dengan format yang benar
        wedges, texts, autotexts = ax1.pie(referee_counts.values, 
                                         labels=referee_counts.index,
                                         autopct=lambda p: f'{int(p * sum(referee_counts.values) / 100)}',
                                         colors=colors,
                                         startangle=90,
                                         wedgeprops=dict(width=0.65))
        
        # Ubah warna teks menjadi putih
        for text in texts:
            text.set_color('white')
            text.set_fontweight('bold')
            text.set_fontsize(9)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax1.set_title('Top 5 Most Frequent Referees', fontweight='bold', color='white', fontsize=14, pad=20)
        
        # Atur style modern dengan teks putih
        ax1 = set_modern_style(ax1)
        st.pyplot(fig1, use_container_width=True)

    with col2:
        st.subheader("Win Comparison: Red vs Blue Corner")
        
        # Hitung total kemenangan
        red_wins = len(filtered_df[filtered_df['winner'] == filtered_df['r_name']])
        blue_wins = len(filtered_df[filtered_df['winner'] == filtered_df['b_name']])
        total_fights = len(filtered_df)
        
        # Hitung persentase
        red_win_percentage = (red_wins / total_fights) * 100
        blue_win_percentage = (blue_wins / total_fights) * 100
        
        # Buat bar chart
        fig2, ax2 = plt.subplots(figsize=(8, 6))  # Same size as fig1
        fig2.patch.set_facecolor('none')
        
        # Data untuk chart
        categories = ['Red Corner', 'Blue Corner']
        values = [red_wins, blue_wins]
        colors = ['#ff6b6b', '#4ecdc4']
        
        # Buat bar chart
        bars = ax2.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        
        # Atur label dan judul
        ax2.set_xlabel('Corner', color='white', fontweight='bold', fontsize=12)
        ax2.set_ylabel('Number of Wins', color='white', fontweight='bold', fontsize=12)
        ax2.set_title('Win Comparison: Red vs Blue Corner', fontweight='bold', color='white', fontsize=14, pad=20)
        
        # Tambahkan nilai di atas setiap bar
        for i, (bar, value, percentage) in enumerate(zip(bars, values, [red_win_percentage, blue_win_percentage])):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                   f'{value} ({percentage:.1f}%)', ha='center', va='bottom', 
                   color='white', fontweight='bold', fontsize=11)
        
        # Tambahkan grid
        ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        # Atur batas y-axis
        ax2.set_ylim(0, max(values) * 1.2)
        
        # Atur style modern dengan teks putih
        ax2 = set_modern_style(ax2)
        st.pyplot(fig2, use_container_width=True)
        # Modern dataframe display with white text
# ... (rest of the code remains the same with similar changes for text colors)

    st.subheader("Fight Locations Map")

# Load data koordinat
    url = "https://github.com/vicktorindra-dev/ufc_streamlit/raw/refs/heads/main/location_coords_full.xlsx"
    df2 = pd.read_excel(url)

    # Pastikan kolom yang diperlukan ada
    if "location" in df2.columns and "latitude" in df2.columns and "longitude" in df2.columns:
        # Hitung jumlah event per lokasi
        location_counts = df2['location'].value_counts().reset_index()
        location_counts.columns = ['location', 'count']
        
        # Gabungkan dengan data koordinat
        map_df = df2[['location', 'latitude', 'longitude']].drop_duplicates()
        location_counts = location_counts.merge(map_df, on='location', how='left')
        
        # Filter hanya lokasi yang memiliki koordinat
        location_counts = location_counts.dropna(subset=['latitude', 'longitude'])
        
        if not location_counts.empty:
            # Tampilkan peta dengan ukuran marker berdasarkan jumlah event
            st.map(location_counts[["latitude", "longitude"]], 
                size='count', 
                color='#ff0000',  # Warna merah untuk marker
                zoom=1)  # Zoom level default
            
            # Tampilkan statistik lokasi
            

        else:
            st.warning("Tidak ada lokasi dengan koordinat yang valid.")
    else:
        st.warning("File koordinat tidak memiliki kolom yang diperlukan (location, latitude, longitude).")
    
    

with tab4:
    st.header("🥊 Fighter Comparison")

    # Select fighters to compare
    all_fighters = sorted(pd.concat([filtered_df['r_name'], filtered_df['b_name']]).unique())

    col1, col2 = st.columns(2)

    with col1:
        fighter1 = st.selectbox("Select Fighter 1", options=all_fighters, index=0, key="fighter1_select")

    with col2:
        other_fighters = [f for f in all_fighters if f != fighter1]
        fighter2 = st.selectbox("Select Fighter 2", options=other_fighters, index=0, key="fighter2_select")

    # Get fighter stats function with error handling
    def get_fighter_stats(fighter_name):
        red_fights = filtered_df[filtered_df['r_name'] == fighter_name]
        blue_fights = filtered_df[filtered_df['b_name'] == fighter_name]
        
        total_fights = len(red_fights) + len(blue_fights)
        wins = len(red_fights[red_fights['winner'] == fighter_name]) + len(blue_fights[blue_fights['winner'] == fighter_name])
        losses = total_fights - wins
        
        # Striking stats with error handling
        avg_sig_strikes = (red_fights['r_sig_str_landed'].sum() + blue_fights['b_sig_str_landed'].sum()) / total_fights if total_fights > 0 else 0
        avg_total_strikes = (red_fights['r_total_str_landed'].sum() + blue_fights['b_total_str_landed'].sum()) / total_fights if total_fights > 0 else 0
        
        # Calculate strike accuracy only if attempted columns exist
        sig_strike_accuracy = 0
        if 'r_sig_str_attempted' in filtered_df.columns and 'b_sig_str_attempted' in filtered_df.columns:
            total_attempted = (red_fights['r_sig_str_attempted'].sum() + blue_fights['b_sig_str_attempted'].sum())
            total_landed = (red_fights['r_sig_str_landed'].sum() + blue_fights['b_sig_str_landed'].sum())
            sig_strike_accuracy = (total_landed / total_attempted * 100) if total_attempted > 0 else 0
        else:
            # Fallback: use simple average if attempted columns don't exist
            sig_strike_accuracy = avg_sig_strikes  # This is a simple approximation
        
        # Grappling stats with error handling
        avg_takedowns = 0
        takedown_accuracy = 0
        if 'r_td_landed' in filtered_df.columns and 'b_td_landed' in filtered_df.columns:
            avg_takedowns = (red_fights['r_td_landed'].sum() + blue_fights['b_td_landed'].sum()) / total_fights if total_fights > 0 else 0
            
            if 'r_td_attempted' in filtered_df.columns and 'b_td_attempted' in filtered_df.columns:
                total_td_attempted = (red_fights['r_td_attempted'].sum() + blue_fights['b_td_attempted'].sum())
                total_td_landed = (red_fights['r_td_landed'].sum() + blue_fights['b_td_landed'].sum())
                takedown_accuracy = (total_td_landed / total_td_attempted * 100) if total_td_attempted > 0 else 0
        
        # Defense stats
        avg_sig_strikes_absorbed = (red_fights['b_sig_str_landed'].sum() + blue_fights['r_sig_str_landed'].sum()) / total_fights if total_fights > 0 else 0
        
        return {
            'Total Fights': total_fights,
            'Wins': wins,
            'Losses': losses,
            'Win Percentage': (wins / total_fights * 100) if total_fights > 0 else 0,
            'Avg Sig Strikes Landed': round(avg_sig_strikes, 1),
            'Avg Total Strikes Landed': round(avg_total_strikes, 1),
            'Sig Strike Accuracy %': round(sig_strike_accuracy, 1),
            'Avg Takedowns Landed': round(avg_takedowns, 1),
            'Takedown Accuracy %': round(takedown_accuracy, 1),
            'Avg Sig Strikes Absorbed': round(avg_sig_strikes_absorbed, 1)
        }

    stats1 = get_fighter_stats(fighter1)
    stats2 = get_fighter_stats(fighter2)

    # Display comparison
    st.markdown("---")
    st.subheader(f"Comparison: {fighter1} vs {fighter2}")

    # Key metrics comparison
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Win %", f"{stats1['Win Percentage']:.1f}%", 
                f"{stats1['Win Percentage'] - stats2['Win Percentage']:.1f}%")
    with col2:
        st.metric("Avg Sig Strikes", f"{stats1['Avg Sig Strikes Landed']:.1f}", 
                f"{stats1['Avg Sig Strikes Landed'] - stats2['Avg Sig Strikes Landed']:.1f}")
    with col3:
        st.metric("TD Accuracy", f"{stats1['Takedown Accuracy %']:.1f}%", 
                f"{stats1['Takedown Accuracy %'] - stats2['Takedown Accuracy %']:.1f}%")
    with col4:
        st.metric("Strike Accuracy", f"{stats1['Sig Strike Accuracy %']:.1f}%", 
                f"{stats1['Sig Strike Accuracy %'] - stats2['Sig Strike Accuracy %']:.1f}%")

    # Radar chart for skill comparison (only include available metrics)
    available_categories = []
    for cat in ['Win Percentage', 'Avg Sig Strikes Landed', 'Sig Strike Accuracy %', 
                'Avg Takedowns Landed', 'Takedown Accuracy %']:
        if stats1.get(cat, 0) is not None and stats2.get(cat, 0) is not None:
            available_categories.append(cat)

    if available_categories:
        st.markdown("### Skills Comparison Radar")
        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=[stats1[cat] for cat in available_categories],
            theta=available_categories,
            fill='toself',
            name=fighter1
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=[stats2[cat] for cat in available_categories],
            theta=available_categories,
            fill='toself',
            name=fighter2
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(max([stats1[cat] for cat in available_categories]), 
                                max([stats2[cat] for cat in available_categories])) * 1.2]
                )),
            showlegend=True
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Detailed stats comparison
    st.markdown("### Detailed Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(fighter1)
        st.write(f"**Record:** {stats1['Wins']}W - {stats1['Losses']}L")
        st.write(f"**Total Fights:** {stats1['Total Fights']}")
        st.write(f"**Avg Significant Strikes:** {stats1['Avg Sig Strikes Landed']}")
        st.write(f"**Strike Accuracy:** {stats1['Sig Strike Accuracy %']}%")
        st.write(f"**Avg Takedowns:** {stats1['Avg Takedowns Landed']}")
        st.write(f"**Takedown Accuracy:** {stats1['Takedown Accuracy %']}%")
        st.write(f"**Avg Strikes Absorbed:** {stats1['Avg Sig Strikes Absorbed']}")

    with col2:
        st.subheader(fighter2)
        st.write(f"**Record:** {stats2['Wins']}W - {stats2['Losses']}L")
        st.write(f"**Total Fights:** {stats2['Total Fights']}")
        st.write(f"**Avg Significant Strikes:** {stats2['Avg Sig Strikes Landed']}")
        st.write(f"**Strike Accuracy:** {stats2['Sig Strike Accuracy %']}%")
        st.write(f"**Avg Takedowns:** {stats2['Avg Takedowns Landed']}")
        st.write(f"**Takedown Accuracy:** {stats2['Takedown Accuracy %']}%")
        st.write(f"**Avg Strikes Absorbed:** {stats2['Avg Sig Strikes Absorbed']}")

    # Bar chart comparison
    st.markdown("### Statistical Comparison")

    # Only include metrics that have values
    comparison_metrics = []
    for metric in ['Win Percentage', 'Avg Sig Strikes Landed', 'Sig Strike Accuracy %', 
                'Avg Takedowns Landed', 'Takedown Accuracy %']:
        if stats1.get(metric, 0) is not None and stats2.get(metric, 0) is not None:
            comparison_metrics.append(metric)

    comparison_df = pd.DataFrame({
        'Metric': comparison_metrics,
        fighter1: [stats1[metric] for metric in comparison_metrics],
        fighter2: [stats2[metric] for metric in comparison_metrics]
    })

    if not comparison_df.empty:
        fig = px.bar(
            comparison_df,
            x='Metric',
            y=[fighter1, fighter2],
            barmode='group',
            title="Fighter Statistics Comparison",
            color_discrete_map={fighter1: "red", fighter2: "blue"}  # warna sesuai fighter
        )
        st.plotly_chart(fig, use_container_width=True)  # Full width

    st.markdown("---")
    st.subheader("Strike Accuracy by Position")

    def get_fighter_accuracy_stats(fighter_name):
        red_fights = filtered_df[filtered_df['r_name'] == fighter_name]
        blue_fights = filtered_df[filtered_df['b_name'] == fighter_name]
        
        total_fights = len(red_fights) + len(blue_fights)
        
        if total_fights == 0:
            return {key: 0 for key in ['head_accuracy', 'body_accuracy', 'leg_accuracy', 
                                    'dist_accuracy', 'clinch_accuracy', 'ground_accuracy']}
        
        # Calculate average accuracy for each position with error handling
        accuracy_stats = {}
        accuracy_columns = {
            'head_accuracy': ['r_landed_head_per', 'b_landed_head_per'],
            'body_accuracy': ['r_landed_body_per', 'b_landed_body_per'],
            'leg_accuracy': ['r_landed_leg_per', 'b_landed_leg_per'],
            'dist_accuracy': ['r_landed_dist_per', 'b_landed_dist_per'],
            'clinch_accuracy': ['r_landed_clinch_per', 'b_landed_clinch_per'],
            'ground_accuracy': ['r_landed_ground_per', 'b_landed_ground_per']
        }
        
        for stat_key, columns in accuracy_columns.items():
            if all(col in filtered_df.columns for col in columns):
                red_sum = red_fights[columns[0]].sum()
                blue_sum = blue_fights[columns[1]].sum()
                accuracy_stats[stat_key] = (red_sum + blue_sum) / total_fights
            else:
                accuracy_stats[stat_key] = 0
        
        return accuracy_stats

    # Get accuracy stats for both fighters
    accuracy1 = get_fighter_accuracy_stats(fighter1)
    accuracy2 = get_fighter_accuracy_stats(fighter2)

    # Create comparison chart only if we have accuracy data
    available_categories = []
    fighter1_acc = []
    fighter2_acc = []

    accuracy_mapping = {
        'Head Strikes': 'head_accuracy',
        'Body Strikes': 'body_accuracy',
        'Leg Strikes': 'leg_accuracy',
        'Distance Strikes': 'dist_accuracy',
        'Clinch Strikes': 'clinch_accuracy',
        'Ground Strikes': 'ground_accuracy'
    }

    for display_name, data_key in accuracy_mapping.items():
        if accuracy1.get(data_key, 0) > 0 or accuracy2.get(data_key, 0) > 0:
            available_categories.append(display_name)
            fighter1_acc.append(accuracy1.get(data_key, 0))
            fighter2_acc.append(accuracy2.get(data_key, 0))

    if available_categories and any(fighter1_acc + fighter2_acc):
        # Create figure
        fig_acc, ax_acc = plt.subplots(figsize=(12, 8))

        # Set width of bars
        bar_width = 0.35
        x_pos = np.arange(len(available_categories))

        # Create bars
        bars1 = ax_acc.bar(x_pos - bar_width/2, fighter1_acc, bar_width, 
                        label=fighter1, alpha=0.8, color='#FF4B4B')
        bars2 = ax_acc.bar(x_pos + bar_width/2, fighter2_acc, bar_width, 
                        label=fighter2, alpha=0.8, color='#1F77B4')

        # Add values on top of bars
        def add_values(bars):
            for bar in bars:
                height = bar.get_height()
                if height > 0:  # Only add text if value is positive
                    ax_acc.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                            f'{height:.1f}%', ha='center', va='bottom', 
                            fontweight='bold', fontsize=9)

        add_values(bars1)
        add_values(bars2)

        # Customize the chart
        ax_acc.set_xlabel('Strike Type', fontweight='bold', fontsize=12)
        ax_acc.set_ylabel('Accuracy Percentage (%)', fontweight='bold', fontsize=12)
        ax_acc.set_title(f'Strike Accuracy Comparison: {fighter1} vs {fighter2}', 
                        fontweight='bold', fontsize=14, pad=20)
        ax_acc.set_xticks(x_pos)
        ax_acc.set_xticklabels(available_categories, rotation=45, ha='right')
        ax_acc.legend()
        ax_acc.grid(True, alpha=0.3, linestyle='--', axis='y')

        # Set y-axis limit
        max_acc = max(max(fighter1_acc), max(fighter2_acc)) if (fighter1_acc + fighter2_acc) else 100
        ax_acc.set_ylim(0, max_acc * 1.15 if max_acc > 0 else 100)

        # Adjust layout
        plt.tight_layout()

        # Display the chart
        st.pyplot(fig_acc, use_container_width=True)

        # Additional accuracy metrics in columns
        st.markdown("### Detailed Accuracy Statistics")

        acc_col1, acc_col2 = st.columns(2)

        with acc_col1:
            st.subheader(fighter1)
            for display_name, data_key in accuracy_mapping.items():
                if accuracy1.get(data_key, 0) > 0:
                    st.write(f"**{display_name}:** {accuracy1[data_key]:.1f}%")

        with acc_col2:
            st.subheader(fighter2)
            for display_name, data_key in accuracy_mapping.items():
                if accuracy2.get(data_key, 0) > 0:
                    st.write(f"**{display_name}:** {accuracy2[data_key]:.1f}%")
    else:
        st.warning("Strike accuracy data is not available for the selected fighters.")

with tab5:
    st.header("Custom Analysis")
    
    st.markdown("""
    ### Create Your Own Visualizations
    Use the options below to create custom charts based on the UFC fight data.
    """)
    
    # Tambahkan date filter untuk custom analysis
    st.subheader("Date Filter")
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        start_date_custom = st.date_input(
            "Start Date",
            value=filtered_df['date'].min(),
            min_value=filtered_df['date'].min(),
            max_value=filtered_df['date'].max()
        )
    
    with col_filter2:
        end_date_custom = st.date_input(
            "End Date",
            value=filtered_df['date'].max(),
            min_value=filtered_df['date'].min(),
            max_value=filtered_df['date'].max()
        )
    
    # Filter data berdasarkan date range yang dipilih
    start_date_custom = pd.to_datetime(start_date_custom)
    end_date_custom = pd.to_datetime(end_date_custom)
    
    custom_filtered_df = filtered_df[
        (filtered_df['date'] >= start_date_custom) & 
        (filtered_df['date'] <= end_date_custom)
    ]
    
    st.info(f"Data range: {start_date_custom.strftime('%Y-%m-%d')} to {end_date_custom.strftime('%Y-%m-%d')} ({len(custom_filtered_df)} fights)")
    
    # Custom chart creator
    chart_type = st.selectbox(
        "Select Chart Type",
        options=["Bar Chart", "Pie Chart", "Histogram", "Scatter Plot", "Time Series"]
    )
    
    if chart_type == "Bar Chart":
        col1, col2 = st.columns(2)
        
        with col1:
            x_column = st.selectbox("X-axis Column", options=custom_filtered_df.columns)
        
        with col2:
            y_column = st.selectbox("Y-axis Column", options=['count'] + list(custom_filtered_df.select_dtypes(include=[np.number]).columns))
        
        title = st.text_input("Chart Title", "Custom Bar Chart")
        x_label = st.text_input("X-axis Label", x_column)
        y_label = st.text_input("Y-axis Label", y_column)
        
        if st.button("Generate Bar Chart"):
            # Group data if needed
            if y_column == 'count':
                chart_data = custom_filtered_df[x_column].value_counts().sort_index()
            else:
                chart_data = custom_filtered_df.groupby(x_column)[y_column].mean()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('none')
            
            bars = ax.bar(range(len(chart_data)), chart_data.values, 
                         color=plt.cm.viridis(np.linspace(0, 1, len(chart_data))),
                         alpha=0.8, edgecolor='white', linewidth=1)
            
            ax.set_xticks(range(len(chart_data)))
            ax.set_xticklabels(chart_data.index, rotation=45, ha='right')
            ax.set_xlabel(x_label, color='white')
            ax.set_ylabel(y_label, color='white')
            ax.set_title(title, fontweight='bold', color='white')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{height:.1f}', ha='center', va='bottom', color='white', fontweight='bold')
            
            ax = set_modern_style(ax)
            st.pyplot(fig, use_container_width=True)
    
    elif chart_type == "Pie Chart":
        column = st.selectbox("Select Column", options=custom_filtered_df.select_dtypes(include=['object']).columns)
        title = st.text_input("Chart Title", f"{column} Distribution")
        
        if st.button("Generate Pie Chart"):
            counts = custom_filtered_df[column].value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('none')
            
            colors = plt.cm.viridis(np.linspace(0, 1, len(counts)))
            wedges, texts, autotexts = ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%',
                                             colors=colors, startangle=90)
            
            # Change text colors to white
            for text in texts:
                text.set_color('white')
                text.set_fontweight('bold')
                
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title(title, fontweight='bold', color='white')
            ax = set_modern_style(ax)
            st.pyplot(fig, use_container_width=True)
    
    elif chart_type == "Histogram":
        column = st.selectbox("Select Numeric Column", options=custom_filtered_df.select_dtypes(include=[np.number]).columns)
        bins = st.slider("Number of Bins", min_value=5, max_value=50, value=15)
        title = st.text_input("Chart Title", f"Distribution of {column}")
        x_label = st.text_input("X-axis Label", column)
        
        if st.button("Generate Histogram"):
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('none')
            
            ax.hist(custom_filtered_df[column], bins=bins, alpha=0.7, color='#4ecdc4', 
                    edgecolor='white', linewidth=0.5)
            
            ax.set_xlabel(x_label, color='white')
            ax.set_ylabel('Frequency', color='white')
            ax.set_title(title, fontweight='bold', color='white')
            
            ax = set_modern_style(ax)
            st.pyplot(fig, use_container_width=True)
    
    elif chart_type == "Scatter Plot":
        col1, col2 = st.columns(2)
        
        with col1:
            x_column = st.selectbox("X-axis Column", options=custom_filtered_df.select_dtypes(include=[np.number]))

with tab6:
    st.header("Data Overview")
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str)

    st.dataframe(df.sort_values('date', ascending=False))

# Footer
st.markdown("---")
st.markdown("### Data Source: UFC Historical Fight Data")
st.markdown("Dashboard created with Streamlit • Modern Design Edition")
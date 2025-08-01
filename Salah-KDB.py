import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

# Define base directory as the folder containing this script
BASE_DIR = Path(__file__).parent

# Create Path objects for your CSV and image files relative to BASE_DIR
kdb_csv_path = BASE_DIR / 'Kevin de Bruyne FPL all-time stats.csv'
salah_csv_path = BASE_DIR / 'Mo Salah FPL all-time Stats.csv'
img_kdb_path = BASE_DIR / 'de Bruyne.png'
img_salah_path = BASE_DIR / 'Salah.png'

@st.cache_data
def load_kdb_data():
    return pd.read_csv(kdb_csv_path)

@st.cache_data
def load_salah_data():
    return pd.read_csv(salah_csv_path)

df_kdb = load_kdb_data()
df_salah = load_salah_data()

st.title("Kevin De Bruyne vs Mohamed Salah All-Time Fantasy Premier League Stats")

# Layout player images side-by-side using columns
col_left, col_right = st.columns(2)

with col_left:
    st.image(str(img_kdb_path), width=160, caption='Kevin De Bruyne')

with col_right:
    st.image(str(img_salah_path), width=160, caption='Mohamed Salah')

# -- Interactivity --

all_columns = df_kdb.columns.tolist()  # Assumes similar columns in both
selected_columns = st.multiselect(
    "Select columns to display",
    options=all_columns,
    default=['season_name', 'goals_scored', 'assists']
)

all_seasons = sorted(df_kdb['season_name'].unique())
selected_seasons = st.multiselect(
    "Select seasons to include",
    options=all_seasons,
    default=all_seasons
)

# Filter dataframes by selected seasons
df_kdb_filtered = df_kdb[df_kdb['season_name'].isin(selected_seasons)]
df_salah_filtered = df_salah[df_salah['season_name'].isin(selected_seasons)]

st.header("Kevin De Bruyne's Data")
if selected_columns:
    st.dataframe(df_kdb_filtered[selected_columns])
else:
    st.write("Please select at least one column")

st.header("Mohamed Salah's Data")
if selected_columns:
    st.dataframe(df_salah_filtered[selected_columns])
else:
    st.write("Please select at least one column")

st.header("Comparison between Kevin De Bruyne and Mohamed Salah")

# Merge filtered data on season_name with all needed columns
merge_columns = ['season_name','goals_scored','assists','total_points',
                 'influence', 'creativity', 'minutes', 'penalties_missed']

df_merged = pd.merge(
    df_kdb_filtered[merge_columns],
    df_salah_filtered[merge_columns],
    on='season_name',
    suffixes=('_kdb', '_salah')
).sort_values('season_name')

# Define a helper function to create and display a plot
def plot_stat(stat, ylabel, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_merged['season_name'], df_merged[f'{stat}_kdb'], marker='o', label='Kevin De Bruyne')
    ax.plot(df_merged['season_name'], df_merged[f'{stat}_salah'], marker='s', label='Mohamed Salah')
    ax.set_xlabel("Season")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Plot each stat
plot_stat('goals_scored', 'Goals Scored', 'Goals Scored by Season')
plot_stat('assists', 'Assists', 'Assists by Season')
plot_stat('total_points', 'Total Points', 'Total Points by Season')
plot_stat('influence', 'Influence', 'Influence by Season')
plot_stat('creativity', 'Creativity', 'Creativity by Season')
plot_stat('minutes', 'Minutes Played', 'Minutes Played by Season')
plot_stat('penalties_missed', 'Penalties Missed', 'Penalties Missed by Season')

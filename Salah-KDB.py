import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

@st.cache_data
def load_kdb_data():
    return pd.read_csv('/Users/siphuvuyomngxunyeni/Downloads/Football Analytics/KDB vs Mo Salah/Kevin de Bruyne FPL all-time stats.csv')

@st.cache_data
def load_salah_data():
    return pd.read_csv('/Users/siphuvuyomngxunyeni/Downloads/Football Analytics/KDB vs Mo Salah/Mo Salah FPL all-time Stats.csv')

df_kdb = load_kdb_data()
df_salah = load_salah_data()

st.title("Kevin De Bruyne vs Mohamed Salah All-Time Fantasy Premier League Stats")

col_left,col_right=st.columns(2)

with col_left:
    st.image('/Users/siphuvuyomngxunyeni/Downloads/Football Analytics/KDB vs Mo Salah/de Bruyne.png', width=150, caption='Kevin De Bruyne')

with col_right:
    st.image('/Users/siphuvuyomngxunyeni/Downloads/Football Analytics/KDB vs Mo Salah/Salah.png', width=150, caption='Mohamed Salah')

# -- Interactivity --

# 1. Select which columns to display
all_columns = df_kdb.columns.tolist()  # Assumes both dataframes have similar columns
selected_columns = st.multiselect(
    "Select columns to display",
    options=all_columns,
    default=['season_name', 'goals_scored', 'assists']  # default columns shown
)

# 2. Select seasons to filter
all_seasons = sorted(df_kdb['season_name'].unique())
selected_seasons = st.multiselect(
    "Select seasons to include",
    options=all_seasons,
    default=all_seasons  # show all seasons by default
)

# Filter dataframes by seasons selected
df_kdb_filtered = df_kdb[df_kdb['season_name'].isin(selected_seasons)]
df_salah_filtered = df_salah[df_salah['season_name'].isin(selected_seasons)]

# Show filtered data with chosen columns
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

# -- Plot filtered data --
st.header("Comparison between Kevin De Bruyne and Mohamed Salah")

# Merge filtered data on season_name
df_merged = pd.merge(
    df_kdb_filtered[['season_name','goals_scored','assists','total_points','influence', 'creativity']],
    df_salah_filtered[['season_name','goals_scored','assists','total_points','influence', 'creativity']],
    on='season_name',
    suffixes=('_kdb', '_salah')
).sort_values('season_name')

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(df_merged['season_name'], df_merged['goals_scored_kdb'], marker='o', label='Kevin De Bruyne')
ax1.plot(df_merged['season_name'], df_merged['goals_scored_salah'], marker='s', label='Mohamed Salah')
ax1.set_xlabel("Season")
ax1.set_ylabel("Goals Scored")
ax1.set_title("Goals Scored by Season")
ax1.legend()
st.pyplot(fig1)

fig2, ax2=plt.subplots(figsize=(10, 6))
ax2.plot(df_merged['season_name'],df_merged['assists_kdb'], marker='o', label='Kevin De Bruyne')
ax2.plot(df_merged['season_name'], df_merged['assists_salah'], marker='s', label='Mohamed Salah')
ax2.set_xlabel("Season")
ax2.set_ylabel("Assists")
ax2.set_title("Assists by Season")
ax2.legend()
st.pyplot(fig2)

fig3, ax3=plt.subplots(figsize=(10, 6))
ax3.plot(df_merged['season_name'],df_merged['total_points_kdb'], marker='o', label='Kevin De Bruyne')
ax3.plot(df_merged['season_name'], df_merged['total_points_salah'], marker='s', label='Mohamed Salah')
ax3.set_xlabel("Season")
ax3.set_ylabel("Total Points")
ax3.set_title("Total Points by Season")
ax3.legend()
st.pyplot(fig3)

fig4, ax4=plt.subplots(figsize=(10, 6))
ax4.plot(df_merged['season_name'],df_merged['influence_kdb'], marker='o', label='Kevin De Bruyne')
ax4.plot(df_merged['season_name'], df_merged['influence_salah'], marker='s', label='Mohamed Salah')
ax4.set_xlabel("Season")
ax4.set_ylabel("Influence")
ax4.set_title("Influence by Season")
ax4.legend()
st.pyplot(fig4)

fig5, ax5=plt.subplots(figsize=(10, 6))
ax5.plot(df_merged['season_name'],df_merged['creativity_kdb'], marker='o', label='Kevin De Bruyne')
ax5.plot(df_merged['season_name'], df_merged['creativity_salah'], marker='s', label='Mohamed Salah')
ax5.set_xlabel("Season")
ax5.set_ylabel("Creativity")
ax5.set_title("Creativity by Season")
ax5.legend()
st.pyplot(fig5)

plt.xticks(rotation=45)
plt.tight_layout()

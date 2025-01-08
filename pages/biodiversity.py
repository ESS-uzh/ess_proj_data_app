import streamlit as st
from streamlit_folium import st_folium
from utils import read_json_file, create_map, load_css

DATA_FILE = "ess_proj_data_loc_02.json"
CSS_FILE = "static/styles.css"

def biodiversity_page():
    load_css(CSS_FILE)
    st.title("Biodiversity")
    st.markdown(
        "Biodiversity refers to the variety of life forms on Earth, encompassing different species, ecosystems, and genetic diversity. "
        "Learn more about projects focusing on preserving and understanding biodiversity."
    )

    # Load and Filter Data
    locations = read_json_file(DATA_FILE)
    topic_locations = [loc for loc in locations if "biodiversity" in loc["tags"]]

    # Map
    map_center = [30.079227, -21.750656]  # Default center
    folium_map = create_map(topic_locations, center=map_center, zoom=2)
    st_folium(folium_map, width=800, height=600)

    # Back to Main Page
    if st.button("Back to Main Page"):
        st.markdown("[Main Page](main)", unsafe_allow_html=True)

if __name__ == "__main__":
    biodiversity_page()

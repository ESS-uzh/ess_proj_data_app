import streamlit as st
from streamlit_folium import st_folium
from utils import read_json_file, create_map, load_css

DATA_FILE = "ess_proj_data_loc_02.json"
CSS_FILE = "static/styles.css"


def ecosystem_services_page():
    load_css(CSS_FILE)
    st.title("Ecosystem Services")
    st.markdown(
        "Ecosystem services are the various benefits that humans derive from healthy ecosystems. These ecosystems, when functioning well, offer such things as provision of food, natural pollination of crops, clean air and water, decomposition of wastes, or flood control."
    )

    # Load and Filter Data
    projects = read_json_file(DATA_FILE)
    topic_projects = [loc for loc in projects if "ecosystem services" in loc["tags"]]

    # Map
    map_center = [30.079227, -21.750656]  # Default center
    folium_map = create_map(topic_projects, center=map_center, zoom=2)
    st_folium(folium_map, width=800, height=600)


if __name__ == "__main__":
    ecosystem_services_page()

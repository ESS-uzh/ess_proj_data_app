import streamlit as st
from streamlit_folium import st_folium
from utils import read_json_file, create_map, load_css

DATA_FILE = "ess_proj_data_loc_02.json"
CSS_FILE = "static/styles.css"


def sustainable_development_page():
    load_css(CSS_FILE)
    st.title("Sustainable Development")
    st.markdown(
        "Sustainable development is an approach to growth and human development that aims to meet the needs of the present without compromising the ability of future generations to meet their own needs. The aim is to have a society where living conditions and resources meet human needs without undermining planetary integrity. Sustainable development aims to balance the needs of the economy, environment, and society."
    )

    # Load and Filter Data
    projects = read_json_file(DATA_FILE)
    topic_projects = [
        loc for loc in projects if "sustainable development" in loc["tags"]
    ]

    # Map
    map_center = [30.079227, -21.750656]  # Default center
    folium_map = create_map(topic_projects, center=map_center, zoom=2)
    st_folium(folium_map, width=800, height=600)


if __name__ == "__main__":
    sustainable_development_page()

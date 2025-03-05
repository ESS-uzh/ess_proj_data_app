import streamlit as st
from streamlit_folium import st_folium

# from utils import read_json_file, create_map, load_css
from utils import (
    load_css,
    resize_image,
    read_json_file,
    display_side_bar_and_map,
)

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
    projects = read_json_file(DATA_FILE)
    projects_biodiversity = [loc for loc in projects if "biodiversity" in loc["tags"]]

    if st.session_state["selected_project"] not in projects_biodiversity:
        st.session_state["selected_project"] = None
        st.session_state["search_query"] = ""  # Reset search query

    display_side_bar_and_map(
        projects_biodiversity, categories=["Location", "Participants"]
    )

    print(st.session_state["current_page"])


if __name__ == "__main__":
    biodiversity_page()

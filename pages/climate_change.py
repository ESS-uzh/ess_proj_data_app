import streamlit as st
from streamlit_folium import st_folium
from utils import (
    read_json_file,
    create_map,
    load_css,
    display_side_bar_and_map,
)

DATA_FILE = "ess_proj_data_loc_02.json"
CSS_FILE = "static/styles.css"


def climate_change_page():
    load_css(CSS_FILE)
    st.title("Climate Change")
    st.markdown(
        """Climate change is a long-term change in the average weather patterns that have come to define Earth’s local, regional and global climates. These changes have a broad range of observed effects that are synonymous with the term.

Changes observed in Earth’s climate since the mid-20th century are driven by human activities, particularly fossil fuel burning, which increases heat-trapping greenhouse gas levels in Earth’s atmosphere, raising Earth’s average surface temperature. Natural processes, which have been overwhelmed by human activities, can also contribute to climate change, including internal variability (e.g., cyclical ocean patterns like El Niño, La Niña and the Pacific Decadal Oscillation) and external forcings (e.g., volcanic activity, changes in the Sun’s energy output, variations in Earth’s orbit).

Scientists use observations from the ground, air, and space, along with computer models, to monitor and study past, present, and future climate change. Climate data records provide evidence of climate change key indicators, such as global land and ocean temperature increases; rising sea levels; ice loss at Earth’s poles and in mountain glaciers; frequency and severity changes in extreme weather such as hurricanes, heatwaves, wildfires, droughts, floods, and precipitation; and cloud and vegetation cover changes.

“Climate change” and “global warming” are often used interchangeably but have distinct meanings. Similarly, the terms "weather" and "climate" are sometimes confused, though they refer to events with broadly different spatial- and timescales."""
    )

    # Load and Filter Data
    projects = read_json_file(DATA_FILE)
    projects_climate_change = [
        loc for loc in projects if "climate change" in loc["tags"]
    ]

    # reset filters
    if st.session_state["selected_project"] not in projects_climate_change:
        st.session_state["selected_project"] = None
        st.session_state["search_query"] = ""  # Reset search query

    display_side_bar_and_map(
        projects_climate_change, categories=["Location", "Participants"]
    )


if __name__ == "__main__":
    climate_change_page()

import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import os
from PIL import Image
import base64

LOGOS_DIR = "logos_resized"
CSS_FILE = "static/styles.css"
DATA_FILE = "data/ess_proj_data_loc_02.json"


# Utility Functions
def load_css(css_file):
    with open(css_file) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    return f"data:image/png;base64,{encoded}"


def resize_image(image_path, width, height):
    image = Image.open(image_path)
    return image.resize((width, height))


def read_json_file(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
    return data["locations"]


def create_map(locations):
    map_center = [30.079227, -21.750656]
    folium_map = folium.Map(
        location=map_center,
        zoom_start=1,
        tiles="OpenStreetMap",
        width="100%",
        height="100%",
    )
    for loc in locations:
        folium.Marker(
            location=[loc["lat"], loc["lon"]],
            tooltip=loc["project"],
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(folium_map)
    return folium_map


def display_details(location):
    if location:
        st.sidebar.markdown(f"### {location['project']}")
        st.sidebar.markdown("#### Participants")
        for participant in location["participants"]:
            st.sidebar.markdown(f"- {participant}")
        st.sidebar.markdown("#### DOI Links")
        if location["doi_data"]:
            st.sidebar.markdown(f"[DOI Data]({location['doi_data']})")
        if location["doi_pub"]:
            st.sidebar.markdown(f"[DOI Publication]({location['doi_pub']})")
        st.sidebar.markdown("#### Funding")
        for logo in location["logos"]:
            logo_path = os.path.join(LOGOS_DIR, logo)
            resized_logo = resize_image(logo_path, width=110, height=80)
            st.sidebar.image(resized_logo)

        st.sidebar.markdown("#### Tags")
        tags_html = " ".join(
            f"<span class='tag'>{tag}</span>" for tag in location["tags"]
        )
        st.sidebar.markdown(tags_html, unsafe_allow_html=True)

        st.sidebar.write("---")

        st.markdown(
            f"""
        <div style="font-family: 'Courier New', monospace; color: black; font-size: 42px; font-weight:bold;">
            {location['project']}:
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
        <div style="font-family: 'Courier New', monospace; color: black; font-size: 20px;font-weight:bold; ">
            {location["description"]}
        </div>
        """,
            unsafe_allow_html=True,
        )
        if location["website"]:
            st.page_link(location["website"], label="More info", icon=":material/info:")

        # st.markdown(f"## {location['project']}")
        # st.markdown(f"### {location['description']}")
        # if location["website"]:
        #    st.markdown(f"[More info]({location['website']})")


def handle_map_click(output, locations):
    if output["last_object_clicked"]:
        clicked_lat = round(output["last_object_clicked"]["lat"], 4)
        clicked_lon = round(output["last_object_clicked"]["lng"], 4)
        for loc in locations:
            if (
                round(loc["lat"], 4) == clicked_lat
                and round(loc["lon"], 4) == clicked_lon
            ):
                return loc
    return None


def create_project_list(global_locations):
    st.markdown("### Global Projects")
    project_names = [loc["project"] for loc in global_locations]
    selected_project = st.radio(
        "Select a global project",
        project_names,
        index=0,
        label_visibility="collapsed",
    )
    for loc in global_locations:
        if loc["project"] == selected_project:
            return loc
    return None


# Main Application
def main():
    st.cache_resource.clear()
    # Use the encoded image in CSS
    background_image_css = f"""
    <style>
    .stApp {{
        background: url('{get_base64_image("logos/biodiv_background.jpeg")}') no-repeat center center fixed;
        background-size: cover;
    }}
    .stMainBlockContainer {{
        overflow: visible !important; /* Ensure content fits without clipping */
        height: auto !important;     /* Adjust to the content height */
    }}
    .leaflet-container {{
        background: transparent !important; /* Fix map background */
    }}
    </style>
    """

    locations = read_json_file(DATA_FILE)
    # Streamlit App Layout
    st.markdown(background_image_css, unsafe_allow_html=True)
    title = '<p style="font-family:sans-serif; color:Black; font-size: 42px; font-weight:bold;">ESS Projects and Data Map</p>'
    st.markdown(title, unsafe_allow_html=True)

    load_css(CSS_FILE)
    global_locations = [loc for loc in locations if loc["location"] == "global"]
    local_locations = [loc for loc in locations if loc["location"] != "global"]
    folium_map = create_map(local_locations)
    output = st_folium(folium_map, width=800, height=600)
    clicked_location = handle_map_click(output, local_locations)
    if clicked_location:
        display_details(clicked_location)
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("logos/globe.png", use_container_width=True)
    with col2:
        selected_location = create_project_list(global_locations)
    display_details(selected_location)


if __name__ == "__main__":
    main()

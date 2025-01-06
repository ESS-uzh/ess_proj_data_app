import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import os
from PIL import Image
import base64

LOGOS_DIR = "logos_resized"
CSS_FILE = "static/styles.css"
DATA_FILE = "ess_proj_data_loc_02.json"


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


def create_map(locations, center=None, zoom=1):
    map_center = center if center else [30.079227, -21.750656]
    folium_map = folium.Map(
        location=map_center,
        zoom_start=zoom,
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


def display_project_details_below_map(location):
    """Display selected project details below the map."""
    if location:
        st.markdown("---")
        st.markdown(f"### {location['project']}")
        st.markdown(f"**Participants:**")
        st.markdown(", ".join(location["participants"]))
        st.markdown(f"**Description:** {location['description']}")
        if location["doi_data"]:
            st.markdown(f"[DOI Data]({location['doi_data']})")
        if location["doi_pub"]:
            st.markdown(f"[DOI Publication]({location['doi_pub']})")
        if location["website"]:
            st.markdown(f"[More info]({location['website']})")

        st.markdown("**Funding Organizations:**")
        for logo in location["logos"]:
            logo_path = os.path.join(LOGOS_DIR, logo)
            resized_logo = resize_image(logo_path, width=110, height=80)
            st.image(resized_logo)
        st.markdown("**Tags:**")
        tags_html = " ".join(
            f"<span class='tag'>{tag}</span>" for tag in location["tags"]
        )
        st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown("---")


def display_research_topics():
    # Topics Section
    st.markdown("---")
    st.markdown("## Main Research Topics")
    col1, col2, col3, col4 = st.columns(4)
    topics = [
        {
            "name": "Biodiversity",
            "image": "topics_resized/biodiversity_img.jpg",
            "url": "https://example.com/biodiversity",
        },
        {
            "name": "Climate Change",
            "image": "topics_resized/climate_change_img.png",
            "url": "https://example.com/climate",
        },
        {
            "name": "Ecosystem Services",
            "image": "topics_resized/ecosystem_services_img.jpg",
            "url": "https://example.com/ecosystem",
        },
        {
            "name": "Sustainable Dev.",
            "image": "topics_resized/sus_dev_img.png",
            "url": "https://example.com/sustainable",
        },
    ]

    for i, topic in enumerate(topics):
        with [col1, col2, col3, col4][i]:
            resized_logo = resize_image(topic["image"], width=150, height=130)
            st.image(resized_logo)
            if st.button(f"Learn more about {topic['name']}"):
                st.markdown(
                    f"[Learn more about {topic['name']}]({topic['url']})",
                    unsafe_allow_html=True,
                )

    st.markdown("---")


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


def filter_projects(locations, query):
    """Filter projects based on a search query."""
    query = query.lower()
    return [
        loc
        for loc in locations
        if query in loc["project"].lower()
        or query in loc["description"].lower()
        or query in " ".join(loc["tags"]).lower()
        or query in loc["location"].lower()
        or any(query in participant.lower() for participant in loc["participants"])
    ]


def display_project_list(filtered_locations):
    """Display a list of projects in the sidebar."""
    st.sidebar.markdown("### Search Results")
    selected = None
    if filtered_locations:
        for loc in filtered_locations:
            if st.sidebar.button(loc["project"], key=f"sidebar-{loc['project']}"):
                selected = loc
    else:
        st.sidebar.write("No matching projects found.")
    return selected


# Main Application
def main():
    print("start")
    # st.cache_resource.clear()
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

    ## Streamlit App Layout
    st.markdown(background_image_css, unsafe_allow_html=True)
    title = '<p style="font-family:sans-serif; color:Black; font-size: 42px; font-weight:bold;">Earth System Science</p>'
    st.markdown(title, unsafe_allow_html=True)

    load_css(CSS_FILE)
    display_research_topics()

    ## Sidebar search functionality
    st.sidebar.markdown("## Filter Projects")
    search_query = st.sidebar.text_input("Use keywords:")
    filtered_locations = (
        filter_projects(locations, search_query) if search_query else locations
    )
    selected_project = display_project_list(filtered_locations)

    # Manage selected project with session state
    if "selected_project" not in st.session_state:
        st.session_state["selected_project"] = None

    if selected_project:
        st.session_state["selected_project"] = selected_project
    selected_project = st.session_state["selected_project"]

    # Determine map center and zoom based on selection
    if selected_project:
        map_center = [selected_project["lat"], selected_project["lon"]]
        map_zoom = 10
    else:
        map_center = [30.079227, -21.750656]  # Default center
        map_zoom = 1

    # Create and display the map
    folium_map = create_map(locations, center=map_center, zoom=map_zoom)
    output = st_folium(folium_map, width=800, height=600)

    # Display project details below the map (if a project is selected)
    if selected_project:
        display_project_details_below_map(selected_project)

    print("end")
    print("---")


if __name__ == "__main__":
    main()

import os
import json
import base64
from PIL import Image
import streamlit as st
import folium


def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def resize_image(image_path, width, height):
    image = Image.open(image_path)
    return image.resize((width, height))


def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    return f"data:image/png;base64,{encoded}"


def read_json_file(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
    return data["projects"]


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


def display_project_details_below_map(location, logos_dir):
    """Display selected project details below the map."""
    if location:

        st.markdown("---")
        st.markdown(f"### {location['project']}")
        st.markdown(f"**Participants:**")
        st.markdown(", ".join(location["participants"]))

        # Add extra space between sections
        st.markdown("&nbsp;", unsafe_allow_html=True)

        st.markdown(f"**Description:** {location['description']}")
        if location["doi_data"]:
            st.markdown(f"[DOI Data]({location['doi_data']})")
        if location["doi_pub"]:
            st.markdown(f"[DOI Publication]({location['doi_pub']})")
        if location["website"]:
            st.markdown(f"[More info]({location['website']})")

        # Add extra space between sections
        st.markdown("&nbsp;", unsafe_allow_html=True)

        st.markdown("**Funding Organizations:**")
        for logo in location["logos"]:
            logo_name, logo_description = logo
            logo_path = os.path.join(logos_dir, logo_name)
            resized_logo = resize_image(logo_path, width=110, height=80)
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(resized_logo)
            with col2:
                # Add extra space between sections
                st.markdown("&nbsp;", unsafe_allow_html=True)
                st.markdown(logo_description)

        # Add extra space between sections
        st.markdown("&nbsp;", unsafe_allow_html=True)

        st.markdown("**Tags:**")
        tags_html = " ".join(
            f"<span class='tag'>{tag}</span>" for tag in location["tags"]
        )
        st.markdown(tags_html, unsafe_allow_html=True)

        st.markdown("---")


def filter_projects(projects, category, query):
    """Filter projects based on selected category and query."""
    query = query.lower()
    if category == "Tags":
        return [loc for loc in projects if query in " ".join(loc["tags"]).lower()]
    elif category == "Location":
        return [loc for loc in projects if query in loc["location"].lower()]
    elif category == "Participants":
        return [
            loc
            for loc in projects
            if any(query in participant.lower() for participant in loc["participants"])
        ]
    elif category == "Project Name":
        return [loc for loc in projects if query in loc["project"].lower()]
    return projects


def get_available_keywords(projects, category):
    """Retrieve unique keywords for the selected category."""
    if category == "Tags":
        keywords = {tag for loc in projects for tag in loc["tags"]}
    elif category == "Location":
        keywords = {loc["location"] for loc in projects}
    elif category == "Participants":
        keywords = {
            participant for loc in projects for participant in loc["participants"]
        }
    else:
        keywords = set()
    return sorted(keywords)  # Sort for a cleaner display


def display_project_list(filtered_projects):
    """Display a list of projects in the sidebar."""
    st.sidebar.markdown("### Search Results")
    selected = None
    if filtered_projects:
        for loc in filtered_projects:
            if st.sidebar.button(loc["project"], key=f"sidebar-{loc['project']}"):
                selected = loc
    else:
        st.sidebar.write("No matching projects found.")
    return selected

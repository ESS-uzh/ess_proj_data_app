import os
import json
import base64
from PIL import Image
import streamlit as st
import folium
from streamlit_folium import st_folium

LOGOS_DIR = "logos_resized"


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


def read_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
    return data


def read_json_file(json_file):
    return read_json(json_file)["projects"]


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
        if "polygon" in loc and loc["polygon"]:
            # Load the geojson file
            data = read_json(f"polygons/{loc['polygon']}")
            polygon = data["features"][0]["geometry"]["coordinates"]
            # Add a Polygon
            folium.Polygon(
                locations=polygon,  # List of [lat, lon] pairs
                color="blue",
                fill=True,
                fill_color="cyan",
                fill_opacity=0.4,
                tooltip=loc["project"],  # Tooltip on hover
            ).add_to(folium_map)
        elif loc["lat"] and loc["lon"]:
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
        st.markdown(location["description"])
        if location["doi_data"]:
            st.markdown(f"[DOI Data]({location['doi_data']})")
        if location["doi_pub"]:
            st.markdown(f"[DOI Publication]({location['doi_pub']})")
        if location["website"]:
            st.markdown(f"[More info]({location['website']})")

        # Add extra space between sections
        st.markdown("&nbsp;", unsafe_allow_html=True)

        st.markdown(
            '<p style="font-family:sans-serif; color:White; font-size: 16px; font-weight:bold;">Participants:</p>',
            unsafe_allow_html=True,
        )
        st.markdown(", ".join(location["participants"]))

        # Add extra space between sections
        st.markdown("&nbsp;", unsafe_allow_html=True)

        st.markdown(
            '<p style="font-family:sans-serif; color:White; font-size: 16px; font-weight:bold;">Funding Organizations:</p>',
            unsafe_allow_html=True,
        )
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

        st.markdown(
            '<p style="font-family:sans-serif; color:White; font-size: 16px; font-weight:bold;">Tags:</p>',
            unsafe_allow_html=True,
        )
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
        return [
            prj
            for prj in projects
            if any(query in location.lower() for location in prj["location"])
        ]
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
        keywords = {loc for prj in projects for loc in prj["location"]}
    elif category == "Participants":
        keywords = {
            participant for loc in projects for participant in loc["participants"]
        }
    else:
        keywords = set()
    return sorted(keywords, key=str.lower)  # Sort for a cleaner display


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


def display_side_bar_and_map(projects, categories=["Tags", "Location", "Participants"]):
    # Clear Filters Button
    if st.sidebar.button("Clear Filters"):
        st.session_state["selected_project"] = None
        st.session_state["search_query"] = ""  # Reset search query
        filtered_projects = projects
    else:
        # Maintain filtered locations if not resetting
        filtered_projects = (
            projects
            if "filtered_projects" not in st.session_state
            else st.session_state["filtered_projects"]
        )

    ## Sidebar search functionality
    st.sidebar.markdown("## Filter Projects")
    category = st.sidebar.selectbox(
        "Select a category to filter by:",
        categories,
    )

    # Display available keywords for the selected category
    available_keywords = get_available_keywords(projects, category)
    if available_keywords:
        selected_keyword = st.sidebar.selectbox(
            f"Available {category.lower()}:", available_keywords
        )
    else:
        st.sidebar.write(f"No available {category.lower()} found.")
        selected_keyword = None

    # Perform filtering based on the selected category and keyword
    if selected_keyword:
        filtered_projects = filter_projects(projects, category, selected_keyword)
    else:
        filtered_projects = projects

    selected_project = display_project_list(filtered_projects)

    # Manage selected project with session state
    if "selected_project" not in st.session_state:
        st.session_state["selected_project"] = None

    if selected_project:
        st.session_state["selected_project"] = selected_project
    selected_project = st.session_state["selected_project"]

    # Determine map center and zoom based on selection
    if selected_project:
        if selected_project["lat"] and selected_project["lon"]:
            map_center = [selected_project["lat"], selected_project["lon"]]
            map_zoom = 5
        else:
            map_center = None
            map_zoom = 2
    else:
        map_center = [30.079227, -21.750656]  # Default center
        map_zoom = 2

    # Create and display the map
    folium_map = create_map(projects, center=map_center, zoom=map_zoom)
    output = st_folium(folium_map, width=800, height=600)

    # Display project details below the map (if a project is selected)
    if selected_project:
        display_project_details_below_map(selected_project, LOGOS_DIR)

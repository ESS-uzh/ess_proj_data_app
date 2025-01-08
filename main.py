import streamlit as st
from streamlit_folium import st_folium
from utils import (load_css, resize_image,
                   get_base64_image, 
                   read_json_file, 
                   create_map,
                   display_project_details_below_map,
                   filter_projects, 
                   display_project_list)
from pages.biodiversity import biodiversity_page

LOGOS_DIR = "logos_resized"
CSS_FILE = "static/styles.css"
DATA_FILE = "ess_proj_data_loc_02.json"

TOPIC_INFO = {
    "Biodiversity": {"image": "topics_resized/biodiversity_img.jpg", "page": "biodiversity"},
    "Climate Change": {"image": "topics_resized/climate_change_img.png", "page": "climate_change"},
    "Ecosystem Services": {"image": "topics_resized/ecosystem_services_img.jpg", "page": "ecosystem_services"},
    "Sustainable Development": {"image": "topics_resized/sus_dev_img.png", "page": "sustainable_dev"},
}
def home_page():
    title = '<p style="font-family:sans-serif; color:White; font-size: 42px; font-weight:bold;">Earth System Science</p>'
    st.markdown(title, unsafe_allow_html=True)
    # Topics Section
    st.markdown("---")
    st.markdown("## Main Research Topics")
    
    cols = st.columns(len(TOPIC_INFO))

    for idx, (topic, info) in enumerate(TOPIC_INFO.items()):
        with cols[idx]:
            resized_image = resize_image(info["image"], width=150, height=130)
            st.image(resized_image)
            st.markdown(f"{topic}")
            #if st.button(f"Explore {topic}", key=f"button_{topic}"):
            #    st.markdown(f"[Explore {topic}]({info['page']})", unsafe_allow_html=True)

    st.markdown("---")
    
    #background_image_css = f"""
    # <style>
    # .stApp {{
    #    background: url('{get_base64_image("logos/biodiv_background.jpeg")}') no-repeat center center fixed;
    #    background-size: cover;
    # }}
    # .stMainBlockContainer {{
    #    overflow: visible !important; /* Ensure content fits without clipping */
    #    height: auto !important;     /* Adjust to the content height */
    # }}
    # .leaflet-container {{
    #    background: transparent !important; /* Fix map background */
    # }}
    # </style>
    # """

    locations = read_json_file(DATA_FILE)

    ### Streamlit App Layout
    #st.markdown(background_image_css, unsafe_allow_html=True)


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
        map_zoom = 2

    # Create and display the map
    folium_map = create_map(locations, center=map_center, zoom=map_zoom)
    output = st_folium(folium_map, width=800, height=600)

    # Display project details below the map (if a project is selected)
    if selected_project:
        display_project_details_below_map(selected_project, LOGOS_DIR)




# Main Application
def main():
    print("start")
    load_css(CSS_FILE)
    # Ensure "current_page" exists in session state
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "main"  # Default to main page

    # Navigation Logic
    if st.session_state["current_page"] == "main":
        home_page()
    elif st.session_state["current_page"] == "biodiversity":
        biodiversity_page()
    #elif st.session_state["current_page"] == "climate_change":
    #    climate_change_page()
    #elif st.session_state["current_page"] == "ecosystem_services":
    #    ecosystem_services_page()
    #elif st.session_state["current_page"] == "sustainable_dev":
    #    sustainable_dev_page()
    
    # Use the encoded image in CSS
    print("end")
    print("---")


if __name__ == "__main__":
    main()

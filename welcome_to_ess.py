import streamlit as st
from utils import (
    load_css,
    resize_image,
    read_json_file,
    display_side_bar_and_map,
)

CSS_FILE = "static/styles.css"
DATA_FILE = "ess_proj_data_loc_02.json"

TOPIC_INFO = {
    "biodiversity": {
        "image": "topics_resized/biodiversity_img.jpg",
        "page": "biodiversity",
    },
    "climate change": {
        "image": "topics_resized/climate_change_img.png",
        "page": "climate_change",
    },
    "ecosystem services": {
        "image": "topics_resized/ecosystem_services_img.jpg",
        "page": "ecosystem_services",
    },
    "social ecological system": {
        "image": "topics_resized/sus_dev_img.png",
        "page": "social_ecological_system",
    },
}


def home_page():
    # Title and logo
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(
            '<p style="font-family:sans-serif; color:White; font-size: 42px; font-weight:bold;">Earth System Science</p>',
            unsafe_allow_html=True,
        )
    with col2:
        st.image("/home/diego/work/dev/github/ess_proj_data_app/logos/UZH.jpg")
    # Topics Section
    st.markdown("---")
    st.markdown("## Main Research Topics")

    cols = st.columns(len(TOPIC_INFO))

    for idx, (topic, info) in enumerate(TOPIC_INFO.items()):
        with cols[idx]:
            resized_image = resize_image(info["image"], width=150, height=130)
            st.image(resized_image)
            # Make the topic name clickable
            if st.button(topic, key=f"btn_{info['page']}"):
                st.switch_page(f"pages/{info['page']}.py")
                st.session_state["current_page"] = info["page"]
                st.rerun()  # Refresh the app

    st.markdown("---")

    projects = read_json_file(DATA_FILE)
    display_side_bar_and_map(projects)


# Main Application
def main():
    st.set_page_config(page_title="ESS App", page_icon="🌍")
    print("start")
    load_css(CSS_FILE)
    # Ensure "current_page" exists in session state
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "main"  # Default to main page

    # Navigation Logic
    if st.session_state["current_page"] == "main":
        home_page()

    # Use the encoded image in CSS
    print(st.session_state["current_page"])
    print("end")
    print("---")


if __name__ == "__main__":
    main()

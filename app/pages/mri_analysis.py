import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MRI Analysis | NeuroMind",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2.5rem;
    padding-left: 4rem;
    padding-right: 4rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit automatic navigation */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f3f5f9;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
    padding-left: 1.3rem;
    padding-right: 1.3rem;
}

/* Page title */
.page-title {
    font-size: 42px;
    font-weight: 750;
    color: #292d3d;
    margin-bottom: 5px;
}

.page-subtitle {
    font-size: 19px;
    color: #68748b;
    margin-bottom: 30px;
}

/* Upload heading */
.upload-heading {
    font-size: 26px;
    font-weight: 700;
    color: #292d3d;
}

.upload-description {
    font-size: 17px;
    color: #68748b;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div style="font-size:28px; font-weight:750; '
        'color:#292d3d; margin-bottom:35px;">'
        '🧠 NeuroMind'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Navigation")

    st.page_link(
        "main.py",
        label="Dashboard",
        icon="🏠"
    )

    st.page_link(
        "pages/behavioral_assessment.py",
        label="Behavioral Assessment",
        icon="📋"
    )

    st.page_link(
        "pages/mri_analysis.py",
        label="MRI Analysis",
        icon="🧠"
    )

    st.page_link(
        "pages/face_body_analysis.py",
        label="Face / Body Analysis",
        icon="👤"
    )

    st.page_link(
        "pages/results.py",
        label="Results",
        icon="📊"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="page-title">MRI Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Upload an MRI image for analysis'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# UPLOAD SECTION
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="upload-heading">Upload MRI Image</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="upload-description">'
        'Select an MRI image from your device.'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose an MRI image",
        type=["jpg", "jpeg", "png"]
    )


# =========================================================
# PREVIEW
# =========================================================

if uploaded_file is not None:

    st.markdown("### MRI Preview")

    st.image(
        uploaded_file,
        caption="Uploaded MRI Image",
        use_container_width=True
    )

    st.markdown("")


    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    if st.button(
        "🧠 Analyze MRI →",
        use_container_width=True
    ):

        st.session_state.mri_result = "Completed"

        st.success(
            "MRI image analysis completed successfully."
        )
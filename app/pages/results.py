import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Results | NeuroMind",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2.5rem;
    padding-left: 4rem;
    padding-right: 4rem;
    padding-bottom: 3rem;
}

/* Hide automatic navigation */
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

/* Title */
.page-title {
    font-size: 42px;
    font-weight: 750;
    color: #292d3d;
    margin-bottom: 5px;
}

.page-subtitle {
    font-size: 19px;
    color: #68748b;
    margin-bottom: 35px;
}

/* Result headings */
.result-title {
    font-size: 23px;
    font-weight: 700;
    color: #292d3d;
}

.result-value {
    font-size: 18px;
    color: #68748b;
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
        icon="🎥"
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
    '<div class="page-title">Results</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'View the results of the completed analyses'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# GET RESULTS
# =========================================================

behavior_result = st.session_state.get(
    "behavior_result",
    None
)

mri_result = st.session_state.get(
    "mri_result",
    None
)

face_result = st.session_state.get(
    "face_result",
    None
)


# =========================================================
# BEHAVIORAL RESULT
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="result-title">'
        '📋 Behavioral Assessment'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    if behavior_result:

        st.success(
            f"Result: {behavior_result}"
        )

    else:

        st.info(
            "Behavioral assessment has not been completed yet."
        )


# =========================================================
# MRI RESULT
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="result-title">'
        '🧠 MRI Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    if mri_result:

        st.success(
            f"Result: {mri_result}"
        )

    else:

        st.info(
            "MRI analysis has not been completed yet."
        )


# =========================================================
# FACE RESULT
# =========================================================

with st.container(border=True):

    st.markdown(
        '<div class="result-title">'
        '🎥 Face / Body Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    if face_result:

        st.success(
            f"Result: {face_result}"
        )

    else:

        st.info(
            "Face / Body analysis has not been completed yet."
        )


# =========================================================
# OVERALL STATUS
# =========================================================

st.markdown("")

completed = sum([
    behavior_result is not None,
    mri_result is not None,
    face_result is not None
])

st.progress(
    completed / 3
)

st.write(
    f"{completed} of 3 analyses completed"
)
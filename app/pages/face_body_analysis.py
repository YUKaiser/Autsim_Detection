import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Face / Body Analysis | NeuroMind",
    page_icon="🎥",
    layout="wide"
)


# =========================================================
# CAMERA PROCESSOR
# =========================================================

class FaceCameraProcessor(VideoProcessorBase):

    def __init__(self):
        self.latest_frame = None

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        self.latest_frame = img.copy()

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
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

/* Camera heading */
.camera-title {
    font-size: 26px;
    font-weight: 700;
    color: #292d3d;
}

.camera-description {
    font-size: 17px;
    color: #68748b;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:750;
            color:#292d3d;
            margin-bottom:35px;
        ">
        🧠 NeuroMind
        </div>
        """,
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
# SESSION STATE
# =========================================================

if "captured_face" not in st.session_state:
    st.session_state.captured_face = None

if "face_camera_error" not in st.session_state:
    st.session_state.face_camera_error = None

if "face_result" not in st.session_state:
    st.session_state.face_result = None


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="page-title">Face / Body Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Capture an image using the live camera'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# LIVE CAMERA
# =========================================================

st.markdown(
    '<div class="camera-title">Live Camera</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="camera-description">'
    'Allow camera access and position the face clearly inside the camera view.'
    '</div>',
    unsafe_allow_html=True
)


ctx = webrtc_streamer(
    key="face-camera",
    video_processor_factory=FaceCameraProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)


# =========================================================
# CAPTURE BUTTON
# =========================================================

if st.button(
    "📸 Capture Image",
    use_container_width=True
):

    if (
        ctx.video_processor is not None
        and ctx.video_processor.latest_frame is not None
    ):

        frame_bgr = ctx.video_processor.latest_frame.copy()

        frame_rgb = cv2.cvtColor(
            frame_bgr,
            cv2.COLOR_BGR2RGB
        )

        st.session_state.captured_face = frame_rgb
        st.session_state.face_camera_error = None

        st.rerun()

    else:

        st.session_state.face_camera_error = (
            "No camera frame is available yet. "
            "Start the camera and try again."
        )


# =========================================================
# CAMERA ERROR
# =========================================================

if st.session_state.face_camera_error:

    st.warning(
        st.session_state.face_camera_error
    )


# =========================================================
# CAPTURED IMAGE
# =========================================================

captured_face = st.session_state.captured_face


if captured_face is not None:

    st.markdown("### Captured Image")

    st.image(
        captured_face,
        caption="Captured Face Image",
        use_container_width=True
    )

    st.markdown("")


    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    if st.button(
        "🧠 Analyze Captured Face →",
        use_container_width=True
    ):

        # Temporary frontend result
        st.session_state.face_result = "Completed"

        st.success(
            "Face analysis completed successfully."
        )


    # =====================================================
    # CAPTURE AGAIN
    # =====================================================

    if st.button(
        "🔄 Capture Again",
        use_container_width=True
    ):

        st.session_state.captured_face = None
        st.session_state.face_camera_error = None
        st.session_state.face_result = None

        st.rerun()
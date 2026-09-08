import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Behavioral Assessment | NeuroMind",
    page_icon="📋",
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

/* Main title */
.assessment-title {
    font-size: 42px;
    font-weight: 750;
    color: #292d3d;
    margin-bottom: 5px;
}

.assessment-subtitle {
    font-size: 19px;
    color: #68748b;
    margin-bottom: 30px;
}

/* Question number */
.question-number {
    font-size: 18px;
    font-weight: 650;
    color: #68748b;
}

/* Question */
.question-text {
    font-size: 25px;
    font-weight: 650;
    color: #292d3d;
    line-height: 1.5;
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
        icon="👤"
    )

    st.page_link(
        "pages/results.py",
        label="Results",
        icon="📊"
    )


# =========================================================
# SESSION STATE
# =========================================================

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "behavior_result" not in st.session_state:
    st.session_state.behavior_result = None


# =========================================================
# QUESTIONS
# =========================================================

questions = [
    "Does the child have difficulty maintaining eye contact?",
    "Does the child have difficulty responding when their name is called?",
    "Does the child prefer playing alone rather than with others?",
    "Does the child have difficulty communicating with others?",
    "Does the child repeat certain words or phrases frequently?",
    "Does the child show repetitive body movements?",
    "Does the child become uncomfortable with changes in routine?",
    "Does the child show unusual sensitivity to sounds or textures?",
    "Does the child have difficulty understanding social situations?",
    "Does the child have difficulty expressing emotions?"
]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="assessment-title">Behavioral Assessment</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="assessment-subtitle">'
    'Complete the behavioral questionnaire'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# PROGRESS
# =========================================================

current = st.session_state.question_index
total = len(questions)

st.progress(
    (current + 1) / total
)

st.markdown(
    f'<div class="question-number">'
    f'Question {current + 1} of {total}'
    f'</div>',
    unsafe_allow_html=True
)


# =========================================================
# QUESTION CARD
# =========================================================

with st.container(border=True):

    st.markdown(
        f'<div class="question-number">'
        f'Question {current + 1}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    st.markdown(
        f'<div class="question-text">'
        f'{questions[current]}'
        f'</div>',
        unsafe_allow_html=True
    )


# =========================================================
# ANSWER
# =========================================================

st.markdown("")

st.markdown("### Select your answer:")

previous_answer = st.session_state.answers.get(current)

answer = st.radio(
    "Answer",
    ["Yes", "No"],
    index=(
        ["Yes", "No"].index(previous_answer)
        if previous_answer in ["Yes", "No"]
        else None
    ),
    key=f"answer_{current}",
    label_visibility="collapsed"
)


# Save answer
if answer:
    st.session_state.answers[current] = answer


# =========================================================
# NAVIGATION BUTTONS
# =========================================================

col1, col2 = st.columns(2)


# Previous
with col1:

    if current > 0:

        if st.button(
            "← Previous",
            use_container_width=True
        ):

            st.session_state.question_index -= 1
            st.rerun()


# Next / Submit
with col2:

    if current < total - 1:

        if st.button(
            "Next →",
            use_container_width=True
        ):

            if answer:

                st.session_state.question_index += 1
                st.rerun()

            else:

                st.warning("Please select an answer.")

    else:

        if st.button(
            "Submit Assessment →",
            use_container_width=True
        ):

            if answer:

                st.session_state.behavior_result = "Completed"

                st.success(
                    "Behavioral assessment completed successfully."
                )

            else:

                st.warning("Please select an answer.")
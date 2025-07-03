import streamlit as st
import pickle
import pandas as pd

# Load data
codejobs = pickle.load(open('codejobs.pkl', 'rb'))

# Set layout
st.set_page_config(layout="wide")
st.set_page_config(page_title="Code Jobs Nepal")

# Set layout
st.set_page_config(layout="wide")
st.set_page_config(page_title="Code Jobs Nepal")

# Inject Open Graph meta tags for LinkedIn and social previews
st.markdown(
    """
    <meta property="og:title" content="Code Jobs Nepal" />
    <meta property="og:description" content="Explore and search for coding jobs in Nepal." />
    <meta property="og:image" content="./codejobslogo.png" />
    <meta property="og:url" content="https://codejobsnepal.streamlit.app" />
    """,
    unsafe_allow_html=True
)


# Session state setup
if 'selected_card_job' not in st.session_state:
    st.session_state.selected_card_job = None
if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False
if 'show_about' not in st.session_state:
    st.session_state.show_about = False

st.markdown(
    """
    <style>
    div.stButton > button:hover,
    div.stButton > button:focus,
    div.stButton > button:focus-visible {
        border-color: #a7a7a7 !important;  /* change the border color */
        color: #555555 !important;         /* text color */
        outline: none !important;          /* remove default outline */
        box-shadow: none !important;       /* remove default shadow */
        background: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# === TITLE AND ABOUT BUTTON SIDE-BY-SIDE ===
col1, col2 = st.columns([7, 1])

with col1:
    st.markdown(
        "<img src='https://raw.githubusercontent.com/sandeshbhattarai101/CodeJobsNepal/main/codejobslogo.png' style='height: 2.2em;'>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown("<div style='height: 1.8em;'></div>", unsafe_allow_html=True)
    about_clicked = st.button("About Us", key="about_btn")


if about_clicked:
    st.session_state.show_about = True

# === ABOUT US SECTION ===
if st.session_state.show_about:

    if st.button("⬅ Back"):
        st.session_state.show_about = False
        st.rerun()

    st.subheader("About This Project")
    st.markdown("""
    This website scrapes data from **[merojob.com](https://merojob.com)** and presents it in a user-friendly format here.  
    It is built purely as a part of my learning process, where I aim to apply my skills by working on real-world projects that feel meaningful and practical.

    ---

    ### About Me  
    I’m **Sandesh Bhattarai**, an aspiring developer with a deep interest in **data science** and **machine learning**.  
    I'm passionate about building tools that connect data with real-world applications and help users interact with information more effectively.

    🔗 [Visit My GitHub Profile](https://github.com/sandeshbhattarai101)
    """, unsafe_allow_html=True)

    st.stop()

# === SEARCH SECTION ===
selected_job_name = st.selectbox('Search for coding jobs', codejobs['Job Title'].unique())

def fetch_job(job_title):
    return codejobs[codejobs['Job Title'] == job_title]

if st.button('Search'):
    st.session_state.search_triggered = True

if st.session_state.search_triggered:
    data = fetch_job(selected_job_name)
    if data.empty:
        st.warning("No jobs found.")
    else:
        for idx, (_, row) in enumerate(data.iterrows()):
            close_key = f"close_btn_{idx}"
            with st.container():
                st.markdown(
                    """
                    <style>
                        .job-card {
                            background-color: #f9f9f9;
                            padding: 20px;
                            border-radius: 15px;
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                            margin-bottom: 20px;
                            position: relative;
                        }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                cols = st.columns([11, 1])
                with cols[1]:
                    if st.button("×", key=close_key):
                        st.session_state.search_triggered = False
                        st.rerun()

                st.markdown(
                    f"""
                    <div class="job-card">
                        <img src="{row.get('Company Image', '')}" alt="Company Logo" style="width: 100px; height: auto; margin-bottom: 10px;">
                        <h4 style="margin-bottom: 10px;">{row['Job Title']} at {row.get('Company', 'Unknown')}</h4>
                        <p><strong>Company:</strong> {row.get('Company Name', 'N/A')}</p>
                        <p><strong>Job Category:</strong> {row.get('Job Category', 'N/A')}</p>
                        <p><strong>Level:</strong> {row.get('Job Level', 'N/A')}</p>
                        <p><strong>Number of Vacancy:</strong> {row.get('No. of Vacancy/s', 'N/A')}</p>
                        <p><strong>Employment Type:</strong> {row.get('Employment Type', 'N/A')}</p>
                        <p><strong>Location:</strong> {row.get('Job Location', 'N/A')}</p>
                        <p><strong>Salary:</strong> {row.get('Offered Salary', 'N/A')}</p>
                        <p><strong>Deadline:</strong> {row.get('Apply Before(Deadline)', 'N/A')}</p>
                        <p><strong>Education Level:</strong> {row.get('Education Level', 'N/A')}</p>
                        <p><strong>Experience Requirement:</strong> {row.get('Experience Required', 'N/A')}</p>
                        <p><strong>Professional Skill Requirement:</strong> {row.get('Professional Skill Required', 'N/A')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# === Handle Query Parameter Clicks ===
query_params = st.query_params
if "selected" in query_params:
    selected_key = query_params["selected"]
    job_row = codejobs.iloc[int(selected_key)]
    st.session_state.selected_card_job = job_row['Job Title']
    st.query_params.clear()
    st.rerun()

# === Selected Job Card View ===
if st.session_state.selected_card_job:
    if st.button("⬅ Back to all jobs"):
        st.session_state.selected_card_job = None
        st.rerun()

    st.subheader(f"Job Details: {st.session_state.selected_card_job}")
    job_data = fetch_job(st.session_state.selected_card_job)
    for _, row in job_data.iterrows():
        st.markdown(
            f"""
            <div style="
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            ">
                <img src="{row.get('Company Image', '')}" alt="Company Logo" style="width: 100px; height: auto; margin-bottom: 10px;">
                <h4 style="margin-bottom: 10px;">{row['Job Title']} at {row.get('Company', 'Unknown')}</h4>
                <p><strong>Company:</strong> {row.get('Company Name', 'N/A')}</p>
                <p><strong>Job Category:</strong> {row.get('Job Category', 'N/A')}</p>
                <p><strong>Level:</strong> {row.get('Job Level', 'N/A')}</p>
                <p><strong>Number of Vacancy:</strong> {row.get('No. of Vacancy/s', 'N/A')}</p>
                <p><strong>Employment Type:</strong> {row.get('Employment Type', 'N/A')}</p>
                <p><strong>Location:</strong> {row.get('Job Location', 'N/A')}</p>
                <p><strong>Salary:</strong> {row.get('Offered Salary', 'N/A')}</p>
                <p><strong>Deadline:</strong> {row.get('Apply Before(Deadline)', 'N/A')}</p>
                <p><strong>Education Level:</strong> {row.get('Education Level', 'N/A')}</p>
                <p><strong>Experience Requirement:</strong> {row.get('Experience Required', 'N/A')}</p>
                <p><strong>Professional Skill Requirement:</strong> {row.get('Professional Skill Required', 'N/A')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# === All Job Cards ===
else:
    st.subheader("All Available Jobs")
    cols = st.columns(3)
    for idx, (_, row) in enumerate(codejobs.iterrows()):
        col = cols[idx % 3]
        with col:
            job_card_html = f"""
            <a href="/?selected={idx}" target="_self" style="text-decoration: none; color: inherit;">
                <div style="
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 15px;
                    text-align: center;
                    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
                    transition: 0.3s;
                    cursor: pointer;
                ">
                    <img src="{row.get('Company Image', '')}" style="width:80px;height:auto;margin-bottom:10px;" />
                    <h5 style="margin-bottom:5px;">{row['Job Title']}</h5>
                    <p style="color:gray;margin-bottom:0;">{row.get('Company Name', 'N/A')}</p>
                </div>
            </a>
            """
            st.markdown(job_card_html, unsafe_allow_html=True)


from resume_builder import generate_resume_pdf
import streamlit as st
import tempfile
from pathlib import Path

from resume_parser import extract_resume_text
from matcher import analyze_resume



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ResumeIQ | AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #090d18;
    --surface: #111827;
    --surface-2: #151e30;
    --border: rgba(148, 163, 184, 0.16);
    --text: #f1f5f9;
    --muted: #94a3b8;
    --accent: #a78bfa;
    --blue: #60a5fa;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%,
            rgba(99, 102, 241, 0.14), transparent 36%),
        radial-gradient(ellipse at 90% 15%,
            rgba(139, 92, 246, 0.10), transparent 30%),
        var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

.block-container {
    max-width: 1120px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.6px;
    color: var(--text);
}

p, label, li {
    color: #d4dbea;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

/* Brand bar */
.brandbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 25px;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border);
}

.brand-left {
    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    color: white;
    font-size: 21px;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    box-shadow: 0 6px 24px rgba(99, 102, 241, .24);
}

.brand-name {
    font-family: 'Manrope', sans-serif;
    font-size: 19px;
    font-weight: 800;
    color: #f8fafc;
}

.brand-caption {
    font-size: 11px;
    color: #94a3b8;
    letter-spacing: 1.3px;
}

.status-pill {
    border: 1px solid rgba(167, 139, 250, .25);
    border-radius: 999px;
    padding: 7px 12px;
    color: #c4b5fd;
    background: rgba(139, 92, 246, .08);
    font-size: 12px;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    padding: 36px;
    margin-bottom: 28px;
    border-radius: 24px;
    border: 1px solid rgba(167, 139, 250, .22);
    background: linear-gradient(
        125deg,
        rgba(30, 41, 75, .96),
        rgba(17, 24, 39, .96) 65%,
        rgba(37, 24, 67, .86)
    );
    box-shadow: 0 20px 65px rgba(0, 0, 0, .18);
}

.hero::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -80px;
    top: -100px;
    border-radius: 50%;
    border: 1px solid rgba(167, 139, 250, .15);
    box-shadow:
        0 0 0 30px rgba(167, 139, 250, .025),
        0 0 0 60px rgba(167, 139, 250, .02);
    pointer-events: none;
}

.hero .brand {
    color: #c4b5fd;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.2px;
}

.hero h1 {
    font-size: clamp(30px, 4.3vw, 48px);
    line-height: 1.15;
    font-weight: 800;
    margin: 17px 0 12px;
    color: #fff;
}

.muted {
    color: #aebbd0;
    font-size: 15px;
    line-height: 1.8;
    max-width: 660px;
}

/* Section headings */
.section-title {
    font-family: 'Manrope', sans-serif;
    color: #f1f5f9;
    font-size: 23px;
    font-weight: 750;
    letter-spacing: -.5px;
    margin: 34px 0 17px;
}

.section-kicker {
    color: #a78bfa;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.8px;
}

/* Panels */
.panel, .metric-card {
    background: linear-gradient(
        145deg,
        rgba(21, 30, 48, .96),
        rgba(15, 23, 42, .96)
    );
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 23px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, .10);
    transition: border-color .2s ease,
                transform .2s ease;
}

.panel:hover, .metric-card:hover {
    border-color: rgba(167, 139, 250, .38);
    transform: translateY(-2px);
}

.panel h3 {
    font-size: 17px;
    font-weight: 700;
    margin-top: 0;
}

.metric-card {
    min-height: 120px;
}

.metric-label {
    color: #94a3b8;
    font-size: 11px;
    letter-spacing: 1.1px;
    font-weight: 700;
    margin-bottom: 13px;
}

.metric-value {
    font-family: 'Manrope', sans-serif;
    color: #f8fafc;
    font-size: 32px;
    line-height: 1.2;
    font-weight: 800;
}

/* Forms */
[data-testid="stFileUploader"] {
    padding: 15px;
    border: 1px dashed rgba(167, 139, 250, .4);
    border-radius: 15px;
    background: rgba(139, 92, 246, .045);
}

[data-testid="stFileUploader"]:hover {
    border-color: #a78bfa;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background: #0d1423 !important;
    color: #f1f5f9 !important;
    border: 1px solid #29364d !important;
    border-radius: 12px !important;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 1px #8b5cf6 !important;
}

[data-testid="stForm"] {
    background: rgba(17, 24, 39, .65);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    border-radius: 12px !important;
    min-height: 46px;
    font-weight: 700 !important;
    transition: all .2s ease !important;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    color: white !important;
    background: linear-gradient(100deg, #7c3aed, #4f46e5) !important;
    border: 1px solid rgba(196, 181, 253, .25) !important;
    box-shadow: 0 5px 18px rgba(99, 102, 241, .18);
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover,
.stDownloadButton > button[kind="primary"]:hover {
    filter: brightness(1.15);
    box-shadow: 0 8px 24px rgba(99, 102, 241, .3);
    transform: translateY(-1px);
}

.stDownloadButton > button[kind="secondary"] {
    background: #172033;
    border: 1px solid #34435c;
    color: #e2e8f0;
}

/* Skill badges */
.skill {
    display: inline-block;
    padding: 7px 11px;
    margin: 4px 4px 4px 0;
    border-radius: 9px;
    font-size: 12px;
    font-weight: 600;
    background: rgba(16, 185, 129, .09);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, .22);
}

.missing {
    background: rgba(251, 146, 60, .08);
    color: #fdba74;
    border-color: rgba(251, 146, 60, .22);
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #8b5cf6, #60a5fa);
    border-radius: 20px;
}

/* Feedback and footer */
[data-testid="stAlert"] {
    border-radius: 12px;
}

.footer-note {
    text-align: center;
    color: #718096;
    font-size: 12px;
    line-height: 1.9;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid var(--border);
}

hr {
    border-color: var(--border) !important;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    .hero {
        padding: 24px;
        border-radius: 18px;
    }

    .brandbar {
        gap: 10px;
    }

    .status-pill {
        font-size: 10px;
    }

    [data-testid="stForm"] {
        padding: 14px;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brandbar">
    <div class="brand-left">
        <div class="brand-icon">✦</div>
        <div>
            <div class="brand-name">ResumeIQ</div>
            <div class="brand-caption">CAREER INTELLIGENCE</div>
        </div>
    </div>
    <div class="status-pill">✦ Smart Resume Analysis</div>
</div>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="brand">RESUMEIQ · CAREER TOOLS</div>
    <h1>Make your next application stronger.</h1>
    <div class="muted">
        Analyze your resume against a job description.
        Discover relevant skills, identify potential gaps,
        and prepare for your next opportunity.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- INPUT FORM ----------------
st.markdown('<div class="section-title">01 · Your documents</div>',
            unsafe_allow_html=True)

with st.form("resume_analysis_form"):
    left, right = st.columns([0.9, 1.1], gap="large")

    with left:
        st.markdown("### Resume")
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf"],
            help="Use a PDF containing selectable text."
        )

        if uploaded_file:
            st.caption(
                f"Selected: {uploaded_file.name} "
                f"({uploaded_file.size / 1024:.1f} KB)"
            )

    with right:
        st.markdown("### Target job")
        job_description = st.text_area(
            "Paste the complete job description",
            height=210,
            placeholder=(
                "Example: Python, SQL, machine learning, "
                "data preprocessing, model evaluation..."
            ),
            label_visibility="collapsed"
        )

    submitted = st.form_submit_button(
        "Analyze my resume →",
        type="primary",
        use_container_width=True
    )


# ---------------- ANALYSIS ----------------
if submitted:
    if uploaded_file is None:
        st.error("Please upload a PDF resume first.")

    elif not job_description.strip():
        st.error("Please paste the job description first.")

    else:
        temp_path = None

        try:
            with st.spinner("Reading your resume and comparing skills..."):
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf",
                    delete=False
                ) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = Path(temp_file.name)

                resume_text = extract_resume_text(str(temp_path))

                results = analyze_resume(
                    resume_text,
                    job_description
                )
                st.session_state.resume_text = resume_text
                st.session_state.analysis_results = results

            score = results["similarity_score"]

            st.markdown(
                '<div class="section-title">02 · Your analysis</div>',
                unsafe_allow_html=True
            )

            # Summary metrics
            c1, c2, c3 = st.columns(3, gap="medium")

            with c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">TEXT SIMILARITY</div>
                    <div class="metric-value">{score:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">MATCHING SKILLS</div>
                    <div class="metric-value">
                        {len(results["matching_skills"])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">POTENTIAL SKILL GAPS</div>
                    <div class="metric-value">
                        {len(results["missing_skills"])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.progress(
                min(max(score / 100, 0.0), 1.0)
            )

            st.caption(
                "Similarity measures text overlap; it is not "
                "a hiring probability or a validated suitability score."
            )

            # Skill results
            st.markdown(
                '<div class="section-title">03 · Skills breakdown</div>',
                unsafe_allow_html=True
            )

            matching_col, missing_col = st.columns(2, gap="large")

            with matching_col:
                st.markdown(
                    '<div class="panel"><h3>✓ Matching skills</h3>',
                    unsafe_allow_html=True
                )

                skills = results["matching_skills"]

                if skills:
                    html = "".join(
                        f'<span class="skill">{skill}</span>'
                        for skill in skills
                    )
                    st.markdown(html, unsafe_allow_html=True)
                else:
                    st.write("No matching predefined skills detected.")

                st.markdown("</div>", unsafe_allow_html=True)

            with missing_col:
                st.markdown(
                    '<div class="panel"><h3>＋ Skills to review</h3>',
                    unsafe_allow_html=True
                )

                skills = results["missing_skills"]

                if skills:
                    html = "".join(
                        f'<span class="skill missing">{skill}</span>'
                        for skill in skills
                    )
                    st.markdown(html, unsafe_allow_html=True)
                else:
                    st.write("No missing predefined skills detected.")

                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(
                '<div class="section-title">04 · Resume skill inventory</div>',
                unsafe_allow_html=True
            )

            resume_skills = results["resume_skills"]

            if resume_skills:
                st.write(", ".join(resume_skills))
            else:
                st.info(
                    "No predefined skills were detected. "
                    "Check that your PDF contains selectable text."
                )

            report = (
                "RESUMEIQ ANALYSIS REPORT\n\n"
                f"Text similarity: {score:.2f}%\n\n"
                f"Resume skills: {', '.join(resume_skills)}\n\n"
                f"Matching skills: "
                f"{', '.join(results['matching_skills'])}\n\n"
                f"Potential skill gaps: "
                f"{', '.join(results['missing_skills'])}\n\n"
                "Note: Similarity is not a hiring probability.\n"
            )

            st.download_button(
                "Download analysis report",
                data=report,
                file_name="resumeiq_report.txt",
                mime="text/plain"
            )

        except Exception as error:
            st.error("The analysis could not be completed.")
            st.write("Error details — share these if you need help:")
            st.exception(error)

        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)


# ---------------- FOOTER ----------------
# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer-note">
    <strong>ResumeIQ</strong>
    <br>
    Your next career move starts here.
    <br>
    © 2026 ResumeIQ
</div>
""", unsafe_allow_html=True)


# ---------------- RESUME PDF BUILDER ----------------

st.divider()

st.markdown(
    '<div class="section-title">'
    '05 · Build your improved resume</div>',
    unsafe_allow_html=True,
)

st.write(
    "Edit the sections below, review your content, "
    "and generate a new professional PDF. "
    "Keep all qualifications and experience truthful."
)

with st.form("resume_builder_form"):
    name = st.text_input("Full name")
    email = st.text_input("Email address")
    phone = st.text_input("Phone number")

    summary = st.text_area(
        "Professional summary",
        height=110,
        placeholder=(
            "Write a short summary of your actual "
            "education, strengths and career interests."
        ),
    )

    skills = st.text_area(
        "Technical skills",
        height=100,
        placeholder="Python, SQL, Pandas, scikit-learn...",
    )

    experience = st.text_area(
    "Experience",
    height=160,
    placeholder=(
        "Job Title | Company | Dates\n"
        "Describe a real responsibility or achievement.\n"
        "Add measurable results when you have evidence."
    ),
)

    education = st.text_area(
        "Education",
        height=100,
        placeholder=(
            "Degree | University | Expected graduation\n"
            "Add actual academic details."
        ),
    )

    projects = st.text_area(
    "Projects",
    height=150,
    placeholder=(
        "Project Name | Technologies\n"
        "What you built and why.\n"
        "Methods used and results achieved."
    ),
)
    build_clicked = st.form_submit_button(
        "Generate improved resume PDF",
        type="primary",
        use_container_width=True,
    )

if build_clicked:
    if not name.strip():
        st.error("Please enter your full name.")
    elif not any([
        summary.strip(),
        skills.strip(),
        experience.strip(),
        education.strip(),
        projects.strip(),
    ]):
        st.error("Please enter at least one resume section.")
    else:
        try:
            pdf_bytes = generate_resume_pdf(
                name=name,
                email=email,
                phone=phone,
                summary=summary,
                skills=skills,
                experience=experience,
                education=education,
                projects=projects,
            )

            st.success(
                "Your new resume PDF is ready."
            )

            st.download_button(
                "Download your improved resume",
                data=pdf_bytes,
                file_name="improved_resume.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )

        except Exception as error:
            st.error("Could not generate the PDF.")
            st.exception(error)

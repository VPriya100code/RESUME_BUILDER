import streamlit as st
import joblib

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4

st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="💼",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #c2e9fb, #a1c4fd);
    font-family: 'Segoe UI', sans-serif;
}

h1 {
    text-align: center;
    color: #0f172a;
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    text-align: center;
    color: #334155;
    font-size: 16px;
    margin-bottom: 40px;
}

.card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 12px;
}

.stButton > button {
    background: linear-gradient(to right, #6366f1, #8b5cf6);
    color: white;
    border-radius: 30px;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
    border: none;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(to right, #8b5cf6, #6366f1);
}

.stDownloadButton > button {
    background: linear-gradient(to right, #22c55e, #16a34a);
    color: white;
    border-radius: 30px;
    height: 48px;
    font-weight: 600;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

model = joblib.load("job_role_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.markdown("<h1>📄 AI Resume Builder</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Smart resumes powered by Machine Learning & AI</div>",
    unsafe_allow_html=True
)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>👤 Personal Information</div>", unsafe_allow_html=True)
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
linkedin = st.text_input("LinkedIn Profile URL")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>💼 Professional Details</div>", unsafe_allow_html=True)
skills = st.text_area("Skills (comma separated)")
education = st.text_area("Education")
projects = st.text_area("Projects")
experience = st.text_area("Experience")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🏆 Achievements & Certifications</div>", unsafe_allow_html=True)
achievements = st.text_area("Achievements")
certifications = st.text_area("Certifications")
st.markdown("</div>", unsafe_allow_html=True)

role = ""
if skills.strip():
    skills_vec = vectorizer.transform([skills])
    role = model.predict(skills_vec)[0]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🎯 Recommended Job Role</div>", unsafe_allow_html=True)
    st.markdown(
        f"<h2 style='color:#4f46e5;margin-top:5px'>{role}</h2>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

def create_pdf(data):
    file_name = "Professional_Resume.pdf"

    doc = SimpleDocTemplate(
        file_name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="NameStyle",
        fontSize=18,
        leading=22,
        spaceAfter=10,
        fontName="Helvetica-Bold"
    ))

    styles.add(ParagraphStyle(
        name="HeadingStyle",
        fontSize=12,
        leading=16,
        spaceBefore=14,
        spaceAfter=6,
        fontName="Helvetica-Bold"
    ))

    styles.add(ParagraphStyle(
        name="BodyStyle",
        fontSize=10,
        leading=14,
        spaceAfter=6
    ))

    content = []

    content.append(Paragraph(data["name"], styles["NameStyle"]))
    content.append(Paragraph(data["role"], styles["BodyStyle"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        f"<b>Email:</b> {data['email']} &nbsp;&nbsp; "
        f"<b>Phone:</b> {data['phone']}<br/>"
        f"<b>LinkedIn:</b> {data['linkedin']}",
        styles["BodyStyle"]
    ))

    def add_section(title, text):
        if text.strip():
            content.append(Paragraph(title, styles["HeadingStyle"]))
            content.append(
                Paragraph(text.replace("\n", "<br/>"), styles["BodyStyle"])
            )

    add_section("PROFESSIONAL SUMMARY",
                f"Motivated and detail-oriented {data['role']} with strong expertise in {data['skills']}.")
    add_section("EDUCATION", data["education"])
    add_section("PROJECTS", data["projects"])
    add_section("EXPERIENCE", data["experience"])
    add_section("ACHIEVEMENTS", data["achievements"])
    add_section("CERTIFICATIONS", data["certifications"])
    add_section("SKILLS", data["skills"])

    doc.build(content)
    return file_name

if st.button("✨ Generate Professional Resume"):
    resume_data = {
        "name": name,
        "role": role,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "skills": skills,
        "education": education,
        "projects": projects,
        "experience": experience,
        "achievements": achievements,
        "certifications": certifications
    }

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📄 Resume Preview</div>", unsafe_allow_html=True)

    st.text(f"""
{name}
{role}

Email: {email}
Phone: {phone}
LinkedIn: {linkedin}

SUMMARY
Motivated and detail-oriented {role} with strong expertise in {skills}.

EDUCATION
{education}

PROJECTS
{projects}

EXPERIENCE
{experience}

ACHIEVEMENTS
{achievements}

CERTIFICATIONS
{certifications}

SKILLS
{skills}
""")

    st.markdown("</div>", unsafe_allow_html=True)

    pdf_file = create_pdf(resume_data)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "⬇️ Download Resume as PDF",
            f,
            file_name="Professional_Resume.pdf",
            mime="application/pdf"
        )

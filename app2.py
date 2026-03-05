import streamlit as st
import pickle
import numpy as np

# ---------- Page config ----------
st.set_page_config(
    page_title="Student Dropout Prediction",
    page_icon="🎓",
    layout="centered"
)
# ---------- Custom CSS ----------
st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(135deg, #0E1117 0%, #121826 100%);
    color: #EAEAF0;
}

/* Header */
.header {
    text-align: center;
    padding: 18px 0 8px 0;
}
.header h1 {
    margin-bottom: 6px;
    font-size: 34px;
    background: linear-gradient(90deg, #FF6F61, #FFB703);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header p {
    color: #B8C0CC;
}

/* Card */
.card {
    background: #0B1220;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,.35);
    margin-bottom: 14px;
}

/* Button */
div.stButton > button {
    background: linear-gradient(90deg, #FF6F61, #FFB703);
    color: #111;
    border-radius: 12px;
    height: 3.2em;
    width: 100%;
    font-size: 16px;
    font-weight: 800;
    border: none;
}

/* Slider accent */
div[data-testid="stSlider"] > div { color: #FFB703; }

/* Badges */
.badge-high { color:#FF5252; font-weight:900; }
.badge-mid  { color:#FFC107; font-weight:900; }
.badge-low  { color:#4CAF50; font-weight:900; }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="header">
  <h1>STUDENT DROPOUT PREDICTION SYSTEM</h1>
  <p>ML-based early risk detection for academic intervention</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("ℹ️ About")
    st.write(
        "This app predicts the *dropout risk* using a trained "
        "Logistic Regression model based on academic & socio-economic factors."
    )
    st.caption("Built with Python • scikit-learn • Streamlit")

# ---------- Load model ----------
model = pickle.load(open("model.pkl", "rb"))

# ---------- Inputs ----------
st.markdown("<div class='card'><h3>📥 Student Details</h3></div>", unsafe_allow_html=True)

attendance = st.slider("Attendance (%)", 0, 100, 75)
marks = st.slider("Marks", 0, 100, 60)
study_hours = st.slider("Study hours per Day", 0, 10, 2)
backlogs = st.number_input("Backlogs", 0, 10, 1)
income = st.number_input("Family Income (₹/month)", 1000, 100000, 30000)
distance = st.slider("Distance from College (km)", 1, 50, 5)
internet = st.selectbox("Internet Access", ["Yes", "No"])
internet = 1 if internet == "Yes" else 0

# ---------- Predict ----------
st.markdown("<div class='card'><h3>📊 Prediction</h3></div>", unsafe_allow_html=True)

if st.button("Predict Dropout Risk"):
    user_input = np.array([[attendance, marks, study_hours,
                            backlogs, income, distance, internet]])

    prob = model.predict_proba(user_input)[0][1]
    st.info(f"Dropout Probability: *{prob*100:.2f}%*")

    # Progress bar
    st.progress(min(int(prob*100), 100))

    # Risk badge
    if prob > 0.7:
        st.markdown("<span class='badge-high'>HIGH RISK OF DROPOUT</span>", unsafe_allow_html=True)
    elif prob > 0.4:
        st.markdown("<span class='badge-mid'>MEDIUM RISK OF DROPOUT</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge-low'>LOW RISK OF DROPOUT</span>", unsafe_allow_html=True)
import streamlit as st
import pickle
import numpy as np
model = pickle.load(open('model.pkl', 'rb'))
st.title("STUDENT DROPOUT PREDICTION SYSTEM")
attendance= st.slider("Attendance (%)", 0, 100, 75)
marks= st.slider("Marks", 0, 100, 60)
study_hours = st.slider("Study hours per Day", 0, 10, 2)
backlogs = st.number_input("Backlogs", 0, 10, 1)
income= st.number_input("Family Income", 1000, 100000, 30000)
distance= st.slider("Distance from College(km)", 1, 50, 5)
internet= st.selectbox("Internet Access", ["Yes","No"])
internet= 1 if internet =="Yes" else 0




if st.button("Predict Dropout Risk"):
    user_input =np.array([[attendance,marks,study_hours,backlogs,income,distance,internet]])
    result=model.predict(user_input)
    prob = model.predict_proba(user_input)[0][1]
    st.info(f"Dropout Probability:{prob * 100: .2f}%")
    if prob > 0.7:
        st.error("HIGH RISK OF DROPOUT")
    elif prob > 0.4:
        st.warning("MEDIUM RISK OF DROPOUT")
    else:
        st.success("LOW RISK OF DROPOUT")
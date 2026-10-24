import streamlit as st

st.set_page_config(
    page_title="MealMatch",
    page_icon="🥗",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

.stApp {
    background-color: #FAF8F2;
    font-family: 'Nunito', sans-serif;
}

h1, h2, h3 {
    color: #315C45;
}

[data-testid="stSidebar"] {
    background-color: #F0F2E8;
}

.stButton > button {
    background-color: #477653;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.title("🥗 MealMatch")
st.subheader("Meals that match your budget, schedule, and taste.")

st.write(
    "Welcome to MealMatch! Find affordable meals "
    "based on your preferences and lifestyle."
)

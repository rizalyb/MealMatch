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
# Sidebar: Student Preferences

with st.sidebar:
    st.title("⚙️ Your Preferences")
    st.write("Customize your meal recommendations.")

    st.subheader("Budget")
    budget = st.slider(
        "Budget per meal ($)",
        min_value=1,
        max_value=30,
        value=10
    )

    weekly_budget = st.slider(
        "Weekly budget ($)",
        min_value=10,
        max_value=200,
        value=30,
        step=5
    )

    st.subheader("Cooking")
    max_time = st.slider(
        "Maximum cooking time (minutes)",
        min_value=5,
        max_value=120,
        value=30,
        step=5
    )

    desired_servings = st.selectbox(
        "How many people are you cooking for?",
        options=[1, 2, 3, 4, 5, 6]
    )

    plan_days = st.selectbox(
        "How many days do you want to plan?",
        options=[1, 3, 5, 7]
    )

    st.subheader("Food Preferences")
    dietary_restrictions = st.selectbox(
        "Dietary restrictions",
        options=[
            "None",
            "Vegetarian",
            "Vegan",
            "Gluten-free",
            "Dairy-free"
        ]
    )

    food_preferences = st.text_input(
        "Foods to avoid",
        placeholder="e.g., seafood, mushrooms"
    )

    st.subheader("Nutrition Goals")
    max_calories = st.number_input(
        "Maximum calories per serving (0 = no limit)",
        min_value=0,
        max_value=2000,
        value=0,
        step=50
    )

    min_protein = st.number_input(
        "Minimum protein per serving (g)",
        min_value=0,
        max_value=150,
        value=0,
        step=5
    )

st.title("🥗 MealMatch")
st.subheader("Meals that match your budget, schedule, and taste.")

st.write(
    "Welcome to MealMatch! Find affordable meals "
    "based on your preferences and lifestyle."
)

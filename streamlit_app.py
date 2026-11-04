import streamlit as st

st.set_page_config(
    page_title="MealMatch",
    page_icon="🥗",
    layout="wide"
)

home_page = st.Page(
    "pages/1_Home.py",
    title="Home",
    icon="🏠",
    default=True
)

planner_page = st.Page(
    "pages/2_Meal_Planner.py",
    title="Meal Planner",
    icon="🍽️"
)

grocery_page = st.Page(
    "pages/3_Grocery_List.py",
    title="Grocery List",
    icon="🛒"
)

# SIDEBAR PREFERENCES

st.sidebar.title("⚙️ Meal Preferences")

budget = st.sidebar.slider(
    "Budget per meal ($)",
    min_value=1,
    max_value=30,
    value=10,
    key="budget"
)

use_weekly_budget = st.sidebar.checkbox(
    "Set a weekly budget",
    value=False,
    key="use_weekly_budget"
)

weekly_budget = 30

if use_weekly_budget:
    weekly_budget = st.sidebar.slider(
        "Weekly budget ($)",
        min_value=10,
        max_value=200,
        value=30,
        step=5,
        key="weekly_budget"
    )

use_time_limit = st.sidebar.checkbox(
    "Set maximum cooking time",
    value=True,
    key="use_time_limit"
)

max_time = 30

if use_time_limit:
    max_time = st.sidebar.slider(
        "Maximum cooking time (minutes)",
        min_value=5,
        max_value=120,
        value=30,
        step=5,
        key="max_time"
    )

desired_servings = st.sidebar.selectbox(
    "Number of servings",
    [1, 2, 3, 4, 5, 6],
    index=0,
    key="desired_servings"
)

plan_days = st.sidebar.selectbox(
    "Number of days to plan",
    [1, 3, 5, 7],
    index=0,
    key="plan_days"
)

dietary_restrictions = st.sidebar.selectbox(
    "Dietary restrictions",
    [
        "None",
        "Vegetarian",
        "Vegan",
        "Gluten-free",
        "Dairy-free"
    ],
    key="dietary_restrictions"
)

food_preferences = st.sidebar.text_input(
    "Foods to avoid",
    placeholder="Example: seafood, mushrooms",
    key="food_preferences"
)

use_calorie_limit = st.sidebar.checkbox(
    "Set maximum calories",
    value=False,
    key="use_calorie_limit"
)

max_calories = 500

if use_calorie_limit:
    max_calories = st.sidebar.number_input(
        "Maximum calories per serving",
        min_value=50,
        max_value=2000,
        value=500,
        step=50,
        key="max_calories"
    )

use_protein_goal = st.sidebar.checkbox(
    "Set minimum protein goal",
    value=False,
    key="use_protein_goal"
)

min_protein = 20

if use_protein_goal:
    min_protein = st.sidebar.number_input(
        "Minimum protein (g)",
        min_value=1,
        max_value=150,
        value=20,
        step=5,
        key="min_protein"
    )

st.sidebar.divider()

navigation = st.navigation([
    home_page,
    planner_page,
    grocery_page
])

navigation.run()

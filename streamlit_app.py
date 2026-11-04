
import streamlit as st
import pandas as pd
from pathlib import Path

# PAGE CONFIGURATION

st.set_page_config(
    page_title="MealMatch",
    page_icon="🥗",
    layout="wide"
)

APP_DIR = Path(__file__).parent


# GLOBAL MEALMATCH DESIGN

st.markdown(
    """
    <style>

    /* THEME COLORS */

    :root {
        --mm-green: #426548;
        --mm-dark-green: #294B35;
        --mm-light-green: #E8EEDF;
        --mm-cream: #F8F7F0;
        --mm-border: #D5DEC9;
    }

    /* LIGHT MODE */

    [data-testid="stAppViewContainer"] {
        background-color: var(--mm-cream);
    }

    [data-testid="stSidebar"] {
        background-color: var(--mm-light-green);
    }

    [data-testid="stSidebar"] * {
        color: #294B35;
    }

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {
        color: #294B35;
    }

    /* MAIN CONTENT */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* SIDEBAR EXPANDERS */

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #F4F5ED;
        border: 1px solid #D5DEC9;
        border-radius: 12px;
    }

    /* SLIDERS */

    [data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: inherit !important;
        font-weight: 700 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    [data-testid="stSlider"] [data-testid="stTickBar"] {
        color: inherit !important;
    }

    /* INPUT LABELS */

    [data-testid="stSidebar"] label {
        font-weight: 500;
    }

    [data-testid="stSidebar"] input {
        color: inherit !important;
    }

    /* CARDS */

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--mm-border);
        border-radius: 14px;
    }

    /* BUTTONS */

    .stButton button,
    .stLinkButton a {
        background-color: var(--mm-green);
        color: white !important;
        border: none;
        border-radius: 10px;
    }

    .stButton button:hover,
    .stLinkButton a:hover {
        background-color: var(--mm-dark-green);
        color: white !important;
    }

    /* DIVIDERS */

    hr {
        border-color: var(--mm-border);
    }

    /* DARK MODE */

    [data-theme="dark"] [data-testid="stAppViewContainer"],
    [data-theme="dark"] .stApp {
        background-color: #18251D;
    }

    [data-theme="dark"] [data-testid="stSidebar"] {
        background-color: #223329;
    }

    [data-theme="dark"] [data-testid="stSidebar"] * {
        color: #E5EDE2;
    }

    [data-theme="dark"] [data-testid="stAppViewContainer"] h1,
    [data-theme="dark"] [data-testid="stAppViewContainer"] h2,
    [data-theme="dark"] [data-testid="stAppViewContainer"] h3 {
        color: #DCE9D9;
    }

    [data-theme="dark"] [data-testid="stAppViewContainer"] p {
        color: #D0DBCE;
    }

    [data-theme="dark"] [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #2C4032;
        border-color: #465B49;
    }

    [data-theme="dark"] [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #465B49;
    }

    [data-theme="dark"] hr {
        border-color: #465B49;
    }

    [data-theme="dark"] [data-testid="stSlider"] {
        color: #E5EDE2;
    }

    [data-theme="dark"] [data-testid="stSidebar"] label {
        color: #E5EDE2;
    }

    [data-theme="dark"] [data-testid="stSidebar"] input {
        color: #E5EDE2 !important;
    }

    [data-theme="dark"] [data-testid="stAppViewContainer"] [data-testid="stAlert"] {
        color: #E5EDE2;
    }

    /* REMOVE TOP HEADER BACKGROUND */

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# LOAD CSV DATA

@st.cache_data
def load_meal_data():

    meals = pd.read_csv(
        APP_DIR / "Rizaly Barlam - MealMatch CSV(Meals).csv",
        encoding="cp1252"
    )

    ingredients = pd.read_csv(
        APP_DIR / "Rizaly Barlam - MealMatch CSV(Ingredients).csv",
        encoding="cp1252"
    )

    return meals, ingredients


meals, ingredients = load_meal_data()

st.session_state["meals"] = meals
st.session_state["ingredients"] = ingredients


# SIDEBAR PREFERENCES

st.sidebar.title("🥗 MealMatch")

st.sidebar.caption(
    "Customize your meal recommendations."
)

st.sidebar.divider()


# BUDGET

with st.sidebar.expander("💰 Budget", expanded=True):

    budget = st.slider(
        "Budget per meal ($)",
        1,
        30,
        10,
        key="budget"
    )

    use_weekly_budget = st.checkbox(
        "Set a weekly budget",
        value=False,
        key="use_weekly_budget"
    )

    if use_weekly_budget:

        weekly_budget = st.slider(
            "Weekly budget ($)",
            10,
            200,
            30,
            step=5,
            key="weekly_budget"
        )

    else:
        weekly_budget = 30
        st.session_state["weekly_budget"] = weekly_budget

st.session_state["weekly_budget"] = weekly_budget


# COOKING AND PLANNING

with st.sidebar.expander("⏱️ Cooking & Planning", expanded=True):

    use_time_limit = st.checkbox(
        "Set maximum cooking time",
        value=True,
        key="use_time_limit"
    )

    if use_time_limit:

        max_time = st.slider(
            "Maximum cooking time (minutes)",
            5,
            120,
            30,
            step=5,
            key="max_time"
        )

    else:
        max_time = None
        st.session_state["max_time"] = None

    desired_servings = st.selectbox(
        "Number of servings",
        [1, 2, 3, 4, 5, 6],
        key="desired_servings"
    )

    plan_days = st.selectbox(
        "Number of days to plan",
        [1, 3, 5, 7],
        key="plan_days"
    )


# FOOD PREFERENCES

with st.sidebar.expander("🥦 Food Preferences", expanded=False):

    dietary_restrictions = st.selectbox(
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

    food_preferences = st.text_input(
        "Foods to avoid",
        placeholder="Example: seafood, mushrooms",
        key="food_preferences"
    )


# NUTRITION GOALS

with st.sidebar.expander("❤️ Nutrition Goals", expanded=False):

    use_calorie_limit = st.checkbox(
        "Set maximum calories",
        value=False,
        key="use_calorie_limit"
    )

    if use_calorie_limit:

        max_calories = st.number_input(
            "Maximum calories per serving",
            50,
            2000,
            500,
            step=50,
            key="max_calories"
        )

    else:
        max_calories = None
        st.session_state["max_calories"] = None

    use_protein_goal = st.checkbox(
        "Set minimum protein goal",
        value=False,
        key="use_protein_goal"
    )

    if use_protein_goal:

        min_protein = st.number_input(
            "Minimum protein (g)",
            1,
            150,
            20,
            step=5,
            key="min_protein"
        )

    else:
        min_protein = None
        st.session_state["min_protein"] = None


# PAGE NAVIGATION

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

explore_page = st.Page(
    "pages/4_Explore_Meals.py",
    title="Explore Meals",
    icon="📖"
)

st.session_state["planner_page"] = planner_page
st.session_state["grocery_page"] = grocery_page
st.session_state["explore_page"] = explore_page

navigation = st.navigation([
    home_page,
    planner_page,
    grocery_page,
    explore_page
])

navigation.run()
